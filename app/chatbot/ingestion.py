import os

import boto3
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_BUCKET,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    DATASET_PATH,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

'''
Buscar os documentos no S3
Carregar os documentos localmente
Fragmentar em chunks prontos para indexação
'''


def download_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=AWS_REGION,
    )
    os.makedirs(DATASET_PATH, exist_ok=True)

    # Baixa todos os arquivos do diretório 'juridicos/'
    response = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=DATASET_PATH)

    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.endswith(".pdf"):
            local_path = os.path.join(DATASET_PATH, os.path.basename(key))
            s3.download_file(AWS_BUCKET, key, local_path)
            print(f"Baixado: {key} -> {local_path}")


def load_and_split():
    # ? loader recursivo para todos os arquivos e diretórios dentro de um diretório
    loader = DirectoryLoader(
        DATASET_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        recursive=True
    )

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)
