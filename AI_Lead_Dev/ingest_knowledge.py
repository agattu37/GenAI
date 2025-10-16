from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

def ingest_knowledge():
    """
    Loads knowledge from a text file, splits it, embeds it,
    and stores it in a local ChromaDB vector store.
    """

    print("Starting knowledge ingestion...")

    loader = TextLoader("knowledge_base.txt")

    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")


    text_splitter = CharacterTextSplitter(
        separator="===",
        chunk_size=500,
        chunk_overlap=0,
        keep_separator=False
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="mxbai-embed-large:latest"),
        persist_directory="./chroma_db"
    )

    print("Knowledge ingestion completed.")


if __name__ == "__main__":
    ingest_knowledge()
