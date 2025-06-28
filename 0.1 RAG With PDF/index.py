from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 1 Load raw pdf

DATA_PATH = 'data/'

# Load PDF
def load_pdf_files(data):
    loder = DirectoryLoader(
        data,
        glob='*.pdf',
        loader_cls= PyPDFLoader
    )
    documents = loder.load()
    return documents

documents = load_pdf_files(data= DATA_PATH)

print(len(documents))

# Step 2 Chunking

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    text_chucks = text_splitter.split_documents(documents)
    return text_chucks

text_chunks = create_chunks(documents)

print(text_chunks)
