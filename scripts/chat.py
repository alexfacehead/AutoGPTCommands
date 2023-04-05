import time
import openai
from dotenv import load_dotenv
from config import Config
import token_counter

cfg = Config()

from llm_utils import create_chat_completion


def create_chat_message(role, content):
    """
    Create a chat message with the given role and content.

    Args:
    role (str): The role of the message sender, e.g., "system", "user", or "assistant".
    content (str): The content of the message.

    Returns:
    dict: A dictionary containing the role and content of the message.
    """
    return {"role": role, "content": content}



# TODO: Change debug from hardcode to argument
def chat_with_ai(
        prompt,
        user_input,
        full_message_history,
        permanent_memory,
        token_limit,
        debug=False):
    while True:
        try:
            """
            Interact with the OpenAI API, sending the prompt, user input, message history, and permanent memory.

            Args:
            prompt (str): The prompt explaining the rules to the AI.
            user_input (str): The input from the user.
            full_message_history (list): The list of all messages sent between the user and the AI.
            permanent_memory (list): The list of items in the AI's permanent memory.
            token_limit (int): The maximum number of tokens allowed in the API call.

            Returns:
            str: The AI's response.
            """
            model = cfg.fast_llm_model # TODO: Change model from hardcode to argument
            # Reserve 1000 tokens for the response
            if debug:
                print(f"Token limit: {token_limit}")
            send_token_limit = token_limit - 1000

            current_context = [
                create_chat_message(
                    "system", prompt), create_chat_message(
                    "system", f"Permanent memory: {permanent_memory}")]                

            # Add messages from the full message history until we reach the token limit
            next_message_to_add_index = len(full_message_history) - 1
            current_tokens_used = 0
            insertion_index = len(current_context)

            # Count the currently used tokens
            current_tokens_used = token_counter.count_message_tokens(current_context, model)
            current_tokens_used += token_counter.count_message_tokens([create_chat_message("user", user_input)], model) # Account for user input (appended later)

            while next_message_to_add_index >= 0:
                # print (f"CURRENT TOKENS USED: {current_tokens_used}")
                message_to_add = full_message_history[next_message_to_add_index]

                tokens_to_add = token_counter.count_message_tokens([message_to_add], model)
                if current_tokens_used + tokens_to_add > send_token_limit:
                    break

                # Add the most recent message to the start of the current context, after the two system prompts.
                current_context.insert(insertion_index, full_message_history[next_message_to_add_index])

                # Count the currently used tokens
                current_tokens_used += tokens_to_add
                
                # Move to the next most recent message in the full message history
                next_message_to_add_index -= 1

            # Append user input, the length of this is accounted for above
            current_context.extend([create_chat_message("user", user_input)])

            # Calculate remaining tokens
            tokens_remaining = token_limit - current_tokens_used
            # assert tokens_remaining >= 0, "Tokens remaining is negative. This should never happen, please submit a bug report at https://www.github.com/Torantulino/Auto-GPT"

            # Debug print the current context
            if debug:
                print(f"Token limit: {token_limit}")
                print(f"Send Token Count: {current_tokens_used}")
                print(f"Tokens remaining for response: {tokens_remaining}")
                print("------------ CONTEXT SENT TO AI ---------------")
                for message in current_context:
                    # Skip printing the prompt
                    if message["role"] == "system" and message["content"] == prompt:
                        continue
                    print(
                        f"{message['role'].capitalize()}: {message['content']}")
                    print()
                print("----------- END OF CONTEXT ----------------")

            # TODO: use a model defined elsewhere, so that model can contain temperature and other settings we care about
            assistant_reply = create_chat_completion(
                model=model,
                messages=current_context,
                max_tokens=tokens_remaining,
            )

            # Update full message history
            full_message_history.append(
                create_chat_message(
                    "user", user_input))
            full_message_history.append(
                create_chat_message(
                    "assistant", assistant_reply))

            return assistant_reply
        except openai.error.RateLimitError:
            # TODO: WHen we switch to langchain, this is built in
            print("Error: ", "API Rate Limit Reached. Waiting 10 seconds...")
            time.sleep(10)
