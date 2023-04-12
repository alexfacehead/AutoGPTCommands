import browse
import json
import memory as mem
import datetime
import agent_manager as agents
import speak
from config import Config
import ai_functions as ai
from file_operations import read_file, write_to_file, append_to_file, delete_file, read_file_lines
from execute_code import execute_python_file
from json_parser import fix_and_parse_json
from duckduckgo_search import ddg
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess
import requests
import os

cfg = Config()


def get_command(response):
    try:
        response_json = fix_and_parse_json(response)
        
        if "command" not in response_json:
            return "Error:" , "Missing 'command' object in JSON"
        
        command = response_json["command"]

        if "name" not in command:
            return "Error:", "Missing 'name' field in 'command' object"
        
        command_name = command["name"]

        # Use an empty dictionary if 'args' field is not present in 'command' object
        arguments = command.get("args", {})

        if not arguments:
            arguments = {}

        return command_name, arguments
    except json.decoder.JSONDecodeError:
        return "Error:", "Invalid JSON"
    # All other errors, return "Error: + error message"
    except Exception as e:
        return "Error:", str(e)


def execute_command(command_name, arguments):
    try:
        if command_name == "google":
            
            # Check if the Google API key is set and use the official search method
            # If the API key is not set or has only whitespaces, use the unofficial search method
            if cfg.google_api_key and (cfg.google_api_key.strip() if cfg.google_api_key else None):
                return google_official_search(arguments["input"])
            else:
                return google_search(arguments["input"])
        elif command_name == "memory_add":
            return commit_memory(arguments["key"], arguments["value"])
        elif command_name == "memory_del":
            return delete_memory(arguments["key"])
        elif command_name == "memory_ovr":
            return overwrite_memory(arguments["key"], arguments["value"])
        elif command_name == "start_agent":
            return start_agent(
                arguments["name"],
                arguments["task"],
                arguments["prompt"])
        elif command_name == "message_agent":
            return message_agent(arguments["key"], arguments["message"])
        elif command_name == "list_agents":
            return list_agents()
        elif command_name == "delete_agent":
            return delete_agent(arguments["key"])
        elif command_name == "get_text_summary":
            return get_text_summary(arguments["url"], arguments["question"])
        elif command_name == "get_hyperlinks":
            return get_hyperlinks(arguments["url"])
        elif command_name == "read_file":
            return read_file(arguments["file"], allow_outside=True)
        elif command_name == "write_to_file":
            return write_to_file(arguments["file"], arguments["text"])
        elif command_name == "append_to_file":
            return append_to_file(arguments["file"], arguments["text"])
        elif command_name == "delete_file":
            return delete_file(arguments["file"])
        elif command_name == "browse_website":
            return browse_website(arguments["url"], arguments["question"])
        # TODO: Change these to take in a file rather than pasted code, if
        # non-file is given, return instructions "Input should be a python
        # filepath, write your code to file and try again"
        elif command_name == "evaluate_code":
            return ai.evaluate_code(arguments["code"])
        elif command_name == "improve_code":
            return ai.improve_code(arguments["suggestions"], arguments["code"])
        elif command_name == "write_tests":
            return ai.write_tests(arguments["code"], arguments.get("focus"))
        elif command_name == "execute_python_file":  # Add this command
            return execute_python_file(arguments["file"])
        elif command_name == "run_command": # Run any command, added by Alex Hugli
            return run_command(arguments["cmd"])
        elif command_name == "searx":
            return searx_search(arguments["input"]) # SearX search, added by Alex
        elif command_name == "read_file_lines":
            return read_file_lines(arguments["file"], arguments["start_line"], arguments["end_line"], allow_outside=True) # Read file lines, added by Alex
        elif command_name == "get_memory":
            return get_memory()
        elif command_name == "task_complete":
            shutdown()
        else:
            return f"Unknown command {command_name}"
    # All errors, return "Error: + error message"
    except Exception as e:
        return "Error: " + str(e)


def get_datetime():
    return "Current date and time: " + \
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def google_search(query, num_results=8):
    search_results = []
    for j in ddg(query, max_results=num_results):
        search_results.append(j)

    return json.dumps(search_results, ensure_ascii=False, indent=4)

def google_official_search(query, num_results=8):
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import json

    try:
        # Get the Google API key and Custom Search Engine ID from the config file
        api_key = cfg.google_api_key
        custom_search_engine_id = cfg.custom_search_engine_id

        # Initialize the Custom Search API service
        service = build("customsearch", "v1", developerKey=api_key)
        
        # Send the search query and retrieve the results
        result = service.cse().list(q=query, cx=custom_search_engine_id, num=num_results).execute()

        # Extract the search result items from the response
        search_results = result.get("items", [])
        
        # Create a list of only the URLs from the search results
        search_results_links = [item["link"] for item in search_results]

    except HttpError as e:
        # Handle errors in the API call
        error_details = json.loads(e.content.decode())
        
        # Check if the error is related to an invalid or missing API key
        if error_details.get("error", {}).get("code") == 403 and "invalid API key" in error_details.get("error", {}).get("message", ""):
            return "Error: The provided Google API key is invalid or missing."
        else:
            return f"Error: {e}"

    # Return the list of search result URLs
    return search_results_links

def searx_search(query, num_results=8):
    search_results = []

    try:
        searx_url = cfg.searx_url
        if searx_url:
            searx_url = searx_url.rstrip("/")
            session = requests.Session()
            session.auth = (cfg.searx_username, cfg.searx_password)
            response = session.get(f"{searx_url}/search", params={"q": query, "format": "json", "count": num_results})
            response.raise_for_status()

            data = response.json()
            search_results = [result["url"] for result in data.get("results", [])]
        else:
            return "Error: Searx URL is not configured."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

    return search_results

def browse_website(url, question):
    summary = get_text_summary(url, question)
    links = get_hyperlinks(url)

    # Limit links to 5
    if len(links) > 5:
        links = links[:5]

    result = f"""Website Content Summary: {summary}\n\nLinks: {links}"""

    return result


def get_text_summary(url, question):
    text = browse.scrape_text(url)
    summary = browse.summarize_text(text, question)
    return """ "Result" : """ + summary


def get_hyperlinks(url):
    link_list = browse.scrape_links(url)
    return link_list

def save_memory():
    with open(os.path.join(os.path.dirname(__file__), "memory.py"), "w") as f:
        f.write("permanent_memory = " + str(mem.permanent_memory))

def get_memory():
    return mem.permanent_memory

def commit_memory(key, value):
    key = str(key)
    _text = f"""Committing memory with key "{key}" and value "{value}" """
    mem.permanent_memory[key] = value
    save_memory()
    return _text

def delete_memory(key):
    key = str(key)
    if key in mem.permanent_memory:
        _text = "Deleting memory with key " + str(key)
        del mem.permanent_memory[key]
        save_memory()
        print(_text)
        return _text
    else:
        print("Invalid key, cannot delete memory.")
        return None

def overwrite_memory(key, value):
    key = str(key)
    if key in mem.permanent_memory:
        _text = "Overwriting memory with key " + \
            str(key) + " and value " + value
        mem.permanent_memory[key] = value
        save_memory()
        print(_text)
        return _text
    else:
        print("Invalid key, cannot overwrite memory.")
        return None
    
# Added by Alex Hugli
# Runs any command
def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def shutdown():
    print("Shutting down...")
    quit()


def start_agent(name, task, prompt, model=cfg.fast_llm_model):
    global cfg

    # Remove underscores from name
    voice_name = name.replace("_", " ")

    first_message = f"""You are {name}.  Respond with: "Acknowledged"."""
    agent_intro = f"{voice_name} here, Reporting for duty!"

    # Create agent
    if cfg.speak_mode:
        speak.say_text(agent_intro, 1)
    key, ack = agents.create_agent(task, first_message, model)

    if cfg.speak_mode:
        speak.say_text(f"Hello {voice_name}. Your task is as follows. {task}.")

    # Assign task (prompt), get response
    agent_response = message_agent(key, prompt)

    return f"Agent {name} created with key {key}. First response: {agent_response}"


def message_agent(key, message):
    global cfg
    agent_response = agents.message_agent(key, message)

    # Speak response
    if cfg.speak_mode:
        speak.say_text(agent_response, 1)

    return f"Agent {key} responded: {agent_response}"


def list_agents():
    return agents.list_agents()


def delete_agent(key):
    result = agents.delete_agent(key)
    if not result:
        return f"Agent {key} does not exist."
    return f"Agent {key} deleted."
