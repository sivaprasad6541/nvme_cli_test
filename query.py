# query.py
import requests
import chromadb
from config import GROQ_API_KEY, GROQ_MODEL

client = chromadb.Client()
collection = client.get_or_create_collection("nvme_cli_code")

def search_chunks(query, k=5):
    results = collection.query(query_texts=[query], n_results=k)
    return results['documents'][0]

def ask_groq(system_prompt, user_prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("\n⚠️ Error response from Groq API:")
        print(response.text)
        raise e


def run_query(query):
    context = search_chunks(query, k=5)
    user_prompt = f"Code Context:\n{'\n---\n'.join(context)}\n\nNow, {query}"
    system_prompt = "You are a Linux C code analysis expert."
    return ask_groq(system_prompt, user_prompt)

if __name__ == "__main__":
    question = input("Ask your query: ")
    answer = run_query(question)
    print("\nAnswer:\n", answer)
