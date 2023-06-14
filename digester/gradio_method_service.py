import json

from everything2text4prompt.everything2text4prompt import Everything2Text4Prompt
from everything2text4prompt.util import BaseData, YoutubeData, PodcastData

from digester.chatgpt_service import LLMService, ChatGPTService
from digester.util import Prompt, provide_text_with_css, GradioInputs

WAITING_FOR_TARGET_INPUT = "Waiting for target source input"
RESPONSE_SUFFIX = "⚡by DigestEverythingGPT"


class GradioMethodService:
    """
    GradioMethodService is defined as gradio functions
    Therefore all methods here will fulfill
    - gradio.inputs as signature
    - gradio.outputs as return
    Detailed-level methods called by methods in GradioMethodService will be in other classes (e.g. DigesterService)
    """

    @staticmethod
    def write_results_to_file(history, file_name=None):
        """
        Writes the conversation history to a file in Markdown format.
        If no filename is specified, the filename is generated using the current time.
        """
        import os, time
        if file_name is None:
            file_name = 'chatGPT_report' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.md'
        os.makedirs('./analyzer_logs/', exist_ok=True)
        with open(f'./analyzer_logs/{file_name}', 'w', encoding='utf8') as f:
            f.write('# chatGPT report\n')
            for i, content in enumerate(history):
                try:
                    if type(content) != str: content = str(content)
                except:
                    continue
                if i % 2 == 0:
                    f.write('## ')
                f.write(content)
                f.write('\n\n')
        res = 'The above material has been written in ' + os.path.abspath(f'./analyzer_logs/{file_name}')
        print(res)
        return res

    @staticmethod
    def fetch_and_summarize(apikey_textbox, source_textbox, source_target_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history):
        g_inputs = GradioInputs(apikey_textbox, source_textbox, source_target_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history)
        g_inputs.history = []
        g_inputs.chatbot = []

        if g_inputs.apikey_textbox == "" or g_inputs.source_textbox == "" or g_inputs.source_target_textbox == "":
            LLMService.report_exception(g_inputs.chatbot, g_inputs.history,
                                        chat_input=f"Source target: [{g_inputs.source_textbox}] {g_inputs.source_target_textbox}",
                                        chat_output=f"{provide_text_with_css('ERROR', 'red')} Please provide api key, source and target source")
            yield g_inputs.chatbot, g_inputs.history, 'Error', WAITING_FOR_TARGET_INPUT
            return
        # TODO: invalid input checking
        is_success, text_data = yield from DigesterService.fetch_text(g_inputs)
        if not is_success:
            return  # TODO: error handling testing
        yield from PromptEngineeringStrategy.execute_prompt_chain(g_inputs, text_data)

    @staticmethod
    def ask_question(apikey_textbox, source_textbox, target_source_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history):
        g_inputs = GradioInputs(apikey_textbox, source_textbox, target_source_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history)
        prompt = f"ask_question(`{qa_textbox}`)"
        g_inputs.chatbot.append((prompt, "Currently the ask feature is not supported yet"))
        yield g_inputs.chatbot, g_inputs.history, 'Normal'

    @staticmethod
    def test_formatting(apikey_textbox, source_textbox, target_source_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history):
        g_inputs = GradioInputs(apikey_textbox, source_textbox, target_source_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history)
        msg = r"""
# ASCII, table, code test
Overall, this program consists of the following files:
- `main.py`: This is the primary script of the program which uses NLP to analyze and summarize Python code.
- `model.py`: This file defines the `CodeModel` class that is used by `main.py` to model the code as graphs and performs operations on them.
- `parser.py`: This file contains custom parsing functions used by `model.py`.
- `test/`: This directory contains test scripts for `model.py` and `util.py`
- `util.py`: This file provides utility functions for the program such as getting the root directory of the project and reading configuration files.

`util.py` specifically has two functions:

| Function | Input | Output | Functionality |
|----------|-------|--------|---------------|
| `get_project_root()` | None | String containing the path of the parent directory of the script itself | Finds the path of the parent directory of the script itself |
| `get_config()` | None | Dictionary containing the contents of `config.yaml` and `config_secret.yaml`, merged together (with `config_secret.yaml` overwriting any keys with the same name in `config.yaml`) | Reads and merges two YAML configuration files (`config.yaml` and `config_secret.yaml`) located in the `config` directory in the parent directory of the script. Returns the resulting dictionary. |The above material has been written in C:\github\!CodeAnalyzerGPT\CodeAnalyzerGPT\analyzer_logs\chatGPT_report2023-04-07-14-11-55.md

The Hessian matrix is a square matrix that contains information about the second-order partial derivatives of a function. Suppose we have a function $f(x_1,x_2,...,x_n)$ which is twice continuously differentiable. Then the Hessian matrix $H(f)$ of $f$ is defined as the $n\times n$ matrix:

$$H(f) = \begin{bmatrix} \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \ \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \ \vdots & \vdots & \ddots & \vdots \ \frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2} \ \end{bmatrix}$$

Each element in the Hessian matrix is the second-order partial derivative of the function with respect to a pair of variables, as shown in the matrix above

Here's an example Python code using SymPy module to get the derivative of a mathematical function:

```
import sympy as sp

x = sp.Symbol('x')
f = input('Enter a mathematical function in terms of x: ')
expr = sp.sympify(f)

dfdx = sp.diff(expr, x)
print('The derivative of', f, 'is:', dfdx)
```

This code will prompt the user to enter a mathematical function in terms of x and then use the `diff()` function from SymPy to calculate its derivative with respect to x. The result will be printed on the screen.



# Non-ASCII test

程序整体功能：CodeAnalyzerGPT工程是一个用于自动化代码分析和评审的工具。它使用了OpenAI的GPT模型对代码进行分析，然后根据一定的规则和标准来评价代码的质量和合规性。

程序的构架包含以下几个模块：

1. CodeAnalyzerGPT: 主程序模块，包含了代码分析和评审的主要逻辑。

2. analyzer: 包含了代码分析程序的具体实现。

每个文件的功能可以总结为下表：

| 文件名 | 功能描述 |
| --- | --- |
| C:\github\!CodeAnalyzerGPT\CodeAnalyzerGPT\CodeAnalyzerGPT.py | 主程序入口，调用各种处理逻辑和输出结果 |
| C:\github\!CodeAnalyzerGPT\CodeAnalyzerGPT\analyzer\code_analyzer.py | 代码分析器，包含了对代码文本的解析和分析逻辑 |
| C:\github\!CodeAnalyzerGPT\CodeAnalyzerGPT\analyzer\code_segment.py | 对代码文本进行语句和表达式的分段处理 |

    """
        g_inputs.chatbot.append(("test prompt query", msg))
        yield g_inputs.chatbot, g_inputs.history, 'Normal'

    @staticmethod
    def test_asking(apikey_textbox, source_textbox, target_source_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history):
        g_inputs = GradioInputs(apikey_textbox, source_textbox, target_source_textbox, qa_textbox, gpt_model_textbox, language_textbox, chatbot, history)
        msg = f"test_ask(`{qa_textbox}`)"
        g_inputs.chatbot.append(("test prompt query", msg))
        g_inputs.chatbot.append(("test prompt query 2", msg))
        g_inputs.chatbot.append(("", "test empty message"))
        g_inputs.chatbot.append(("test empty message 2", ""))
        g_inputs.chatbot.append((None, "output msg, test no input msg"))
        g_inputs.chatbot.append(("input msg, , test no output msg", None))
        g_inputs.chatbot.append((None, '<span style="background-color: yellow; color: black; padding: 3px; border-radius: 8px;">WARN</span>'))
        yield g_inputs.chatbot, g_inputs.history, 'Normal'


class DigesterService:
    @staticmethod
    def update_ui(chatbot_input, chatbot_output, status, target_md, chatbot, history, is_append=True):
        """
        For instant chatbot_input+output
        Not suitable if chatbot_output have delay / processing time
        """
        if is_append:
            chatbot.append((chatbot_input, chatbot_output))
        else:
            chatbot[-1] = (chatbot_input, chatbot_output)
        history.append(chatbot_input)
        history.append(chatbot_output)
        yield chatbot, history, status, target_md

    @staticmethod
    def fetch_text(g_inputs: GradioInputs) -> (bool, BaseData):
        """Fetch text from source using everything2text4prompt. No OpenAI call here"""
        converter = Everything2Text4Prompt(openai_api_key=g_inputs.apikey_textbox)
        text_data, is_success, error_msg = converter.convert_text(g_inputs.source_textbox, g_inputs.source_target_textbox)
        text_content = text_data.full_content

        chatbot_input = f"Converting source to text for [{g_inputs.source_textbox}] {g_inputs.source_target_textbox} ..."
        target_md = f"[{g_inputs.source_textbox}] {g_inputs.source_target_textbox}"
        if is_success:
            chatbot_output = f"""
Extracted text successfully:

{text_content}
            """
            yield from DigesterService.update_ui(chatbot_input, chatbot_output, "Success", target_md, g_inputs.chatbot, g_inputs.history)
        else:
            chatbot_output = f"""
{provide_text_with_css("ERROR", "red")} Text extraction failed ({error_msg})
            """
            yield from DigesterService.update_ui(chatbot_input, chatbot_output, "Error", target_md, g_inputs.chatbot, g_inputs.history)
        return is_success, text_data


class PromptEngineeringStrategy:
    @staticmethod
    def execute_prompt_chain(g_inputs: GradioInputs, text_data: BaseData):
        if g_inputs.source_textbox == 'youtube':
            yield from PromptEngineeringStrategy.execute_prompt_chain_youtube(g_inputs, text_data)
        elif g_inputs.source_textbox == 'podcast':
            yield from PromptEngineeringStrategy.execute_prompt_chain_podcast(g_inputs, text_data)

    @staticmethod
    def execute_prompt_chain_youtube(g_inputs: GradioInputs, text_data: YoutubeData):
        yield from YoutubeChain.execute_chain(g_inputs, text_data)

    @staticmethod
    def execute_prompt_chain_podcast(g_inputs: GradioInputs, text_data: PodcastData):
        pass


class Chain:
    @staticmethod
    def execute_chain(g_inputs: GradioInputs, text_data: YoutubeData):
        raise NotImplementedError


class YoutubeChain(Chain):
    CLASSIFIER_PROMPT = Prompt(
        prompt_prefix="""
[Youtube Video types]
N things: The youtube will shows N items that will be described in the video. For example "17 cheap purchases that save me time", "10 AMAZING Ways AutoGPT Is Being Used RIGHT NOW". Usually the title starts with a number.
Tutorials: how to do or make something in order to teach a skill or how to use a product or software
How-to and DIY: People show how to make or do something yourself, like crafts, recipes, projects, etc
Interview: Interviewee shows their standpoint with a topic.
Others: If the video type is not listed above

[TITLE]
{title}

[TRANSCRIPT]
""",
        prompt_main="""
{transcript}
""",
        prompt_suffix="""
[TASK]
From the above title, transcript, classify the youtube video type listed above.
Give the video type with JSON format like {"type": "N things"}, and exclude other text.
""")
    TIMESTAMPED_SUMMARY_PROMPT = Prompt(
        prompt_prefix="""
[TITLE]
{title}

[Transcript with timestamp]
""",
        prompt_main="""
{transcript_with_ts}
""",
        prompt_suffix="""
[TASK]
Convert this into youtube summary. 
Separate for 2-5minutes chunk, maximum 20 words for one line.
Start with the timestamp followed by the summarized text for that chunk.
Must use language: {language}

Example format:
{first_timestamp} - This is the first part
{second_minute}:44 - This is the second part
{third_minute}:02 - This is the third part
""")

    FINAL_SUMMARY_PROMPT = Prompt(
        prompt_prefix="""
[VIDEO_TYPE]
This is the video type
N things: The youtube will shows N items that will be described in the video. For example "17 cheap purchases that save me time", "10 AMAZING Ways AutoGPT Is Being Used RIGHT NOW"
Tutorials: how to do or make something in order to teach a skill or how to use a product or software

[TITLE]
{title}

[TRANSCRIPT]
""",
        prompt_main="""
{transcript}
""",
        prompt_suffix="""
[TASK]
Summarize the above transcript. Step by step showing points for the main concepts.
Use markdown format.
Must use language: {language}
{task_constraint} 

The format is like:
Summary: (content of summary)
{format_constraint}
""")

    FINAL_SUMMARY_TASK_CONSTRAINTS = {
        "N things": """
Additionally, since it is a N things video, the summary should include the N items stated in the video.
""",
        "Tutorials": """
Additionally, since it is a Tutorial video, provide step by step instructions for the tutorial. 
""",
    }
    FINAL_SUMMARY_FORMAT_CONSTRAINTS = {
        "N things": """
Items mentioned in the video: (content of N things)
""",
        "Tutorials": """
Instructions: (step by step instructions)
""",
    }

    @staticmethod
    def execute_chain(g_inputs: GradioInputs, text_data: YoutubeData):
        text_content = text_data.full_content
        timestamped_summary = yield from YoutubeChain.execute_timestamped_summary_chain(g_inputs, text_data)
        video_type = yield from YoutubeChain.execute_classifer_chain(g_inputs, text_data)
        final_summary = yield from YoutubeChain.execute_final_summary_chain(g_inputs, text_data, video_type)
        full_summary = f"""
{provide_text_with_css("✅DONE", "green")}
🎞️Video: {text_data.title}
📝Timestamped summary
{timestamped_summary}

📝Summary
{final_summary}

{RESPONSE_SUFFIX}
        """
        prompt_show_user = "Full summary"
        g_inputs.chatbot[-1] = (prompt_show_user, full_summary)
        g_inputs.history.append(prompt_show_user)
        g_inputs.history.append(full_summary)
        yield g_inputs.chatbot, g_inputs.history, "Success", f"[{g_inputs.source_textbox}] {g_inputs.source_target_textbox}"

    @classmethod
    def execute_classifer_chain(cls, g_inputs: GradioInputs, youtube_data: YoutubeData):
        TRANSCRIPT_CHAR_LIMIT = 200  # Because classifer don't need to see the whole transcript
        prompt = Prompt(cls.CLASSIFIER_PROMPT.prompt_prefix.format(title=youtube_data.title),
                        cls.CLASSIFIER_PROMPT.prompt_main.format(transcript=youtube_data.full_content[:TRANSCRIPT_CHAR_LIMIT]),
                        cls.CLASSIFIER_PROMPT.prompt_suffix
                        )
        prompt_show_user = "Classify the video type for me"
        response, len_prompts = yield from ChatGPTService.trigger_callgpt_pipeline(prompt, prompt_show_user, g_inputs)
        try:
            video_type = json.loads(response)['type']
        except Exception as e:
            # TODO: Exception handling, show error in UI
            video_type = 'Others'
        return video_type

    @classmethod
    def execute_timestamped_summary_chain(cls, g_inputs: GradioInputs, youtube_data: YoutubeData):
        transcript_with_ts = ""
        for entry in youtube_data.ts_transcript_list:
            transcript_with_ts += f"{int(entry['start'] // 60)}:{int(entry['start'] % 60):02d} {entry['text']}\n"
        prompt = Prompt(cls.TIMESTAMPED_SUMMARY_PROMPT.prompt_prefix.format(title=youtube_data.title),
                        cls.TIMESTAMPED_SUMMARY_PROMPT.prompt_main.format(transcript_with_ts=transcript_with_ts),
                        cls.TIMESTAMPED_SUMMARY_PROMPT.prompt_suffix.replace("{language}", g_inputs.language_textbox)
                        )
        prompt_show_user = "Generate the timestamped summary"
        response, len_prompts = yield from ChatGPTService.trigger_callgpt_pipeline(prompt, prompt_show_user, g_inputs, is_timestamp=True)
        return response

    @classmethod
    def execute_final_summary_chain(cls, g_inputs: GradioInputs, youtube_data: YoutubeData, video_type):
        if video_type in cls.FINAL_SUMMARY_TASK_CONSTRAINTS.keys():
            task_constraint = cls.FINAL_SUMMARY_TASK_CONSTRAINTS[video_type]
            format_constraint = cls.FINAL_SUMMARY_FORMAT_CONSTRAINTS[video_type]
        else:
            task_constraint, format_constraint = "", ""
        prompt = Prompt(
            cls.FINAL_SUMMARY_PROMPT.prompt_prefix.format(title=youtube_data.title),
            cls.FINAL_SUMMARY_PROMPT.prompt_main.format(transcript=youtube_data.full_content),
            cls.FINAL_SUMMARY_PROMPT.prompt_suffix.format(task_constraint=task_constraint, format_constraint=format_constraint, language=g_inputs.language_textbox)
        )
        prompt_show_user = "Generate the final summary"
        response, len_prompts = yield from ChatGPTService.trigger_callgpt_pipeline(prompt, prompt_show_user, g_inputs)
        if len_prompts > 1:
            # Give summary of summaries if the video is long
            prompt = Prompt(
                cls.FINAL_SUMMARY_PROMPT.prompt_prefix.format(title=youtube_data.title),
                cls.FINAL_SUMMARY_PROMPT.prompt_main.format(transcript=response),
                cls.FINAL_SUMMARY_PROMPT.prompt_suffix.format(task_constraint=task_constraint, format_constraint=format_constraint, language=g_inputs.language_textbox)
            )
            prompt_show_user = "Since the video is long, generating the final summary of the summaries"
            response, len_prompts = yield from ChatGPTService.trigger_callgpt_pipeline(prompt, prompt_show_user, g_inputs)
        return response


if __name__ == '__main__':
    GPT_MODEL = "gpt-3.5-turbo-16k"
    API_KEY = ""
    input_1 = """Give me 2 ideas for the summer"""
    # input_1 = """Explain more on the first idea"""
    response_1 = ChatGPTService.single_rest_call_chatgpt(API_KEY, input_1, GPT_MODEL)
    print(response_1)

    input_2 = """
For the first idea, suggest some step by step planning for me
    """
    response_2 = ChatGPTService.single_rest_call_chatgpt(API_KEY, input_2, GPT_MODEL, history=[input_1, response_1])
    print(response_2)
