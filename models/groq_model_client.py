from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
from config.constants import MODEL_GROQ
from dotenv import load_dotenv
import os

def get_model_client():
    load_dotenv()  # Load environment variables from .env file
    groq_model_client=OpenAIChatCompletionClient(
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
    include_name_in_message=True, # Essential for multi-agent coordination
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "family": ModelFamily.UNKNOWN,
        },
    )
    return groq_model_client