import os
import streamlit as st

# Note: langchain-related imports are done lazily inside functions to
# avoid import-time ModuleNotFoundError when running outside the project venv.


## Uncomment the following files if you're not using pipenv as your virtual environment manager
from dotenv import load_dotenv
load_dotenv()


DB_FAISS_PATH="vectorstore/db_faiss"
@st.cache_resource
def get_vectorstore():
    # Import embeddings lazily so the module can be imported even if the
    # environment doesn't have langchain_huggingface installed system-wide.
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except Exception:
        try:
            from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
        except Exception:
            st.error(
                "HuggingFaceEmbeddings is not available. Make sure you run Streamlit with the project's venv where langchain_huggingface or langchain_community is installed."
            )
            return None

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    try:
        from langchain_community.vectorstores import FAISS
    except Exception:
        st.error("langchain_community is not available. Install the project's venv or add langchain_community to your environment.")
        return None

    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db


def set_custom_prompt(custom_prompt_template):
    try:
        from langchain_core.prompts import PromptTemplate
    except Exception:
        st.error("PromptTemplate not available. Ensure langchain_core is installed in the venv.")
        return None
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt


def main():
    st.title("Ask Chatbot!")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt=st.chat_input("Pass your prompt here")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role':'user', 'content': prompt})
                
        try: 
            vectorstore=get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load the vector store")

            GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
            if not GROQ_API_KEY:
                st.warning("GROQ_API_KEY is not set. The Groq LLM may not work. Set GROQ_API_KEY in your environment or use a different LLM.")
            GROQ_MODEL_NAME = "llama-3.1-8b-instant"  # Change to any supported Groq model
            # Lazily import LLM and chain helpers so app can start without system-wide
            # langchain packages installed.
            try:
                from langchain_groq import ChatGroq
                from langchain_core.prompts import ChatPromptTemplate
                from langchain_classic.chains import create_retrieval_chain
                from langchain_classic.chains.combine_documents import create_stuff_documents_chain
            except Exception as e:
                st.error(f"Required langchain packages are not available: {e}")
                return

            llm = ChatGroq(
                model=GROQ_MODEL_NAME,
                temperature=0.5,
                max_tokens=512,
                api_key=GROQ_API_KEY,
            )

            # Build an inline chat prompt that accepts the formatted documents as {context}
            chat_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a helpful medical assistant. Use the provided context: {context} to answer the question."),
                    ("human", "{input}"),
                ]
            )

            # Document combiner chain (stuff documents into prompt)
            combine_docs_chain = create_stuff_documents_chain(llm, chat_prompt)

            # Retrieval chain (retriever + doc combiner)
            rag_chain = create_retrieval_chain(vectorstore.as_retriever(search_kwargs={"k": 3}), combine_docs_chain)

            response=rag_chain.invoke({'input': prompt})

            result=response["answer"]
            st.chat_message('assistant').markdown(result)
            st.session_state.messages.append({'role':'assistant', 'content': result})

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()