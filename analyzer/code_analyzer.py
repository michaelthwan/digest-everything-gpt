import glob
import os
import time

from analyzer.chatgpt_service import LLMService, ChatGPTService

WAITING_FOR_PF_INPUT = "Waiting for project folder input"


class CodeAnalyzerService:
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
    def get_project_folder_md(project_folder_textbox):
        return f"Current:\n{project_folder_textbox}"

    @staticmethod
    def analyze_project(file_manifest, pf_md, project_folder, chatbot, history):
        print('begin analysis on:', file_manifest)
        for index, fp in enumerate(file_manifest):
            status = 'Normal'
            with open(fp, 'r', encoding='utf-8') as f:
                file_content = f.read()

            # for each file, ask chatgpt
            prefix = "Please analyze the following files.\n" if index == 0 else ""
            i_say = prefix + f'Please make a summary of the following program file. File name: {os.path.relpath(fp, project_folder)}. Source code: ```{file_content}```'
            i_say_show_user = prefix + f'[{index + 1}/{len(file_manifest)}] Please make a summary of the following program file: {os.path.abspath(fp)}'

            yield from ChatGPTService.call_chatgpt(i_say, i_say_show_user, chatbot, history, status, pf_md)

            i_say = """
Please describe each function with format

- <method name>(<input>) -> <output>:
<description> 
- <method name>(<input>) -> <output>:
<description>
File name: {os.path.relpath(fp, project_folder)}. Source code: ```{file_content}```"""
            i_say_show_user = f'[{index + 1}/{len(file_manifest)}] Please describe each function: {os.path.abspath(fp)}'
            yield from ChatGPTService.call_chatgpt(i_say, i_say_show_user, chatbot, history, status, pf_md)

            # chatbot.append((i_say_show_user, "[INFO] waiting for ChatGPT's response."))
            # yield chatbot, history, status, pf_md
            # gpt_say = yield from ChatGPTService.predict_no_ui_but_counting_down(pf_md, i_say, i_say_show_user, chatbot, history=[])
            # chatbot[-1] = (i_say_show_user, gpt_say)
            # history.append(i_say_show_user)
            # history.append(gpt_say)
            # yield chatbot, history, status, pf_md

            time.sleep(2)

        # Overall, ask chatgpt
        all_file = ', '.join([os.path.relpath(fp, project_folder) for index, fp in enumerate(file_manifest)])
        i_say = f'Based on your own analysis above, make a summary of the overall functionality and architecture of the program. Then use a markdown table to explain the functionality of each file (including {all_file}).'
        i_say_show_user = i_say

        yield from ChatGPTService.call_chatgpt(i_say, i_say_show_user, chatbot, history, status, pf_md)
        # chatbot.append((i_say_show_user, "[INFO] waiting for ChatGPT's response."))
        # yield chatbot, history, status, pf_md
        # gpt_say = yield from ChatGPTService.predict_no_ui_but_counting_down(pf_md, i_say, i_say, chatbot, history=history)
        # chatbot[-1] = (i_say_show_user, gpt_say)
        # history.append(i_say_show_user)
        # history.append(gpt_say)
        # yield chatbot, history, status, pf_md

        res = CodeAnalyzerService.write_results_to_file(history)
        chatbot.append(("Completed? ", res))
        yield chatbot, history, status, pf_md

    @staticmethod
    def analyze_python_project(project_folder_textbox, qa_textbox, chatbot, history):
        history = []
        pf_md = CodeAnalyzerService.get_project_folder_md(project_folder_textbox)  # pf_md = project folder markdown

        if not os.path.exists(project_folder_textbox):
            if project_folder_textbox == "":
                project_folder_textbox = 'Empty input'
                LLMService.report_exception(chatbot, history,
                                            a=f"Project folder analyzed: {project_folder_textbox}",
                                            b=f"Cannot find the project folder / no permission to read: {project_folder_textbox}")
                yield chatbot, history, 'Normal', WAITING_FOR_PF_INPUT
                return

        project_folder = project_folder_textbox
        file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.py', recursive=True)]
        if len(file_manifest) == 0:
            LLMService.report_exception(chatbot, history,
                                        a=f"Project folder analyzed: {project_folder_textbox}",
                                        b=f"Cannnot find any .py files: {project_folder_textbox}")
            yield chatbot, history, 'Normal', WAITING_FOR_PF_INPUT
            return
        yield from CodeAnalyzerService.analyze_project(file_manifest, pf_md, project_folder, chatbot, history)

    @staticmethod
    def ask_question(project_folder_textbox, qa_textbox, chatbot, history):
        msg = f"ask_question(`{qa_textbox}`)"
        chatbot.append(("test prompt query", msg))
        yield chatbot, history, 'Normal'

    @staticmethod
    def test_asking(project_folder_textbox, qa_textbox, chatbot, history):
        msg = f"test_ask(`{qa_textbox}`)"
        chatbot.append(("test prompt query", msg))
        yield chatbot, history, 'Normal'

    @staticmethod
    def test_formatting(txt, qa_textbox, chatbot, history):
        msg = r"""
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

    """
        chatbot.append(("test prompt query", msg))
        yield chatbot, history, 'Normal'
