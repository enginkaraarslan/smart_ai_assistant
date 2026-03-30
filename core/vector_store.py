from langchain_community.vectorstores import FAISS
from core.embeddings import get_embeddings

def create_vector_store(text):
    embeddings = get_embeddings()

   
    texts = [text]

    return FAISS.from_texts(texts, embeddings)


def retrieve_docs(vector_store, query):
    return vector_store.similarity_search(query, k=3)