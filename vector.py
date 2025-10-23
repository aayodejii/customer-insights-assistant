import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Load the new SaaS reviews CSV
df = pd.read_csv("saas_product_reviews.csv")

# Initialize embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        # Create a descriptive title from the role and sentiment
        title = f"{row['role']} - {row['sentiment']} Review"

        # Combine title and review for better context
        document = Document(
            page_content=title + " " + row["review"],
            metadata={
                "rating": row["rating"],
                "date": row["date"],
                "reviewer": row["reviewer"],
                "role": row["role"],
                "company_size": row["company_size"],
                "sentiment": row["sentiment"],
            },
            id=str(i),
        )
        ids.append(str(i))
        documents.append(document)

# Create vector store
vector_store = Chroma(
    collection_name="saas_reviews",
    persist_directory=db_location,
    embedding_function=embeddings,
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
    print(f"✓ Added {len(documents)} reviews to vector store")

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

print(f"✓ Vector store ready with {len(df)} reviews!")
