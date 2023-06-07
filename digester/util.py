import os
from pathlib import Path

import tiktoken
import yaml


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
    return config


def get_token(text: str):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(tokenizer.encode(text, disallowed_special=()))


if __name__ == '__main__':
    print(get_token("def get_token(text: str)"))
    print(get_token("皆さんこんにちは"))
