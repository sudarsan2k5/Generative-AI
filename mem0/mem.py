from email import message
from operator import truediv
from turtle import mode
from mem0 import Memory
from openai import OpenAI

OPENAI_API_KEY = ""

QUADRANT_HOST = "localhost"

NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "reform-william-center-vibrate-press-5829"

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"}},
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QUADRANT_HOST,
            "port": 6333,
        },
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {"url": NEO4J_URL, "username": NEO4J_USERNAME, "password": NEO4J_PASSWORD},
    },
}

mem_client = Memory.from_config(config)
print(mem_client)

openai_client = OpenAI(api_key = OPENAI_API_KEY)

def chat(message):
    mem_result = mem_client.search(query=message, user_id="s123")

    # print(f"\n\n MEMORY: \n\n{mem_result}\n\n")

    # memories = ""
    # for memory in mem_result:
    #     memories += f"{str(memory.get("memory"))}: {str(memory.get("score"))}"
    memories = "\n".join([m["memory"] for m in mem_result.get('results', [])])

    SYSTEM_PROMPT = f"""
        You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory and Score:
        {memories}
    """
    
    print(f"\n\n MEMORY: \n\n{memories}\n\n")

    message = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
    ]

    result = openai_client.chat.completions.create(
        model = "gpt-4.1",
        messages=message
    )


    message.append(
        {"role": "assistant", "content": result.choices[0].message.content}
    )

    mem_client.add(message, user_id="s123")
    return result.choices[0].message.content


while True:
    message = input(">> ")
    print("Bot: ", chat(message=message))