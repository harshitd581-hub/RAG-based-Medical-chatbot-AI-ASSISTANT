Run the script with the project's virtual environment

The script `create_memory_for_llm.py` uses `langchain_community` and `langchain_text_splitters` packages. If you see import errors like `No module named 'langchain.text_splitter'`, the fix is to use `langchain_text_splitters` for `RecursiveCharacterTextSplitter`.

Recommended steps (macOS, zsh):

1. Activate the venv (if created in this repo):

```bash
source ./venv/bin/activate
```

2. Install dependencies (if not already):

```bash
pip install -r requirements.txt
# or install packages shown in the project
```

3. Run the script with the venv python (ensures installed packages are used):

```bash
cd "/Users/harshitdubey/Desktop/MEDICAL CHATBOT"
./venv/bin/python3 create_memory_for_llm.py
```

This will load PDFs from the `data/` folder, create text chunks, compute embeddings with `HuggingFaceEmbeddings`, and save a FAISS index under `vectorstore/db_faiss`.

Notes:
- `langchain-community` is deprecated; consider migrating to supported packages in future updates.
- If you get HF Hub rate-limit warnings, set the `HF_TOKEN` environment variable.

Running the Streamlit app (medibot)

If you plan to run the Streamlit UI (`medibot.py`):

1. Activate the project venv so the installed packages are available:

```bash
source ./venv/bin/activate
```

2. Run the Streamlit app using the venv's streamlit executable (recommended):

```bash
./venv/bin/streamlit run medibot.py
```

or (if the venv is activated):

```bash
streamlit run medibot.py
```

Note: If you run `python medibot.py` without activating the venv, you may see errors like `ModuleNotFoundError: No module named 'langchain_huggingface'` because your system Python may not have the same packages installed.

Troubleshooting: `sentence-transformers` or other package import errors

If the app shows errors like "Could not import sentence_transformers python package", it means Streamlit is running under a different Python than your project's venv. To verify and fix:

1. Confirm the package is installed in the venv:

```bash
./venv/bin/python3 -c "import sentence_transformers; print('OK')"
```

2. Ensure Streamlit uses the venv's Python. Preferred ways:

```bash
# Method A: use the venv streamlit executable directly
./venv/bin/streamlit run medibot.py

# Method B: activate the venv then run
source ./venv/bin/activate
streamlit run medibot.py
```

3. If Streamlit still launches with the wrong Python, check which streamlit binary is picked by your shell:

```bash
which streamlit
```

It should point to `./venv/bin/streamlit` (or the path inside your venv). If not, use the direct venv path as in Method A above.