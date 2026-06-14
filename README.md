🩺 AI Medical Chatbot using RAG (Retrieval-Augmented Generation)
## Problem Statement

Traditional healthcare information systems and standalone Large Language Models often generate generic or inaccurate responses due to the lack of access to domain-specific knowledge. Users are required to manually search through lengthy medical documents, which is time-consuming and inefficient. In addition, conventional LLMs may produce hallucinated responses that reduce reliability. Therefore, there is a need for an intelligent system that can retrieve relevant information from medical documents and generate accurate, context-aware responses. The proposed AI Medical Chatbot using Retrieval-Augmented Generation (RAG) addresses these limitations by combining semantic search with Large Language Models to improve answer accuracy and reduce hallucinations.


## Workflow of Proposed System

START
   ↓
Load Medical PDF Documents
   ↓
Extract Text
   ↓
Split Text into Chunks
   ↓
Generate Embeddings (Hugging Face)
   ↓
Store Embeddings in FAISS
   ↓
User Enters Query
   ↓
Convert Query into Embedding
   ↓
Semantic Similarity Search
   ↓
Retrieve Relevant Chunks
   ↓
Create Prompt using LangChain
   ↓
Send Prompt to Llama-3.1-8B via Groq API
   ↓
Generate Response
   ↓
Display Answer using Streamlit
   ↓
END

📌 Features
💬 Natural language interaction
📄 PDF-based medical knowledge base
🔍 Semantic search using embeddings
🧠 RAG architecture for accurate responses
🤖 LLM-powered answer generation
🎤 Voice input support (Speech-to-Text)
🔊 Text-to-Speech response generation
🖼️ Medical image analysis support
🌐 Interactive web interface using Gradio
⚡ Fast and efficient retrieval using Vector Database


## Folder Structure
AI-Medical-Chatbot
├── gradio_app.py
├── brain_of_the_doctor.py
├── voice_of_the_patient.py
├── requirements.txt
└── README.md
