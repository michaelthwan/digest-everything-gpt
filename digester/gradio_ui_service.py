import gradio as gr
import markdown

from digester.code_analyzer import GradioMethodService

title_html = "<h1 align=\"center\">DigestEverythingGPT</h1>"

cancel_handles = []


class GradioUIService:
    @staticmethod
    def get_functions():
        functions = {
            "Fetch and summarize!": {
                "function": GradioMethodService.fetch_and_summarize,
            },
            "Ask": {
                "function": GradioMethodService.ask_question
            },
            "Test formatting": {
                "function": GradioMethodService.test_formatting
            },
            "Test asking": {
                "function": GradioMethodService.test_asking
            },
        }
        return functions

    @staticmethod
    def post_define_functions(functions, folder_md):
        """Append extra gradio objects to functions after creating gradio objects"""
        functions["Fetch and summarize!"]["extra_outputs"] = [folder_md]
        return functions

    @staticmethod
    def get_gradio_ui():
        def get_extra_outputs(functions, fn_key):
            if functions[fn_key].get('extra_outputs'):
                return functions[fn_key]['extra_outputs']
            return []

        gr.Chatbot.postprocess = GradioUIService.format_io
        functions = GradioUIService.get_functions()
        with gr.Blocks(theme=GradioUIService.get_theme(), css=GradioUIService.get_css()) as demo:
            gr.HTML(title_html)
            with gr.Row().style(equal_height=True):
                with gr.Column(scale=1):
                    with gr.Row():
                        apikey_textbox = gr.Textbox(label="OpenAI API key", placeholder="e.g. sk-xxxxx")
                    with gr.Row():
                        source_textbox = gr.Dropdown(
                            ["youtube", "podcast", "pdf"], label="Source", info="Choose your content provider"
                            # TODO: dynamic list from everything2text4prompt
                        )
                    with gr.Row():
                        source_target_textbox = gr.Textbox(show_label=True, label="URL / source target",
                                                           placeholder="For youtube video, give video id\nFor podcast, give podcast URL")
                    with gr.Row():
                        functions["Fetch and summarize!"]["btn"] = gr.Button("Fetch and summarize!", variant="primary")
                    with gr.Row().style(equal_height=True):
                        gr.Markdown(f"Status: ")
                        status_md = gr.Markdown(f"Normal")
                    with gr.Row():
                        folder_md = gr.Markdown(f"Waiting for source target input")
                    with gr.Row():
                        qa_textbox = gr.Textbox(show_label=False, placeholder="Ask questions").style(container=False)
                    with gr.Row():
                        functions["Ask"]["btn"] = gr.Button("Ask", variant="primary")
                    with gr.Row():
                        reset_btn = gr.Button("Reset", variant="secondary")
                        reset_btn.style(size="sm")
                        stop_btn = gr.Button("Stop", variant="secondary")
                        stop_btn.style(size="sm")
                    with gr.Accordion("debug", open=True):
                        with gr.Row():
                            functions["Test formatting"]["btn"] = gr.Button("Test formatting")
                            functions["Test asking"]["btn"] = gr.Button("Test asking")

                with gr.Column(scale=3):
                    chatbot = gr.Chatbot()
                    chatbot.style(height=1100)
                    history = gr.State([])
            # after creating gradio objects, append to functions to centralize things.
            functions = GradioUIService.post_define_functions(functions, folder_md)
            #### handle click(=submit) and cancel behaviour
            # Standard inputs/outputs (global for all actions)
            inputs = [apikey_textbox, source_textbox, source_target_textbox, qa_textbox, chatbot, history]
            outputs = [chatbot, history, status_md]
            # fetch_and_summarize_textbox
            fn_key = "Fetch and summarize!"
            analyze_code_base_args = dict(fn=functions[fn_key]["function"], inputs=inputs, outputs=[*outputs, folder_md])
            cancel_handles.append(source_target_textbox.submit(**analyze_code_base_args))
            # qa_textbox
            fn_key = "Ask"
            ask_args = dict(fn=functions[fn_key]["function"], inputs=inputs, outputs=outputs)
            cancel_handles.append(qa_textbox.submit(**ask_args))
            # all buttons
            for fn_key in functions:
                click_handle = functions[fn_key]["btn"].click(fn=functions[fn_key]["function"],
                                                              inputs=inputs, outputs=[*outputs, *get_extra_outputs(functions, fn_key)])
                cancel_handles.append(click_handle)
            stop_btn.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)
            reset_btn.click(fn=lambda: ([], [], "Already reset"), inputs=None, outputs=outputs)
        demo.title = "CodeAnalyzerGPT"
        return demo

    def format_io(self, y):
        """
        Convert the input and output to HTML format.
            Paragraphize the input part of the last item in y,
            and convert the Markdown and mathematical formula in the output part to HTML format.
        """

        def text_divide_paragraph(text):
            """
            Separate the text according to the paragraph separator and generate HTML code with paragraph tags.
            """
            if '```' in text:
                return text
            else:
                lines = text.split("\n")
                for i, line in enumerate(lines):
                    lines[i] = lines[i].replace(" ", "&nbsp;")
                text = "</br>".join(lines)
                return text

        def close_up_code_segment_during_stream(gpt_reply):
            """
            Handling when the GPT output is cut in half
            Add '```' at the end of the output if the output is not complete.
            """
            # guard pattern for normal cases
            if '```' not in gpt_reply:
                return gpt_reply
            if gpt_reply.endswith('```'):
                return gpt_reply

            # otherwise
            segments = gpt_reply.split('```')
            n_mark = len(segments) - 1
            if n_mark % 2 == 1:
                return gpt_reply + '\n```'
            else:
                return gpt_reply

        def markdown_convertion(txt):
            """
            Convert markdown text to HTML format
            """
            pre = '<div class="markdown-body">'
            suf = '</div>'
            # if ('$' in txt) and ('```' not in txt):
            #     return pre + markdown.markdown(txt, extensions=['fenced_code', 'tables']) + '<br><br>' + markdown.markdown(convert_math(txt, splitParagraphs=False),
            #                                                                                                                extensions=['fenced_code', 'tables']) + suf
            # else:
            #     return pre + markdown.markdown(txt, extensions=['fenced_code', 'tables']) + suf
            return pre + markdown.markdown(txt, extensions=['fenced_code', 'tables']) + suf

        if y is None or y == []: return []
        i_ask, gpt_reply = y[-1]
        i_ask = text_divide_paragraph(i_ask)
        gpt_reply = close_up_code_segment_during_stream(gpt_reply)
        y[-1] = (
            None if i_ask is None else markdown.markdown(i_ask, extensions=['fenced_code', 'tables']),
            None if gpt_reply is None else markdown_convertion(gpt_reply)
        )
        return y

    @staticmethod
    def get_theme():
        try:
            set_theme = gr.themes.Default(
                primary_hue=gr.themes.utils.colors.cyan,
                neutral_hue=gr.themes.utils.colors.gray,
                font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif", ],
                font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "Consolas", "ui-monospace", "monospace"]
            )
        except Exception as e:
            set_theme = None
            print(f'please upgrade to newer version of gradio {e}')
        return set_theme

    @staticmethod
    def get_css():
        css = """
/* Set the outer margins of the table to 1em, merge the borders between internal cells, and display empty cells. */
.markdown-body table {
    margin: 1em 0;
    border-collapse: collapse;
    empty-cells: show;
}

/* Set the inner margin of the table cell to 5px, the border thickness to 1.2px, and the color to --border-color-primary. */
.markdown-body th, .markdown-body td {
    border: 1.2px solid var(--border-color-primary);
    padding: 5px;
}

/* Set the table header background color to rgba(175,184,193,0.2) and transparency to 0.2. */
.markdown-body thead {
    background-color: rgba(175,184,193,0.2);
}

/* Set the padding of the table header cell to 0.5em and 0.2em. */
.markdown-body thead th {
    padding: .5em .2em;
}

/* Remove the default padding of the list prefix to align it with the text line. */
.markdown-body ol, .markdown-body ul {
    padding-inline-start: 2em !important;
}

/* Set the style of the chat bubble, including the radius, the maximum width, and the shadow. */
[class *= "message"] {
    border-radius: var(--radius-xl) !important;
    /* padding: var(--spacing-xl) !important; */
    /* font-size: var(--text-md) !important; */
    /* line-height: var(--line-md) !important; */
    /* min-height: calc(var(--text-md)*var(--line-md) + 2*var(--spacing-xl)); */
    /* min-width: calc(var(--text-md)*var(--line-md) + 2*var(--spacing-xl)); */
}
[data-testid = "bot"] {
    max-width: 95%;
    /* width: auto !important; */
    border-bottom-left-radius: 0 !important;
}
[data-testid = "user"] {
    max-width: 100%;
    /* width: auto !important; */
    border-bottom-right-radius: 0 !important;
}

/* Set the background of the inline code to light gray, set the radius and spacing. */
.markdown-body code {
    font-family: 'JetBrains Mono', monospace;
    display: inline;
    white-space: break-spaces;
    border-radius: 6px;
    margin: 0 2px 0 2px;
    padding: .2em .4em .1em .4em;
    background-color: rgba(175,184,193,0.2);
}
/* Set the style of the code block, including the background color, the inner and outer margins, and the radius. */
.markdown-body pre code {
    font-family: 'JetBrains Mono', monospace;
    display: block;
    overflow: auto;
    white-space: pre;
    background-color: rgba(175,184,193,0.2);
    border-radius: 10px;
    padding: 1em;
    margin: 1em 2em 1em 0.5em;
}
"""
        return css
