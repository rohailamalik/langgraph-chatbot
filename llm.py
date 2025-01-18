from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
import httpx
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API Key is not set. Please add it to the .env file.")

# Update the URL based on the request
def update_base_url(request: httpx.Request) -> None:
    if request.url.path == "/chat/completions":
        request.url = request.url.copy_with(path="/v1/chat")
    elif request.url.path == "/embeddings":
        request.url = request.url.copy_with(path="/v1/openai/ada-002/embeddings")

# Initialize HTTP client with event hook to update the base URL
http_client = httpx.Client(
    event_hooks={"request": [update_base_url]}
)

# Initialize the LLM
llm = ChatOpenAI(
    base_url="https://aalto-openai-apigw.azure-api.net",
    api_key=openai_api_key,
    default_headers={
        "Ocp-Apim-Subscription-Key": openai_api_key,
    },
    http_client=http_client
)

# Create the Embedding model
embeddings = OpenAIEmbeddings(
    base_url="https://aalto-openai-apigw.azure-api.net",
    api_key=openai_api_key,
    default_headers={
        "Ocp-Apim-Subscription-Key": openai_api_key,
    },
    http_client=http_client
)