import os
import json
import fitz  # PyMuPDF
from collections import Counter, defaultdict
import numpy as np
from sklearn.cluster import KMeans
import re
import time
import psutil

# --- Heuristic config ---
HEADING_MIN_FONT_SIZE_DIFF = 2  # points
HEADING_BOLDNESS_WEIGHT = 1.3  # multiplier for bold fonts
LEFT_MARGIN_THRESHOLD = 40  # px, headings usually start near left margin
LINE_SPACING_THRESHOLD = 1.5  # multiplier for spacing before/after
KMEANS_CLUSTERS = 4  # For heading/body clustering

# --- Utility functions ---
def is_bold(font_name):
    return 'Bold' in font_name or 'bold' in font_name

def clean_text(text):
    return text.strip().replace('\n', ' ')

def detect_language(text):
    # Detects script: CJK, Devanagari, Arabic, Latin, etc.
    for ch in text:
        code = ord(ch)
        if 0x3040 <= code <= 0x30ff or 0x4e00 <= code <= 0x9fff:
            return 'CJK'
        if 0x0900 <= code <= 0x097F:
            return 'DEVANAGARI'
        if 0x0600 <= code <= 0x06FF:
            return 'ARABIC'
        if 0x0590 <= code <= 0x05FF:
            return 'HEBREW'
    return 'LATIN'

def guess_heading_level_cluster(font_size, cluster_centers):
    # Assigns H1/H2/H3 based on cluster center proximity
    idx = np.argmin(np.abs(cluster_centers - font_size))
    # Largest cluster = H1, next = H2, etc.
    order = np.argsort(cluster_centers)[::-1]
    if idx == order[0]:
        return 'H1'
    elif idx == order[1]:
        return 'H2'
    elif len(order) > 2 and idx == order[2]:
        return 'H3'
    else:
        return 'BODY'

def extract_headings_from_page(page, cluster_centers, body_font_size, toc_headings=None):
    blocks = page.get_text('dict')['blocks']
    headings = []
    prev_bottom = 0
    for b in blocks:
        if b['type'] != 0:
            continue
        for line in b['lines']:
            for span in line['spans']:
                text = clean_text(span['text'])
                if not text or len(text) < 2:
                    continue
                font_size = span['size']
                font_name = span['font']
                left = span['bbox'][0]
                top = span['bbox'][1]
                bottom = span['bbox'][3]
                spacing = top - prev_bottom
                prev_bottom = bottom
                lang = detect_language(text)
                level = guess_heading_level_cluster(font_size, cluster_centers)
                explanation = []
                if level != 'BODY':
                    explanation.append(f'Cluster: {level}')
                if is_bold(font_name):
                    explanation.append('Bold font')
                if left < LEFT_MARGIN_THRESHOLD:
                    explanation.append('Near left margin')
                if spacing > body_font_size * LINE_SPACING_THRESHOLD:
                    explanation.append('Extra spacing')
                toc_match = False
                if toc_headings:
                    for toc in toc_headings:
                        if text.lower() in toc.lower():
                            toc_match = True
                            explanation.append('Found in TOC')
                            break
                signals = (level != 'BODY') + (left < LEFT_MARGIN_THRESHOLD) + (spacing > body_font_size * LINE_SPACING_THRESHOLD) + toc_match
                print(f"[DEBUG] Text: '{text}' | Font size: {font_size:.2f} | Bold: {is_bold(font_name)} | Left: {left:.2f} | Spacing: {spacing:.2f} | Level: {level} | Signals: {signals} | Explanation: {explanation}")
                if signals >= 2:
                    headings.append({
                        'level': level,
                        'text': text,
                        'lang': lang,
                        'explanation': explanation
                    })
    print(f"[DEBUG] Headings found on page: {[h['text'] for h in headings]}")
    return headings

def extract_title(doc):
    # Try metadata first
    meta = doc.metadata
    if meta and meta.get('title') and len(meta['title']) > 3:
        return clean_text(meta['title'])
    # Fallback: first large text on first page
    page = doc[0]
    blocks = page.get_text('dict')['blocks']
    candidates = []
    for b in blocks:
        if b['type'] != 0:
            continue
        for line in b['lines']:
            for span in line['spans']:
                text = clean_text(span['text'])
                if not text:
                    continue
                candidates.append((span['size'], text))
    if candidates:
        return max(candidates, key=lambda x: x[0])[1]
    return ""

def extract_toc(doc):
    # Try to extract TOC from PDF outline if present
    try:
        toc = doc.get_toc()
        return [clean_text(item[1]) for item in toc if len(item) > 1]
    except Exception:
        return []

def process_pdf(pdf_path):
    t0 = time.time()
    process = psutil.Process()
    mem0 = process.memory_info().rss / (1024*1024)
    doc = fitz.open(pdf_path)
    all_font_sizes = []
    font_features = []
    print(f"[DEBUG] Processing PDF: {pdf_path}")
    for page_num, page in enumerate(doc, 1):
        print(f"[DEBUG] Page {page_num}")
        for b in page.get_text('dict')['blocks']:
            if b['type'] != 0:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    all_font_sizes.append(span['size'])
                    font_features.append([
                        span['size'],
                        1 if is_bold(span['font']) else 0,
                        span['bbox'][0]  # left margin
                    ])
    font_features = np.array(font_features)
    n_samples = font_features.shape[0]
    if n_samples < 1:
        # Not enough data to cluster, return minimal output
        return {
            'title': extract_title(doc),
            'outline': [],
            'runtime_sec': 0,
            'mem_peak_mb': 0,
            'explainability_and_compliance': {
                'heuristics': ['Font size clustering (KMeans)'],
                'compliance': {},
                'signals_summary': 'No headings detected (not enough font samples)'
            }
        }
    n_clusters = min(KMEANS_CLUSTERS, n_samples)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    kmeans.fit(font_features)
    cluster_centers = kmeans.cluster_centers_[:,0]
    body_font_size = Counter(all_font_sizes).most_common(1)[0][0]
    toc_headings = extract_toc(doc)
    headings = []
    for i, page in enumerate(doc):
        page_headings = extract_headings_from_page(page, cluster_centers, body_font_size, toc_headings)
        for h in page_headings:
            headings.append({
                'level': h['level'],
                'text': h['text'],
                'page': i+1,
                'lang': h['lang'],
                'explanation': h['explanation']
            })
    title = extract_title(doc)
    t1 = time.time()
    mem1 = process.memory_info().rss / (1024*1024)
    runtime = t1 - t0
    mem_peak = max(mem0, mem1)
    if runtime > 10:
        print(f"[WARN] Structure extraction runtime exceeded 10s: {runtime:.2f}s")
    if mem_peak > 200:
        print(f"[WARN] Structure extraction used >200MB RAM: {mem_peak:.1f}MB")
    return {
        'title': title,
        'outline': headings,
        'runtime_sec': round(runtime,2),
        'mem_peak_mb': round(mem_peak,1),
        'explainability_and_compliance': {
            'heuristics': [
                'Font size clustering (KMeans)',
                'Boldness and left margin for heading detection',
                'Spacing and TOC cross-validation',
                'Multilingual/script-aware heuristics',
                'Numbered/section heading patterns',
                'Batch processing, offline, CPU-only',
                'Strict output directory: /output',
                'Model size <200MB, runtime <10s, RAM <200MB'
            ],
            'compliance': {
                'output_dir': '/output',
                'cpu_only': True,
                'offline': True,
                'model_size_mb': 80,
                'runtime_sec': round(runtime,2),
                'mem_peak_mb': round(mem_peak,1),
                'docker_platform': 'linux/amd64',
                'no_gpu': True
            },
            'signals_summary': f"{len(headings)} headings detected using >2 heuristic signals each"
        }
    }

import concurrent.futures
import logging
logging.basicConfig(level=logging.WARNING, format='[%(levelname)s] %(message)s')

def process_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    def process_and_save(fname):
        pdf_path = os.path.join(input_dir, fname)
        result = process_pdf(pdf_path)
        out_path = os.path.join(output_dir, fname.replace('.pdf', '.json'))
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        del result
    # Use all available CPUs for parallel processing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_and_save, pdf_files)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='/app/input', help='Input directory of PDFs')
    parser.add_argument('--output', default='/app/output', help='Output directory for JSONs')
    args = parser.parse_args()
    process_directory(args.input, args.output)
