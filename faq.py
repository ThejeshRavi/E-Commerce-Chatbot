import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

chroma_client = chromadb.Client()
groq_client = Groq(api_key =os.environ['GROQ_API_KEY'])
collection_name_faq = 'faqs'
faqs_path = "faq_data.csv"

def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into Chormadb..")

        collection = chroma_client.create_collection(
            name = collection_name_faq ,
            embedding_function = ef
        )
        df = pd.read_csv(path)
        docs = df['question'].to_list()
        metadata =[{'answer':ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
            documents =  docs,
            metadatas = metadata,
            ids = ids
        )
        print(f"FAQ Data sucessfully injested into Chroma collection:{collection_name_faq}")

    else:
        print(f"Collection: {collection_name_faq} already exists")

def get_relevant_qa(query):
     collection = chroma_client.get_collection(
            name = collection_name_faq ,
            embedding_function = ef
        )
     result = collection.query(
         query_texts = [query],
         n_results = 2
     )
     return result

def generate_answer(query,context):
    prompt = f'''Given the following context and question,generate answer based on this context only.
    if the answer is not found in the contexr,kindly state "I don't know".Don't try to  make up an answer.

    CONTEXT:{context}
    QUESTION : {query}
    '''
    completion = groq_client.chat.completions.create(
        model = os.environ['GROQ_MODEL'],
        messages=[
        {
            "role": "user",
            "content": prompt
        }
      ]
    )
    return completion.choices[0].message.content

def faq_chain(query):
    result = get_relevant_qa(query)
    
    context_parts = []
    for r_list in result['metadatas']:
        if r_list and isinstance(r_list, list) and len(r_list) > 0:
            # Assuming the first element of the inner list is the metadata dictionary
            metadata_dict = r_list[0]
            if isinstance(metadata_dict, dict) and 'answer' in metadata_dict:
                context_parts.append(metadata_dict.get('answer'))
    context = " ".join(context_parts)
    
    print("Context:",context)
    answer = generate_answer(query,context)
    return answer

if __name__ == '__main__':
    ingest_faq_data(faqs_path)
    query = "How can I track my order?"
    answer = faq_chain(query)
    print("Answer:",answer)
