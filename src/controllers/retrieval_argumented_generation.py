import os
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.environ['OPENAI_API_KEY']

class RetrievalArgumentedGeneration:

    def __init__(self):
        self.llm_name = "gpt-3.5-turbo"
        self.file = "src/rag/docs/returns_policies/return_policies.pdf"
        self.chain_type = "stuff"
        self.k = 4
        self.qa = self.load_db(self.file, self.chain_type, self.k)

    def load_db(self, file, chain_type, k):
        # load documents
        loader = PyPDFLoader(file)
        documents = loader.load()
        # split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(documents)
        # define embedding
        embeddings = OpenAIEmbeddings()
        # create vector database from data
        db = DocArrayInMemorySearch.from_documents(docs, embeddings)
        # define retriever
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
        # create a chatbot chain.
        qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=self.llm_name, temperature=0),
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=True,
            return_generated_question=True,
        )
        return qa

    def query(self, query, chat_history, debug=True):
        response = self.qa({"question": query, "chat_history": chat_history})
        if debug:
            print(f'answer RAG: {response["answer"]}')
        chat_history.extend([(query, response["answer"])])
        return response['answer'], chat_history


if __name__ == "__main__":

    RAG = RetrievalArgumentedGeneration()
    query = "What is Electronic bot return policies period"
    query = "how could I contact to Electronic bot for return policies"
    query = "What happen with defective items after 30 Days"
    answer = RAG.query_rag(query, [])
    print(answer)

