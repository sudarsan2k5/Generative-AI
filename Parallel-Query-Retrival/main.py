from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()

file_path = './layout-parser-paper.pdf'
print(file_path)

loder = PyPDFLoader(file_path)
docs = loder.load()

print(len(docs))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

text = text_splitter.split_documents(docs)
print(len(text))
print(type(text))

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# Initialize the vector store with your split documents
VectorStore = QdrantVectorStore.from_documents(
    documents=text,
    url="http://localhost:6333/",
    collection_name="chat-with-pdf",
    embedding=embeddings,
)

print("Injection Done")

retrival = QdrantVectorStore.form_existing_collection(
    url="http://localhost:6333/",
    collection_name="chat-with-pdf",
    embedding=embeddings,
)

search_result = retrival.similarsimilarity_search(
    query = "what this PDF about ?"
)