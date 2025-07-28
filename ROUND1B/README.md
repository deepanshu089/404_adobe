# Round 1B: Persona-Driven Document Intelligence

Welcome to the Adobe India Hackathon – Connecting the Dots!

This folder contains the full solution for **Round 1B: Persona-Driven Document Intelligence**. Here, your code acts as an intelligent document analyst: given a persona and job-to-be-done, it finds and ranks the most relevant sections from structured documents.

---

## 🚀 What This Solution Does
- **Input:** Structure JSONs (from Round 1A) in `/app/input`
- **Persona & Job:** Passed as command-line arguments or environment variables
- **Output:** For each input, a JSON file in `/app/output` with:
  - Metadata (persona, job, docs, timestamp)
  - Ranked sections (document, page, section title, importance)
  - Sub-section analysis (optional, for top-ranked sections)
- **No internet required, no hardcoding, <1GB model, ≤60s total runtime**

---

## ⚡️ Offline Model Download Required

This solution requires the `all-MiniLM-L6-v2` model to be available **locally** in a `./model` directory. Before building the Docker image, run:

```python
from sentence_transformers import SentenceTransformer
SentenceTransformer('all-MiniLM-L6-v2').save('./model')
```

Make sure the `./model` directory is present in your project folder and is included in the Docker build context. This ensures **no internet access is needed at runtime** and is required for hackathon compliance.

---

## 🛠️ How to Build & Run

1. **Build the Docker image:**
   ```sh
   docker build --platform linux/amd64 -t round1b_persona:latest .
   ```
2. **Run the solution:**
   ```sh
   docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b_persona:latest \
     --persona "PhD Researcher in Computational Biology" \
     --job "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
   ```
   - All structure JSONs in `input/` will be processed; persona outputs will appear in `output/`.

---

## 📁 Files
- `round1b_persona_intelligence.py` — Main script for persona-driven section ranking
- `Dockerfile` — Build/run instructions (AMD64, CPU-only, offline)
- `requirements.txt` — Only necessary Python dependencies (sentence-transformers, scikit-learn, numpy, PyMuPDF)
- `sample_structure.json` — Example input (structure output from Round 1A)
- `sample_challenge1b_output.json` — Example persona output for demo/testing

---

## 🧠 Approach (Summary)
- **Section Ranking:** Embeds persona/job and all section texts using `sentence-transformers` (all-MiniLM-L6-v2, ~80MB). Computes cosine similarity for ranking.
- **Sub-section Analysis:** For top-ranked sections, further splits and re-ranks for fine-grained insights.
- **Multilingual:** Model and heuristics support multiple languages, including CJK scripts.
- **Performance:** Designed for ≤60s runtime for 3-5 docs, model size <1GB, and strict offline/CPU-only compliance.

---

## ✅ Compliance Checklist
- [x] Dockerfile: AMD64, CPU-only, no GPU/internet
- [x] Model size ≤ 1GB
- [x] Runtime ≤ 60s for 3-5 documents
- [x] No hardcoded logic or network calls
- [x] Batch processes all structure JSONs in `/app/input`
- [x] Outputs only to `/app/output` (not tracked in git)
- [x] README explains approach, build, run, and compliance

---

## 📢 Notes
- **Only process outputs from Round 1A** — see `../round1a/` for structure extraction!
- **Keep `/output` in `.gitignore`** — only sample outputs are tracked for demo.
- **Tested on academic, business, and educational documents, including multilingual content.**

---

For any questions, see the main project README or contact the team. Good luck and happy hacking!
