from pydantic import BaseModel, validator

class ChatbotModel(BaseModel):
    """
    Model to chat with the chatbot
    """
    query: str
