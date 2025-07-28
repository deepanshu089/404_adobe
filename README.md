# Adobe India Hackathon – Connecting the Dots

This repository contains two offline, dockerized solutions for document intelligence:

- **[ROUND1A](ROUND1A/)**: PDF Structure Extraction  
- **[ROUND1B](ROUND1B/)**: Persona-Driven Section Ranking

---

## 📂 Folder Structure

```
ROUND1A/    # Round 1A: Extracts hierarchical structure from PDFs (Title, H1, H2, H3)
ROUND1B/    # Round 1B: Ranks and highlights sections by persona/job using structure JSONs
```

---

## 🚀 Quick Start

### 1️⃣ Round 1A: Structure Extraction

- **Input:** Place PDFs in `ROUND1A/input/`
- **Output:** Extracted structure JSONs in `ROUND1A/output/`

**Build & Run:**
```sh
cd ROUND1A
docker build --platform linux/amd64 -t round1a_structure:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a_structure:latest
```

See [ROUND1A/README.md](ROUND1A/README.md) for details.

---

### 2️⃣ Round 1B: Persona-Driven Document Intelligence

- **Input:** Place structure JSONs (from Round 1A) in `ROUND1B/input/`
- **Output:** Persona-ranked JSONs in `ROUND1B/output/`
- **Model:** Download [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) to `ROUND1B/model/` before building.

**Build & Run:**
```sh
cd ROUND1B
# Download model (run once)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2').save('./model')"
docker build --platform linux/amd64 -t round1b_persona:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b_persona:latest \
  --persona "PhD Researcher in Computational Biology" \
  --job "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

See [ROUND1B/README.md](ROUND1B/README.md) for details.

---

## 📝 Notes

- Both solutions are **offline**, **CPU-only**, and require **no internet at runtime**.
- Outputs are written only to the `output/` folders (not tracked in git).
- For sample inputs/outputs and compliance details, see the respective subfolders.

---

Good luck
