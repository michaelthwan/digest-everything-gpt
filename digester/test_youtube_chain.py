from chatgpt_service import ChatGPTService
from everything2text4prompt.everything2text4prompt import Everything2Text4Prompt
from everything2text4prompt.util import BaseData, YoutubeData, PodcastData
from gradio_method_service import YoutubeChain

import json


class VideoExample:
    def __init__(self, title, description, transcript):
        self.title = title
        self.description = description
        self.transcript = transcript

    @classmethod
    def get_youtube_data(cls, api_key: str, video_id: str):
        converter = Everything2Text4Prompt(openai_api_key=api_key)
        text_data, is_success, error_msg = converter.convert_text("youtube", video_id)
        text_data: YoutubeData
        title = text_data.title
        description = text_data.description
        transcript = text_data.full_content
        ts_transcript_list = text_data.ts_transcript_list
        return YoutubeData(transcript, title, description, ts_transcript_list)

    @staticmethod
    def get_nthings_10_autogpt():
        video_id = "lSTEhG021Jc"
        return VideoExample.get_youtube_data("", video_id)

    @staticmethod
    def get_nthings_7_lifelesson():
        video_id = "CUPe_TZECQQ"
        return VideoExample.get_youtube_data("", video_id)

    @staticmethod
    def get_tutorial_skincare():
        video_id = "OrElyY7MFVs"
        return VideoExample.get_youtube_data("", video_id)


class TestChain():
    @staticmethod
    def test_compression():
        pass  # TODO


class YoutubeTestChain:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def run_testing_chain(self):
        input_1 = """Give me 2 ideas for the summer"""
        # input_1 = """Explain more on the first idea"""
        response_1 = ChatGPTService.single_call_chatgpt(self.api_key, input_1)

        input_2 = """
    For the first idea, suggest some step by step planning for me
        """
        response_2 = ChatGPTService.single_call_chatgpt(self.api_key, input_2, [input_1, response_1])

    def test_youtube_classifier(self, youtube_data: YoutubeData):
        TRANSCRIPT_CHAR_LIMIT = 200  # Because classifer don't need to see the whole transcript
        input_1 = YoutubeChain.CLASSIFIER_PROMPT.format(title=youtube_data.title, transcript=youtube_data.full_content[:TRANSCRIPT_CHAR_LIMIT]) + YoutubeChain.CLASSIFER_TASK_PROMPT
        response_1 = ChatGPTService.single_call_chatgpt(self.api_key, input_1)
        video_type = json.loads(response_1)['type']
        print(f"\nparsed video_type: \n{video_type}")

    def test_youtube_timestamped_summary(self, youtube_data: YoutubeData):
        transcript_with_ts = ""
        for entry in youtube_data.ts_transcript_list:
            transcript_with_ts += f"{int(entry['start'] // 60)}:{int(entry['start'] % 60):02d} {entry['text']}\n"
        prompt = YoutubeChain.TIMESTAMPED_SUMMARY_PROMPT.format(title=youtube_data.title, transcript_with_ts=transcript_with_ts)
        prompt_show_user, chatbot = "", ['prompt1', 'response1']
        response = yield from ChatGPTService.multi_call_chatgpt_with_handling("", prompt, prompt_show_user, chatbot, self.api_key, history=[])
        # print(f"\nresponse_1: \n{response}")

    def test_youtube_final_summary(self, video_type: str, youtube_data: YoutubeData):
        if video_type in YoutubeChain.FINAL_SUMMARY_TASKS.keys():
            task_constraint = YoutubeChain.FINAL_SUMMARY_TASKS[video_type]
        else:
            task_constraint = ""
        prompt = YoutubeChain.FINAL_SUMMARY_PROMPT.format(title=youtube_data.title, transcript=youtube_data.full_content, task_constraint=task_constraint)
        prompt_show_user, chatbot = "", ['prompt1', 'response1']
        response = yield from ChatGPTService.multi_call_chatgpt_with_handling("", prompt, prompt_show_user, chatbot, self.api_key, history=[])
        # print(f"\nresponse: \n{response}")


if __name__ == '__main__':
    API_KEY = ""
    TARGET_SOURCE = "lSTEhG021Jc"
    assert API_KEY

    youtube_data: YoutubeData = VideoExample.get_tutorial_skincare()

    youtube_test_chain = YoutubeTestChain(API_KEY)
    # youtube_test_chain.test_youtube_classifier(youtube_data)
    next(youtube_test_chain.test_youtube_timestamped_summary(youtube_data))
    # video_type = "N things"
    video_type = "Others"
    # next(youtube_test_chain.test_youtube_final_summary(video_type, youtube_data))

    # converter = Everything2Text4Prompt(openai_api_key="")
    # source_textbox = "youtube"
    # target_source_textbox = "CUPe_TZECQQ"
    # text_data, is_success, error_msg = converter.convert_text(source_textbox, target_source_textbox)
    # print(text_data.title)
    # print(text_data.description)
    # print(text_data.full_content)
    # print(text_data.ts_transcript_list)
