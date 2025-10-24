from config import BEDROCK_MODEL_ID, CHROMA_PATH
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import Chroma

'''
Cria o banco vetorial Chroma
OU
Reabre o banco persistido para consultas futuras
'''


def build_vector_store(docs):
    embeddings = BedrockEmbeddings(model_id=BEDROCK_MODEL_ID)
    return Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_PATH)


def load_vector_store():
    embeddings = BedrockEmbeddings(model_id=BEDROCK_MODEL_ID)
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
