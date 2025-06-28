from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---- PDF Folder -------
DATA_PATH = 'data/'

# Load PDF from local
def load_pdf_files(data):
    loder = DirectoryLoader(
        data,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )
    loder = loder.load()
    return loder

documents = load_pdf_files(data=DATA_PATH)
print(len(documents))


# Step 2 Chunking PDF
def create_text_splitter(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    text_splitter = text_splitter.split_documents(documents=documents)
    return text_splitter

splitter_text = create_text_splitter(documents=documents)
print(len(splitter_text))

# Step 3 Create Vector Embedding


