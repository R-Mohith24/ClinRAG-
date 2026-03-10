"""
Chat Engine Module (CRC — Conversational Retrieval Chain)
Wraps the QueryEngine in a CondenseQuestionChatEngine with a memory buffer.
This gives the chatbot the ability to remember previous turns of the conversation.
"""

from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.memory import ChatMemoryBuffer


def build_chat_engine(query_engine) -> CondenseQuestionChatEngine:
    """Build and return a CondenseQuestionChatEngine.

    How it works (simple explanation):
    - The user asks a follow-up question like "What about its side effects?"
    - This engine looks at the full chat history + the new question together.
    - It rewrites the question into a standalone one: "What are the side effects of Type 2 Diabetes?"
    - That rewritten question is sent to the QueryEngine (which searches FAISS + BioMistral).
    - The final answer is generated and returned.

    Args:
        query_engine: A configured QueryEngine from src.rag.query_engine.build_query_engine.

    Returns:
        A CondenseQuestionChatEngine ready for multi-turn medical conversations.
    """
    memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        memory=memory,
        # The global Settings.llm (BioMistral) is used automatically here
        verbose=True,  # Show the condensed query in the console so you can see what's happening
    )
    return chat_engine
