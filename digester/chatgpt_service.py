import json
import logging
import re
import threading
import time
import traceback

import requests

from digester.util import get_config, Prompt, get_first_n_tokens_and_remaining, provide_text_with_css

timeout_bot_msg = "Request timeout. Network error"
LLM_MODEL = "gpt-3.5-turbo"
SYSTEM_PROMPT = "Be a assistant to digest youtube, podcast content to give summaries and insights"
TIMEOUT_MSG = f'{provide_text_with_css("ERROR", "red")} Request timeout.'

# This piece of code heavily reference
# - https://github.com/GaiZhenbiao/ChuanhuChatGPT
# - https://github.com/binary-husky/chatgpt_academic


config = get_config()


class LLMService:
    @staticmethod
    def report_exception(chatbot, history, chat_input, chat_output):
        chatbot.append((chat_input, chat_output))
        history.append(chat_input)
        history.append(chat_output)

    @staticmethod
    def get_full_error(chunk, stream_response):
        while True:
            try:
                chunk += next(stream_response)
            except:
                break
        return chunk

    @staticmethod
    def generate_payload(api_key, inputs, history, stream):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        conversation_cnt = len(history) // 2

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if conversation_cnt:
            for index in range(0, 2 * conversation_cnt, 2):
                what_i_have_asked = {}
                what_i_have_asked["role"] = "user"
                what_i_have_asked["content"] = history[index]
                what_gpt_answer = {}
                what_gpt_answer["role"] = "assistant"
                what_gpt_answer["content"] = history[index + 1]
                if what_i_have_asked["content"] != "":
                    if what_gpt_answer["content"] == "": continue
                    if what_gpt_answer["content"] == timeout_bot_msg: continue
                    messages.append(what_i_have_asked)
                    messages.append(what_gpt_answer)
                else:
                    messages[-1]['content'] = what_gpt_answer['content']

        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = inputs
        messages.append(what_i_ask_now)

        payload = {
            "model": LLM_MODEL,
            "messages": messages,
            "temperature": 1.0,
            "top_p": 1.0,
            "n": 1,
            "stream": stream,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }

        print(f"generate_payload() LLM: {LLM_MODEL}, conversation_cnt: {conversation_cnt} : {inputs}")
        print(f"\n[[[[[INPUT]]]]]\n{inputs}")
        print(f"[[[[[OUTPUT]]]]]")
        return headers, payload


class ChatGPTService:
    @staticmethod
    def get_reduce_token_percent(text):
        try:
            pattern = r"(\d+)\s+tokens\b"
            match = re.findall(pattern, text)
            EXCEED_ALLO = 500
            max_limit = float(match[0]) - EXCEED_ALLO
            current_tokens = float(match[1])
            ratio = max_limit / current_tokens
            assert ratio > 0 and ratio < 1
            return ratio, str(int(current_tokens - max_limit))
        except:
            return 0.5, 'Unknown'

    @staticmethod
    def trigger_callgpt_pipeline(prompt_obj: Prompt, prompt_show_user: str, chatbot, history, api_key, source_md):
        chatbot.append((prompt_show_user, "[INFO] waiting for ChatGPT's response."))
        status = "Success"
        yield chatbot, history, status, source_md  # show prompt_show_user (waiting for chatgpt)
        prompts = ChatGPTService.split_prompt_content(prompt_obj)
        full_gpt_response = ""
        for prompt in prompts:
            prompt_str = f"{prompt.prompt_prefix}{prompt.prompt_main}{prompt.prompt_suffix}"
            gpt_response = yield from ChatGPTService.multi_call_chatgpt_with_handling(source_md, prompt_str, prompt_show_user, chatbot, api_key, history=[])
            chatbot[-1] = (prompt_show_user, gpt_response)
            history.append(prompt_show_user)
            history.append(gpt_response)
            full_gpt_response += gpt_response
            yield chatbot, history, status, source_md  # show gpt output
        return full_gpt_response

    @staticmethod
    def split_prompt_content(prompt: Prompt) -> list:
        """
        Split the prompt.prompt_main into multiple parts, each part is less than <content_token=3500> tokens
        Then return all prompts object
        """
        prompts = []
        content_token = config.get('openai').get('content_token')
        temp_prompt_main = prompt.prompt_main
        while True:
            if len(temp_prompt_main) == 0:
                break
            elif len(temp_prompt_main) < content_token:
                prompts.append(Prompt(prompt_prefix=prompt.prompt_prefix,
                                      prompt_main=temp_prompt_main,
                                      prompt_suffix=prompt.prompt_suffix))
                break
            else:
                first, last = get_first_n_tokens_and_remaining(temp_prompt_main, content_token)
                temp_prompt_main = last
                prompts.append(Prompt(prompt_prefix=prompt.prompt_prefix,
                                      prompt_main=first,
                                      prompt_suffix=prompt.prompt_suffix))
        return prompts

    @staticmethod
    def multi_call_chatgpt_with_handling(source_md, prompt_str: str, prompt_show_user: str, chatbot, api_key, history=[]):
        """
        Handling
        - token exceeding -> split input
        - timeout -> retry 2 times
        - other error -> retry 2 times
        """

        TIMEOUT_SECONDS, MAX_RETRY = config['openai']['timeout_sec'], config['openai']['max_retry']
        # When multi-threaded, you need a mutable structure to pass information between different threads
        # list is the simplest mutable structure, we put gpt output in the first position, the second position to pass the error message
        mutable_list = [None, '']

        # multi-threading worker
        def mt(prompt_str, history):
            while True:
                try:
                    mutable_list[0] = ChatGPTService.single_call_chatgpt(api_key, prompt_str=prompt_str, history=history)
                    break
                except ConnectionAbortedError as token_exceeded_error:
                    # Try to calculate the ratio and keep as much text as possible
                    print(f'[Local Message] Token exceeded: {token_exceeded_error}.')
                    p_ratio, n_exceed = ChatGPTService.get_reduce_token_percent(str(token_exceeded_error))
                    if len(history) > 0:
                        history = [his[int(len(his) * p_ratio):] for his in history if his is not None]
                    else:
                        prompt_str = prompt_str[:int(len(prompt_str) * p_ratio)]
                    mutable_list[1] = f'Warning: text too long will be truncated. Token exceeded：{n_exceed}，Truncation ratio: {(1 - p_ratio):.0%}。'
                except TimeoutError as e:
                    mutable_list[0] = TIMEOUT_MSG
                    raise TimeoutError
                except Exception as e:
                    mutable_list[0] = f'{provide_text_with_css("ERROR", "red")} Exception: {str(e)}.'
                    raise RuntimeError(f'[ERROR] Exception: {str(e)}.')
                # TODO retry

        # Create a new thread to make http requests
        thread_name = threading.Thread(target=mt, args=(prompt_str, history))
        thread_name.start()
        # The original thread is responsible for continuously updating the UI, implementing a timeout countdown, and waiting for the new thread's task to complete
        cnt = 0
        while thread_name.is_alive():
            cnt += 1
            chatbot[-1] = (prompt_show_user, f"""
{provide_text_with_css("PROCESSING...", "blue")} {mutable_list[1]}waiting gpt response {cnt}/{TIMEOUT_SECONDS * 2 * (MAX_RETRY + 1)}{''.join(['.'] * (cnt % 4))} 
{mutable_list[0]}
            """)

            yield chatbot, history, 'Normal', source_md
            time.sleep(1)
        # Get the output of gpt out of the mutable
        gpt_response = mutable_list[0]
        if gpt_response == TIMEOUT_MSG:
            raise TimeoutError
        return gpt_response

    @staticmethod
    def single_call_chatgpt(api_key, prompt_str: str, history=[], observe_window=None):
        """
        Single call chatgpt only. No handling on multiple call (it should be in upper caller multi_call_chatgpt_with_handling())
        - Support stream=True
        - observe_window: used to pass the output across threads, most of the time just for the fancy visual effect, just leave it empty
        - retry 2 times
        """
        headers, payload = LLMService.generate_payload(api_key, prompt_str, history, stream=True)

        retry = 0
        while True:
            try:
                # make a POST request to the API endpoint, stream=False
                response = requests.post(config['openai']['api_url'], headers=headers,
                                         json=payload, stream=True, timeout=config['openai']['timeout_sec']
                                         )
                break
            except requests.exceptions.ReadTimeout as e:
                max_retry = config['openai']['max_retry']
                retry += 1
                traceback.print_exc()
                if retry > max_retry:
                    raise TimeoutError
                if max_retry != 0:
                    print(f'Request timeout. Retrying ({retry}/{max_retry}) ...')

        stream_response = response.iter_lines()
        result = ''
        while True:
            try:
                chunk = next(stream_response).decode()
            except StopIteration:
                break
            if len(chunk) == 0: continue
            if not chunk.startswith('data:'):
                error_msg = LLMService.get_full_error(chunk.encode('utf8'), stream_response).decode()
                if "reduce the length" in error_msg:
                    raise ConnectionAbortedError("OpenAI rejected the request:" + error_msg)
                else:
                    raise RuntimeError("OpenAI rejected the request: " + error_msg)
            json_data = json.loads(chunk.lstrip('data:'))['choices'][0]
            delta = json_data["delta"]
            if len(delta) == 0: break
            if "role" in delta: continue
            if "content" in delta:
                result += delta["content"]
                print(delta["content"], end='')
                if observe_window is not None: observe_window[0] += delta["content"]
            else:
                raise RuntimeError("Unexpected Json structure: " + delta)
        if json_data['finish_reason'] == 'length':
            raise ConnectionAbortedError("Completed normally with insufficient Tokens")
        return result


if __name__ == '__main__':
    import pickle

    prompt: Prompt = pickle.load(open('prompt_obj.pkl', 'rb'))
    prompts = ChatGPTService.split_prompt_content(prompt)
    for prompt in prompts:
        print("=====================================")
        print(prompt.prompt_prefix)
        print(prompt.prompt_main)
        print(prompt.prompt_suffix)
