import os
from pathlib import Path
from config import Config
SRC_DIR = Path(__file__).parent

def load_prompt():
    try:
        # get directory of this file:
        file_dir = Path(os.path.dirname(os.path.realpath(__file__)))
        data_dir = file_dir / "data"
        prompt_file = data_dir / "prompt.txt"
        cfg = Config()
        if cfg.no_search == True:
            prompt_file = data_dir / "prompt_no_search.txt"
        # Load the promt from data/prompt.txt
        if cfg.no_search == True:
            with open(SRC_DIR/ "data/prompt_no_search.txt", "r") as prompt_file:
                prompt = prompt_file.read()
        else:
            with open(SRC_DIR/ "data/prompt.txt", "r") as prompt_file:
                prompt = prompt_file.read()

        return prompt
    except FileNotFoundError:
        print("Error: Prompt file not found", flush=True)
        return ""
