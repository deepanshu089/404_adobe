# Approach Explanation – Round 1A

## Problem Statement
Extract the hierarchical structure (headings, subheadings, etc.) from PDF documents in a robust, language-agnostic way.

## Key Steps & Logic
1. **Input Handling:**
   - Accepts a directory of PDFs as input via `--input` argument.
   - Outputs extracted structure as JSON files in the `output` directory.
2. **PDF Parsing:**
   - Uses PDF parsing libraries to extract text and layout information.
   - Applies heuristics to identify headings based on font size, style, and position.
3. **Hierarchy Construction:**
   - Builds a tree-like structure of headings and subheadings.
   - Handles multi-level nesting and edge cases.
4. **Batch Processing:**
   - Processes all PDFs in the input directory.
   - Outputs one JSON per PDF.
5. **Dockerization:**
   - The solution is packaged with a Dockerfile for reproducibility and easy execution.

## Features & Compliance
- **No hardcoded paths:** All scripts use arguments for input/output.
- **CPU-only, AMD64:** Dockerfile enforces platform compatibility.
- **No network calls:** Fully offline.
- **Runtime:** Designed for <10s per 50-page doc.
- **Output:** Only writes to `/output`, never commits outputs to git (except sample).
- **Modular code:** Well-documented, easy to extend.

## Usage
```sh
docker build -t round1a_structure:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output round1a_structure:latest --input /app/input --output /app/output
```

## Notes
- See `README.md` for more details and sample commands.
