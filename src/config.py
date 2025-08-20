import os

# Input and Output folder
PROJECT_PATH = os.environ.get("PROJECT_PATH") or "/home/maxib/ws/simple_rag_system" 

RAW_DIR = f"{PROJECT_PATH}/documents_db/raw"
INGESTED_DIR = f"{PROJECT_PATH}/documents_db/ingested"
CHUNKED_DIR = f"{PROJECT_PATH}/documents_db/chunked "