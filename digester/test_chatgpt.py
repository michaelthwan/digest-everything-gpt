from chatgpt_service import ChatGPTService
from everything2text4prompt.everything2text4prompt import Everything2Text4Prompt
from everything2text4prompt.util import BaseData, YoutubeData, PodcastData
from gradio_method_service import YoutubeChain, GradioInputs
from digester.util import get_config, Prompt

import json

if __name__ == '__main__':
    config = get_config()
    api_key = config.get("openai").get("api_key")
    assert api_key

    gradio_inputs = GradioInputs(apikey_textbox=api_key, source_textbox="", source_target_textbox="", qa_textbox="", chatbot=[], history=[])
    prompt_str = """
[[[[[INPUT]]]]]

[TITLE]
8 Surprising Habits That Made Me A Millionaire

[Transcript with timestamp]
6:42 "Hey, let's do everything ourselves." That brings us on to habit number six which is to make friends
with people in real life and more importantly,
well, not more importantly, but additionally, on the internet. And the single best way I find
for doing this is Twitter. Twitter is an incredible,
incredible, incredible invention that you can use to make friends with people all around the world. And the nice thing about Twitter is that it's different to Instagram. Instagram is very sort of visual and based on posting pretty pictures, but Twitter is very much
based on sharing good ideas. And if you are sharing interesting ideas and you're connecting with other people who are sharing those similar ideas, that automatically leads you
7:13 to kind of becoming internet friends, and then they follow you, you follow them, you chat a little bit in the DMs. And over the last year, I've
met up with so many people who I initially met on Twitter. And I've got friends all around the world who I've never ever met in real life, but we've talked on Twitter. We know we liked the same stuff. We share the same ideas. And, A, this just makes
life much more fun. But if we're talking about habits to get to becoming a millionaire, I can point to lots of
these different connections that have really accelerated
the growth of my business. For example, me and my mate Thomas Frank became friends on Twitter
like two weeks ago. Thomas Frank then
introduced me to Standard
7:44 which is the YouTuber
agency that I'm now part of and that completely changed
the game for my business. Secondly, there's two chaps,
Tiago Forte and David Perell who run their own online courses. We became friends on Twitter
after I took their courses and started engaging with them on Twitter. And then I DMed them when I wanted help for my own Part-Time YouTuber Academy and they really helped with that. And again, that really accelerated the growth of the business to becoming a $2 million business. And when it comes to this
making friends thing, it's one of those things
that's very hard to like, if you make friends with someone,
then it will lead to this. It's more like you have
this general habit, this general attitude
towards making friends with whoever shares the same ideas as you
8:16 and just generally trying to
be a nice and helpful person, and you know that, eventually, that'll lead to really interesting things happening in your life
further down the line. On a somewhat related note, habit number seven is reading a lot. And just like we can get
wisdom from our real life and our internet friends via Twitter, we can get a lot more wisdom from people who have
written books about stuff. You know, if you speak to anyone who's successful in almost any way, they will almost always say
that they read a lot of books. And they will also almost always say that everyone else that
they know who's successful also reads a lot of books.
8:47 So if you're telling yourself,
"I don't have time to read," then you're kind of screwing yourself because (laughs) basically
every millionaire you ask will have spent tonnes and
tonnes of time reading books. And again, the great thing about books is that you've got five,
10, 20 years of experience that someone has boiled down to a thing that takes you
a few hours to read. Like Tim Ferriss was doing
the entrepreneurial thing for 10 years before he wrote the book. That's pretty sick. That's 10 years of wisdom that
you can read in a few hours. And if you read lots of books
of this or entrepreneurship, like business, finance,
9:19 basically anything you're interested in, you can just get a huge
amount of value from them. And it doesn't really cost very much. You can find PDFs on the internet for free if you're really averse
to paying for books if that's your vibe. And it's just such a great way
to accelerate your learning in almost anything. If you didn't know, I
am also writing a book, which is probably gonna
come out in two years' time. But I'll put a link to my
book mailing list newsletter, which is where I share my book journey and what it's like to
write and research a book and sample chapters and getting the audience's
opinion and stuff. So that'll be linked in
the video description if you wanna check it out. And finally, habit number eight
for becoming a millionaire is to acquire financial literacy.
9:51 Now, this is one of those things that no one teaches us in
school or university or college, but it's just one of those things that you have to learn for yourself. And you can get it through reading books, such as, for example, this book, oh crap, "The Psychology of
Money" by Morgan Housel, which is now a little bit dilapidated. I read this recently. It's
really, really, really good. 20 bite-sized lessons about money. Gonna make a video about that. But also just generally
taking your financial life into your own hands. I know so many people who have sort of relegated their financial
life to, you know, "Oh, it's just something that
the government will sort out."
10:22 Or "Oh, you know, my hospital "will figure out what taxes I need to pay "and then I'll just kind
of do it from there." Money is such an important part of life. It's one of the biggest sources
of stress in anyone's life if you don't have much of it. And so much of our life is
spent in the pursuit of money and financial freedom,
financial independence, that if we don't have financial literacy, if we don't understand the
basics of saving or investing or how the stock market
works or how taxes work, any of that kind of stuff, again, we are just screwing ourselves. Because if you wanna become a millionaire you have to have some
level of financial literacy to know what it takes
to become a millionaire and how that might actually work.
10:53 So recommend reading a book like "The Psychology of
Money by Morgan Housel. Or, if you like, you can check
out this video over here, which is my ultimate guide to investing in stocks and shares. That's like a half an
hour-long crash course on everything you need
to know about investing. If you don't know about investing definitely check out that video. Thank you so much for watching. Hope you found this video useful. And I will see you in
the next one. Bye-bye.


[TASK]
Convert this into youtube summary. 
Separate for 2-5minutes chunk, maximum 20 words for one line.
Start with the timestamp followed by the summarized text for that chunk.
Example format:
6:42 - This is the first part
8:00 - This is the second part
9:22 - This is the third part
    """
    GPT_MODEL = "gpt-3.5-turbo-16k"
    ChatGPTService.single_rest_call_chatgpt(api_key, prompt_str, GPT_MODEL)
