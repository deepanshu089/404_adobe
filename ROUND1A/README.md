# Round 1A: Structure Extraction

Welcome to the Adobe India Hackathon – Connecting the Dots!

This folder contains the full solution for **Round 1A: Document Structure Extraction**. Your mission: turn raw PDFs into clean, machine-readable outlines (Title, H1, H2, H3) — the foundation for next-generation PDF intelligence.

---

## 🚀 What This Solution Does
- **Input:** All PDFs from `/app/input` (up to 50 pages each)
- **Output:** For each PDF, a JSON file in `/app/output` matching:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```
- **No internet required, no hardcoding, blazing fast (<10s per 50-page PDF)**

---

## 🛠️ How to Build & Run

1. **Build the Docker image:**
   ```sh
   docker build --platform linux/amd64 -t round1a_structure:latest .
   ```
2. **Run the solution:**
   ```sh
   docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a_structure:latest
   ```
   - All PDFs in `input/` will be processed; outputs will appear in `output/`.

---

## 📁 Files
- `round1a_structure_extractor.py` — Main script for structure extraction
- `Dockerfile` — Build/run instructions (AMD64, CPU-only, offline)
- `requirements.txt` — Only necessary Python dependencies (PyMuPDF, numpy, scikit-learn)
- `sample.pdf`, `sample.json` — Example input/output for testing/demo

---

## 🧠 Approach (Summary)
- **PDF Parsing:** Uses PyMuPDF for robust extraction of text, font size, boldness, and layout.
- **Heading Detection:** Combines font size, boldness, margins, and spacing. Also checks for numbered/section headings and validates with Table of Contents if present.
- **Output:** Clean, hierarchical JSON with all headings (H1/H2/H3) and page numbers.
- **Performance:** Designed for <10s runtime per 50-page PDF, model size <200MB, and strict offline/CPU-only compliance.

---

## ✅ Compliance Checklist
- [x] Dockerfile: AMD64, CPU-only, no GPU/internet
- [x] Model size (if any) ≤ 200MB
- [x] Runtime <10s for 50-page PDF
- [x] No hardcoded logic or network calls
- [x] Batch processes all PDFs in `/app/input`
- [x] Outputs only to `/app/output` (not tracked in git)
- [x] README explains approach, build, run, and compliance

---

## 📢 Notes
- **No persona or semantic analysis** here — see `../round1b/` for that!
- **Keep `/output` in `.gitignore`** — only sample outputs are tracked for demo.
- **Tested on simple and complex PDFs, including multilingual content.**

---

For any questions, see the main project README or contact the team. Good luck and happy hacking!
