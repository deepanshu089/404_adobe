# Approach Explanation – Round 1B

## Problem Statement
Given a structured JSON (from Round 1A) and a persona/job description, extract and rank the most relevant sections and provide fine-grained highlights and summaries.

## Key Steps & Logic
1. **Input Handling:**
   - Accepts JSON files (from structure extractor) via `--input` argument.
   - Outputs enriched JSONs in the `output` directory.
2. **Embedding & Similarity:**
   - Loads a local SentenceTransformer model (`all-MiniLM-L6-v2`).
   - Embeds the persona/job and all section texts.
   - Ranks sections by cosine similarity to the persona/job.
3. **Highlighting & Summarization:**
   - For top-ranked sections, extracts most relevant sentences/paragraphs and generates summaries using TextRank.
4. **Batch Processing:**
   - Processes all JSONs in the input directory.
   - Outputs one enriched JSON per input.
5. **Dockerization:**
   - Fully dockerized for reproducibility and platform compatibility.

## Features & Compliance
- **No hardcoded paths:** All scripts use arguments for input/output.
- **CPU-only, AMD64:** Dockerfile enforces platform compatibility.
- **No network calls:** Fully offline; model loaded locally.
- **Model size:** <1GB, meets requirements.
- **Runtime:** <60s per doc.
- **Output:** Only writes to `/output`, never commits outputs to git (except sample).
- **Modular code:** Well-documented, easy to extend.
- **Multilingual:** Model supports multiple languages.

## Usage
```sh
docker build -t round1b_persona:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output round1b_persona:latest --input /app/input --output /app/output
```

## Notes
- See `README.md` for more details and sample commands.
