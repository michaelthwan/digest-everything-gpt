from chatgpt_service import ChatGPTService
from everything2text4prompt.everything2text4prompt import Everything2Text4Prompt
from everything2text4prompt.util import BaseData, YoutubeData, PodcastData
from gradio_method_service import YoutubeChain, GradioInputs
from digester.util import get_config, Prompt

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
    def get_nthings_8_habits():
        video_id = "IScN1SOcj7A"
        return VideoExample.get_youtube_data("", video_id)

    @staticmethod
    def get_tutorial_skincare():
        video_id = "OrElyY7MFVs"
        return VideoExample.get_youtube_data("", video_id)


class YoutubeTestChain:
    def __init__(self, api_key: str, gpt_model):
        self.api_key = api_key
        self.gpt_model = gpt_model

    def run_testing_chain(self):
        input_1 = """Give me 2 ideas for the summer"""
        # input_1 = """Explain more on the first idea"""
        response_1 = ChatGPTService.single_rest_call_chatgpt(self.api_key, input_1, self.gpt_model)

        input_2 = """
    For the first idea, suggest some step by step planning for me
        """
        response_2 = ChatGPTService.single_rest_call_chatgpt(self.api_key, input_2, self.gpt_model, history=[input_1, response_1])

    def test_youtube_classifier(self, gradio_inputs: GradioInputs, youtube_data: YoutubeData):
        iter = YoutubeChain.execute_classifer_chain(gradio_inputs, youtube_data)
        while True:
            next(iter)

    def test_youtube_timestamped_summary(self, gradio_inputs: GradioInputs, youtube_data: YoutubeData):
        iter = YoutubeChain.execute_timestamped_summary_chain(gradio_inputs, youtube_data)
        while True:
            next(iter)

    def test_youtube_final_summary(self, gradio_inputs: GradioInputs, youtube_data: YoutubeData, video_type):
        iter = YoutubeChain.execute_final_summary_chain(gradio_inputs, youtube_data, video_type)
        while True:
            next(iter)


if __name__ == '__main__':
    config = get_config()
    api_key = config.get("openai").get("api_key")
    assert api_key

    gradio_inputs = GradioInputs(apikey_textbox=api_key, source_textbox="", source_target_textbox="", qa_textbox="", chatbot=[], history=[])
    youtube_data: YoutubeData = VideoExample.get_nthings_8_habits()

    youtube_test_chain = YoutubeTestChain(api_key)
    # youtube_test_chain.test_youtube_classifier(gradio_inputs, youtube_data)
    youtube_test_chain.test_youtube_timestamped_summary(gradio_inputs, youtube_data)
    # video_type = "N things"
    # video_type = "Tutorials"
    # video_type = "Others"
    # youtube_test_chain.test_youtube_final_summary(gradio_inputs, youtube_data, video_type)

    # converter = Everything2Text4Prompt(openai_api_key="")
    # source_textbox = "youtube"
    # target_source_textbox = "CUPe_TZECQQ"
    # text_data, is_success, error_msg = converter.convert_text(source_textbox, target_source_textbox)
    # print(text_data.title)
    # print(text_data.description)
    # print(text_data.full_content)
    # print(text_data.ts_transcript_list)
