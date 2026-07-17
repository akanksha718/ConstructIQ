import os

from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)


vector_store = PGVector(

    embeddings=embeddings,

    collection_name="constructiq_documents",

    connection=os.getenv("DATABASE_URL"),

    use_jsonb=True,

)