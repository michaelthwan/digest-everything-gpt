from chatgpt_service import ChatGPTService
from everything2text4prompt.everything2text4prompt import Everything2Text4Prompt
from everything2text4prompt.util import BaseData, YoutubeData, PodcastData

import json

CLASSIFIER_PROMPT = """
[Youtube Video types]
N things: The youtube will shows N items that will be described in the video. For example "17 cheap purchases that save me time", "10 AMAZING Ways AutoGPT Is Being Used RIGHT NOW"
Tutorials: how to do or make something in order to teach a skill or how to use a product or software
How-to and DIY: People show how to make or do something yourself, like crafts, recipes, projects, etc
Interview: Interviewee shows their standpoint with a topic.
Others: If the video type is not listed above

[TITLE]
{title}

[TRANSCRIPT]
{transcript}

"""

CLASSIFIER_PROMPT_TASK = """
[TASK]
From the above title, transcript, classify the youtube video type listed above
Give the video type with JSON format like {"type": "N things"}, and exclude other text
"""

TIMESTAMPED_SUMMARY_PROMPT = """
[TITLE]
{title}

[Transcript with timestamp]
{transcript_with_ts}
"""

TIMESTAMPED_SUMMARY_TASK = """
[TASK]
Convert this into youtube summary.
Separate for 2-5minutes chunk as one line, and start with the timestamp followed by the summarized text for that chunk
"""


class VideoExample:
    def __init__(self, title, description, transcript):
        self.title = title
        self.description = description
        self.transcript = transcript

    @staticmethod
    def get_lSTEhG021Jc():
        video_id = "lSTEhG021Jc"
        title = "10 AMAZING Ways AutoGPT Is Being Used RIGHT NOW"
        description = "Subscribe To My Channel: https://www.youtube.com/channel/UCPokyXp3FhVSQeZJ0bC2CqA?sub_confirmation=1#AutoGPT is available here:AutoGPT Website: https://news...."
        transcript = "if you're into chat gbt you're probably hearing about Auto GPT baby AGI and agents this is essentially GPT on steroids you see we're not hiring interns or assistants anymore now we're building them we're creating them and in this video we're going to talk about all the incredible ways that people are using Auto gbt right now there's also going to be a lot of Great Clips demos to show exactly what they're doing so make sure you stay until the very end solely is using Auto GPT to build a website in less than three minutes and he mentions that the results are so crazy that soon we won't even need a code anymore he also gives more information he mentions that the objective was very simple create a website using react and he does clarify that this was just a basic example to show what's possible it took him one hour to set up a team of smart Engineers could probably make an agent that's a hundred times more complicated Andy mentions took half a day to get it right I tried initially to just prompt it to build a website but it ends up getting stuck in a loop Felipe is also doing something really similar he's using Auto gbt in this case baby AGI to write code combining multiple files and then shortly after he mentions that he made some tweaks to make it a little bit better baby AGI following a detailed description of a small Python program and correctly creating it by managing multiple files with different classes in this version it can write new code edit existing code and run commands for example to install dependencies and this is pretty interesting he says that there are 11 agents in this system One agent allows human feedback before executing each task but it's disabled in this video this can possibly help to get better results from the tasks or skip unnecessary or duplicate tasks which he says happens a lot Omar is using it for sales prospecting and there's four important screenshots in the first one he gives it an objective he says we are a SAS that helps you save time on hiring interviews and in the following screenshots you start seeing how it does the research it compiles everything all the emails the contacts with the final result of drafting an email template for outbound emails to Target companies you're starting to see the trend Auto gbt can do all your busy work such as a to-do list that's how Garrett's using it the thing that he built was that every time you add a task a gpt4 agent is spawned to complete it it already has the context it needs on you and your company and has access to your apps that's also what Linus is using it for he was playing around with god mode and mentions that you can order your coffee at Starbucks perform market analysis and even find and negotiate a lease research is something that auto GPT seems to be pretty good at and that's also why David launched an agent specifically designed for research he gives three examples you can use it to write a podcast script based on the latest news you can also use it to get a market research report and also for new GitHub repos trending on Hacker News when you give it and objective the system will automatically break it down and complete it here's what it looks like if you want to write a script for a podcast but as you can imagine you can write a ton of different content whether it's for a website maybe you're trying to write a book get some more ideas that's what this can help you for and on the academic side if you're a teacher you can use Auto GPT to prepare lesson plans here's another example of an AI agent doing research for you and in this case James is also using Auto GPT to create an agent that researches current affairs and then prepares a podcast framework what about completing goals that's what a seam is doing give your own AI agent a goal and watch as it thinks comes up with an execution plan and takes actions and here's an interesting one Anise is using mobile auto GPT to deploy your own Auto GPT telegram bot you can also create Discord Bots and then the AI agents they can do all the work for you Soul decoder mentioned that this is insane we've added Auto GPT baby AGI in Discord ask our bot a question and it creates AI agents that operate automatically on their own and complete tasks for our marketing and Business Development staff can view output and collab on it very easily he also adds some additional thoughts if you thought Chachi PT was crazy Auto GPT takes it to the next level chains together llm's thoughts has internet access long and short-term memory access to websites and file storage with Discord we can view and even vote on the tasks it gives using emojis John is using it to create Virtual Worlds filled with AI agents this is crazy I ran a 100 agent-wide autonomous simulation of a virtual world as part of a research project for forever voices using nothing but Auto GPT and gpt4 in the second video you'll see that it decides on its own to bring forward an economic crisis among our 100 AI personas as part of the virtual world simulation it's kind of like you're having a bunch of Sims but this time they're a lot more advanced so who knows what they're talking about thinking about and planning to do next David is using in Auto GPT to interact with the blockchain today we signed one of the first ever transactions on the blockchain Via an autonomous AI agent kryptonot GPT is able to understand how to use crypto and send transactions and interact with defy in this example the agent swaps Matic for usdt and here's an interesting one Joshua the CEO of do not pay is using Auto gbt to manage his finances he says that getting a refund canceling a subscription fighting a credit bureau and many other robot lawyer products should be as simple as texting your friend so he gave Auto GPT access to his bank financial statements credit report and email and according to him he's up so far 217 dollars and 85 cents because Auto GPT is helping him save money and he shows exactly how he did it first using a do not pay plot connection I had it log into every bank account and credit card that I own and Scan 10 000 Plus transactions it found eighty dollars and eighty six cents leaving my account every month in useless subscriptions and offered to cancel every single one the Bots got to work mailing letters in the case of gyms chatting automatically with agents and even clicking online buttons to get them canceled you see what's possible it can chat with real agents and it can even click around on a website he gives even more details I asked it to scan the same transactions and find me one where I could get an easy refund from my email it identified a United Airlines in-flight Wi-Fi receipt for 36.99 from London to New York and then asked me did it work properly when I said no it immediately drafted a persuasive and firm legal letter to United requesting a refund the letter was both legalistic citing FTC statutes and convincing a bot then sent it to them via their website within 48 Hours United agreed to refund the 36.99 he keep keeps going I wanted to take a break from saving money and ask gpt4 about my credit score using the array API it got my score and Report without advertisements or trying to sell me a credit card I am currently working on several gbt credit disputes and will report back now it was time to unleash gpt4 on my bills I'm a customer of Comcast and so I asked it to negotiate my bill when Comcast offered a 50 discount the bot pushed back it said no I want more and it got 100 back GPT 3.5 never pushed back for what it's worth and he ends it like this I am already up 217.86 in under 24 hours and have a dozen other disputes pending my goal is to have gpt4 make me ten thousand dollars which one's your favorite let me know in the comments and if you're using Auto GPT right now share your thoughts the results your overall experiences whatever you want that's it I'll see you soon"
        ts_transcript_list = [{
            'text': "if you're into chat gbt you're probably hearing about Auto GPT baby AGI and agents this is essentially GPT on steroids you see we're not hiring interns or assistants anymore now we're building them we're creating them and in this video we're going to talk about all the incredible ways that people are using Auto gbt right now there's also going to be a lot of Great Clips demos to show exactly what they're doing so make sure you stay until the very end solely is using Auto GPT to build a",
            'start': 0.0}, {
            'text': "website in less than three minutes and he mentions that the results are so crazy that soon we won't even need a code anymore he also gives more information he mentions that the objective was very simple create a website using react and he does clarify that this was just a basic example to show what's possible it took him one hour to set up a team of smart Engineers could probably make an agent that's a hundred times more complicated Andy mentions took half a day to get it right I tried initially to just prompt it to build a website but it ends up getting",
            'start': 30.539}, {
            'text': "stuck in a loop Felipe is also doing something really similar he's using Auto gbt in this case baby AGI to write code combining multiple files and then shortly after he mentions that he made some tweaks to make it a little bit better baby AGI following a detailed description of a small Python program and correctly creating it by managing multiple files with different classes in this version it can write new code edit existing code and run commands for example to install dependencies and this is pretty interesting he says that there",
            'start': 62.1}, {
            'text': "are 11 agents in this system One agent allows human feedback before executing each task but it's disabled in this video this can possibly help to get better results from the tasks or skip unnecessary or duplicate tasks which he says happens a lot Omar is using it for sales prospecting and there's four important screenshots in the first one he gives it an objective he says we are a SAS that helps you save time on hiring interviews and in the following screenshots you start seeing how it does the research it compiles everything all",
            'start': 93.54}, {
            'text': "the emails the contacts with the final result of drafting an email template for outbound emails to Target companies you're starting to see the trend Auto gbt can do all your busy work such as a to-do list that's how Garrett's using it the thing that he built was that every time you add a task a gpt4 agent is spawned to complete it it already has the context it needs on you and your company and has access to your apps that's also what Linus is using it for he was playing around with god mode and mentions that you can order your coffee",
            'start': 123.6}, {
            'text': "at Starbucks perform market analysis and even find and negotiate a lease research is something that auto GPT seems to be pretty good at and that's also why David launched an agent specifically designed for research he gives three examples you can use it to write a podcast script based on the latest news you can also use it to get a market research report and also for new GitHub repos trending on Hacker News when you give it and objective the system will automatically break it down and complete it here's",
            'start': 153.959}, {
            'text': "what it looks like if you want to write a script for a podcast but as you can imagine you can write a ton of different content whether it's for a website maybe you're trying to write a book get some more ideas that's what this can help you for and on the academic side if you're a teacher you can use Auto GPT to prepare lesson plans here's another example of an AI agent doing research for you and in this case James is also using Auto GPT to create an agent that researches current affairs and then prepares a",
            'start': 184.2}, {
            'text': "podcast framework what about completing goals that's what a seam is doing give your own AI agent a goal and watch as it thinks comes up with an execution plan and takes actions and here's an interesting one Anise is using mobile auto GPT to deploy your own Auto GPT telegram bot you can also create Discord Bots and then the AI agents they can do all the work for you Soul decoder mentioned that this is insane we've added Auto GPT baby AGI in Discord ask our bot a question and it creates AI",
            'start': 214.26}, {
            'text': "agents that operate automatically on their own and complete tasks for our marketing and Business Development staff can view output and collab on it very easily he also adds some additional thoughts if you thought Chachi PT was crazy Auto GPT takes it to the next level chains together llm's thoughts has internet access long and short-term memory access to websites and file storage with Discord we can view and even vote on the tasks it gives using emojis John is using it to create",
            'start': 244.56}, {
            'text': "Virtual Worlds filled with AI agents this is crazy I ran a 100 agent-wide autonomous simulation of a virtual world as part of a research project for forever voices using nothing but Auto GPT and gpt4 in the second video you'll see that it decides on its own to bring forward an economic crisis among our 100 AI personas as part of the virtual world simulation it's kind of like you're having a bunch of Sims but this time they're a lot more advanced so who knows what they're talking about thinking",
            'start': 275.1}, {
            'text': "about and planning to do next David is using in Auto GPT to interact with the blockchain today we signed one of the first ever transactions on the blockchain Via an autonomous AI agent kryptonot GPT is able to understand how to use crypto and send transactions and interact with defy in this example the agent swaps Matic for usdt and here's an interesting one Joshua the CEO of do not pay is using Auto gbt to manage his finances he says that getting a refund",
            'start': 306.24}, {
            'text': "canceling a subscription fighting a credit bureau and many other robot lawyer products should be as simple as texting your friend so he gave Auto GPT access to his bank financial statements credit report and email and according to him he's up so far 217 dollars and 85 cents because Auto GPT is helping him save money and he shows exactly how he did it first using a do not pay plot connection I had it log into every bank account and credit card that I own and",
            'start': 337.56}, {
            'text': "Scan 10 000 Plus transactions it found eighty dollars and eighty six cents leaving my account every month in useless subscriptions and offered to cancel every single one the Bots got to work mailing letters in the case of gyms chatting automatically with agents and even clicking online buttons to get them canceled you see what's possible it can chat with real agents and it can even click around on a website he gives even more details I asked it to scan the same transactions and find me one where I could get an easy refund from my email",
            'start': 367.68}, {
            'text': 'it identified a United Airlines in-flight Wi-Fi receipt for 36.99 from London to New York and then asked me did it work properly when I said no it immediately drafted a persuasive and firm legal letter to United requesting a refund the letter was both legalistic citing FTC statutes and convincing a bot then sent it to them via their website within 48 Hours United agreed to refund the 36.99 he keep keeps going I wanted',
            'start': 397.86}, {
            'text': "to take a break from saving money and ask gpt4 about my credit score using the array API it got my score and Report without advertisements or trying to sell me a credit card I am currently working on several gbt credit disputes and will report back now it was time to unleash gpt4 on my bills I'm a customer of Comcast and so I asked it to negotiate my bill when Comcast offered a 50 discount the bot pushed back it said no I want more and it got 100 back GPT 3.5",
            'start': 429.9}, {
            'text': "never pushed back for what it's worth and he ends it like this I am already up 217.86 in under 24 hours and have a dozen other disputes pending my goal is to have gpt4 make me ten thousand dollars which one's your favorite let me know in the comments and if you're using Auto GPT right now share your thoughts the results your overall experiences whatever you want that's it I'll see you soon",
            'start': 460.16}]
        return YoutubeData(transcript, title, description, ts_transcript_list)


class YoutubeChain():
    @staticmethod
    def run_testing_chain():
        input_1 = """Give me 2 ideas for the summer"""
        # input_1 = """Explain more on the first idea"""
        response_1 = ChatGPTService.predict_no_ui_long_connection(input_1)

        input_2 = """
    For the first idea, suggest some step by step planning for me
        """
        response_2 = ChatGPTService.predict_no_ui_long_connection(input_2, [input_1, response_1])

    @staticmethod
    def test_youtube_classifier(youtube_data: YoutubeData):
        TRANSCRIPT_CHAR_LIMIT = 200  # Because classifer don't need to see the whole transcript
        input_1 = CLASSIFIER_PROMPT.format(title=youtube_data.title, transcript=youtube_data.full_content[:TRANSCRIPT_CHAR_LIMIT]) + CLASSIFIER_PROMPT_TASK
        response_1 = ChatGPTService.predict_no_ui_long_connection(input_1)
        video_type = json.loads(response_1)['type']
        print(f"\nparsed video_type: \n{video_type}")

    @staticmethod
    def test_youtube_timestamped_summary(youtube_data: YoutubeData):
        transcript_with_ts = ""
        for entry in youtube_data.ts_transcript_list:
            transcript_with_ts += f"{int(entry['start'] // 60)}:{int(entry['start'] % 60):02d} {entry['text']}\n"
        input_1 = TIMESTAMPED_SUMMARY_PROMPT.format(title=youtube_data.title, transcript_with_ts=transcript_with_ts) + TIMESTAMPED_SUMMARY_TASK
        response_1 = ChatGPTService.predict_no_ui_long_connection(input_1)
        print(f"\nresponse_1: \n{response_1}")


if __name__ == '__main__':
    # YoutubeChain.run_testing_chain()
    youtube_data: YoutubeData = VideoExample.get_lSTEhG021Jc()
    # YoutubeChain.test_youtube_classifier(youtube_data)
    YoutubeChain.test_youtube_timestamped_summary(youtube_data)

    # converter = Everything2Text4Prompt(openai_api_key="")
    # source_textbox = "youtube"
    # target_source_textbox = "lSTEhG021Jc"
    # text_data, is_success, error_msg = converter.convert_text(source_textbox, target_source_textbox)
    # print(text_data.title)
    # print(text_data.description)
    # print(text_data.full_content)
    # print(text_data.ts_transcript_list)
