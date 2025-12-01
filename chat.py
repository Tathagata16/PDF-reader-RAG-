from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from openai import OpenAI

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

#retrive the vector embeddings form the existing vector database
vector_db = QdrantVectorStore.from_existing_collection(
    embedding = embedding_model,
    url = "http://localhost:6333",
    collection_name = "learning"
)

#taking user input
user_query = input(">>")

#time to do the similarity search -> returns the relevant chunks from vector db
searched_results = vector_db.similarity_search(query = user_query)

#creating a context for the llm
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
    you are a helpful ai assistant who answers user query based on the available context retrived from a pdf file along with page_contents and page number

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.

    Context: {context}

"""


openai_client.chat.completions.create(
    model = "gpt-5",
    messages = [
        {
            "role": "system", "content":SYSTEM_PROMPT
        },
        {
            "role": "user", "content":user_query
        }
    ]
)

print(f"💀: {response.choices[0].message.content}")