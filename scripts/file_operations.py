import os
import os.path

# Set a dedicated folder for file I/O
working_directory = "auto_gpt_workspace"

if not os.path.exists(working_directory):
    os.makedirs(working_directory)


def safe_join(base, *paths):
    new_path = os.path.join(base, *paths)
    norm_new_path = os.path.normpath(new_path)

    if os.path.commonprefix([base, norm_new_path]) != base:
        base_auto_gpt = "/home/dev/Auto-GPT/"
        if os.path.commonprefix([base_auto_gpt, norm_new_path]) != base_auto_gpt:
            raise ValueError("Attempted to access outside of allowed directories.")

    return norm_new_path


def read_file(filename, allow_outside=False):
    try:
        if allow_outside:
            filepath = os.path.join("/home/dev/Auto-GPT/", filename)
        else:
            filepath = safe_join(working_directory, filename)

        with open(filepath, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return "Error: " + str(e)


def write_to_file(filename, text, allow_outside=False):
    try:
        if allow_outside:
            filepath = os.path.join("/home/dev/Auto-GPT/", filename)
        else:
            filepath = safe_join(working_directory, filename)

        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w") as f:
            f.write(text)
        return "File written to successfully."
    except Exception as e:
        return "Error: " + str(e)

def append_to_file(filename, text, allow_outside=False):
    try:
        if allow_outside:
            filepath = os.path.join("/home/dev/Auto-GPT/", filename)
        else:
            filepath = safe_join(working_directory, filename)

        with open(filepath, "a") as f:
            f.write(text)
        return "Text appended successfully."
    except Exception as e:
        return "Error: " + str(e)


def delete_file(filename):
    try:
        filepath = safe_join(working_directory, filename)
        os.remove(filepath)
        return "File deleted successfully."
    except Exception as e:
        return "Error: " + str(e)
