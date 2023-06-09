import os
from pathlib import Path

import tiktoken
import yaml

tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


class Prompt:
    """
    Define the prompt structure
    Prompt = "{prompt_prefix}{prompt_main}{prompt_suffix}"
    where if the prompt is too long, {prompt_main} will be splitted into multiple parts to fulfill context length of LLM

    Example: for Youtube-timestamped summary
        prompt_prefix: Youtube Video types definitions, Title
        prompt_main: transcript (splittable)
        prompt_suffix: task description / constraints
    """

    def __init__(self, prompt_prefix, prompt_main, prompt_suffix):
        self.prompt_prefix = prompt_prefix
        self.prompt_main = prompt_main
        self.prompt_suffix = prompt_suffix


def get_project_root():
    return Path(__file__).parent.parent


def get_config():
    with open(os.path.join(get_project_root(), 'config/config.yaml'), encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    try:
        with open(os.path.join(get_project_root(), 'config/config_secret.yaml'), encoding='utf-8') as f:
            config_secret = yaml.load(f, Loader=yaml.FullLoader)
            config.update(config_secret)
    except FileNotFoundError:
        pass  # okay to not have config_secret.yaml
    return config


def get_token(text: str):
    return len(tokenizer.encode(text, disallowed_special=()))


def get_first_n_tokens_and_remaining(text: str, n: int):
    tokens = tokenizer.encode(text, disallowed_special=())
    return tokenizer.decode(tokens[:n]), tokenizer.decode(tokens[n:])


def provide_text_with_css(text, color):
    if color == "red":
        return f'<span style="background-color: red; color: white; padding: 3px; border-radius: 8px;">{text}</span>'
    elif color == "green":
        return f'<span style="background-color: green; color: white; padding: 3px; border-radius: 8px;">{text}</span>'
    elif color == "blue":
        return f'<span style="background-color: blue; color: white; padding: 3px; border-radius: 8px;">{text}</span>'
    elif color == "yellow":
        return f'<span style="background-color: yellow; color: black; padding: 3px; border-radius: 8px;">{text}</span>'
    else:
        return text


if __name__ == '__main__':
    # print(get_token("def get_token(text: str)"))
    # print(get_token("皆さんこんにちは"))
    print(get_first_n_tokens_and_remaining("This is a string with some text to tokenize.", 30))
