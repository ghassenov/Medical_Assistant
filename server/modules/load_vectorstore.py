import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import JinaEmbeddings
from tqdm import tqdm  # Changed import

load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medicalindex"

os.environ['JINA_API_KEY'] = JINA_API_KEY
UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# initialize pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)

# fetch existing indexes
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,  # JINA embeddings dimension is 768
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

def load_vector_database(uploaded_files):
    # Initialize JINA embeddings
    embed_model = JinaEmbeddings(
        jina_api_key=JINA_API_KEY,
        model_name="jina-embeddings-v2-base-en"  # You can change this to other JINA models
    )
    
    file_paths = []
    
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))
        
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"🔍 Embedding {len(texts)} chunks with JINA...")
        embeddings = embed_model.embed_documents(texts)

        print("Uploading to Pinecone...")
        # Fixed: using tqdm directly as function
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            # Prepare vectors for upsert
            vectors = []
            for i, (id, embedding, metadata) in enumerate(zip(ids, embeddings, metadatas)):
                vectors.append({
                    "id": id,
                    "values": embedding,
                    "metadata": metadata
                })
            
            # Upsert in batches (Pinecone recommends batch sizes of 100 or less)
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                index.upsert(vectors=batch)
                progress.update(len(batch))

        print(f"Upload complete for {file_path}")