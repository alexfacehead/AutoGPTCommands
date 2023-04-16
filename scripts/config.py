import os
import openai
from dotenv import load_dotenv
# Load environment variables from .env file
env_file = "" # EXACT file path of your .env file goes here. EXAMPLE: /home/dev/Auto-GPT/scripts/.env
# If the user doesn't provide the exact path, use the default .env location
if not env_file:
    current_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_path, "..")
    env_file = os.path.join(project_root, ".env")

load_dotenv(env_file)

class Singleton(type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """

    def __init__(self):
        #self.no_search = os.getenv("NO_SEARCH")
        self.searx_url = os.getenv("SEARX_URL")
        self.searx_username = os.getenv("SEARX_USERNAME")
        self.searx_password = os.getenv("SEARX_PASSWORD")
        self.continuous_mode = False
        self.speak_mode = False
        # TODO - make these models be self-contained, using langchain, so we can configure them once and call it good 
        self.fast_llm_model = os.getenv("FAST_LLM_MODEL", "gpt-3.5-turbo") 
        self.smart_llm_model = os.getenv("SMART_LLM_MODEL", "gpt-4")
        self.fast_token_limit = int(os.getenv("FAST_TOKEN_LIMIT", 4000))
        self.smart_token_limit = int(os.getenv("SMART_TOKEN_LIMIT", 2000))
        
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

        # Initialize the OpenAI API client
        openai.api_key = self.openai_api_key

    def set_continuous_mode(self, value: bool):
        self.continuous_mode = value

    def set_speak_mode(self, value: bool):
        self.speak_mode = value

    def set_fast_llm_model(self, value: str):
        self.fast_llm_model = value

    def set_searx_url(self, value: str):
        self.searx_url = value

    def set_searx_username(self, value: str):
        self.searx_username = value

    def set_searx_password(self, value: str):
        self.searx_password = value

    def set_smart_llm_model(self, value: str):
        self.smart_llm_model = value

    def set_fast_token_limit(self, value: int):
        self.fast_token_limit = value

    def set_smart_token_limit(self, value: int):
        self.smart_token_limit = value

    def set_openai_api_key(self, value: str):
        self.openai_api_key = value
    
    def set_elevenlabs_api_key(self, value: str):
        self.elevenlabs_api_key = value
        
    def set_google_api_key(self, value: str):
        self.google_api_key = value
    
    def set_custom_search_engine_id(self, value: str):
        self.custom_search_engine_id = value

    def update_env(self, key: str, value: str, env_file: str):
        with open(env_file, 'r') as file:
            lines = file.readlines()

        with open(env_file, 'w') as file:
            for line in lines:
                if line.startswith(key):
                    line = f"{key}={value}\n"
                file.write(line)

    def set_no_search(self, value: bool):
        self.no_search = value
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_file = os.path.join(base_dir, ".env")
        self.update_env('NO_SEARCH', str(value), env_file)