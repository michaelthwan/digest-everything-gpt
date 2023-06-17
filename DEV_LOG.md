# DEV log

Document interesting findings and journey of text tuning

Without comparison, it is quite difficult to understand quality of different text summarization approach. Of course it is very common in generative AI (like image models).
Therefore during the tuning, it is a good chance to record so for deeper understanding.

## 20230617 Enhancement for timestamp summary

People seems to like shorter version in timestamped summary while maintaining useful keypoints in summary.

Test video: [[Youtube] 8 Surprising Habits That Made Me A Millionaire](https://www.youtube.com/watch?v=IScN1SOcj7A&ab_channel=AliAbdaal)

GPT-model: `gpt-3.5-turbo-16k`

- Previous version, 20 words constraint

```
0:00 - Habits for financial success: multiple streams of income, streams not reliant on trading time for money.
0:32 - Strategic laziness: automating tasks, optimizing time, focusing on outcomes.
1:03 - Developing an entrepreneurial mindset: identifying problems and finding solutions.
2:03 - Applying strategic laziness to business: focusing on the end goal and avoiding unnecessary tasks.
3:06 - Growth mindset: believing that everything is figureoutable.
4:39 - The power of networking: making friends in real life and online, utilizing Twitter.
6:10 - The importance of reading: gaining wisdom and knowledge from books.
8:16 - Acquiring financial literacy: taking control of your financial life and understanding money
```

- Tuning attempt #1: 10 words constraint

```
0:00 - Introduction to habits that helped the speaker become a millionaire.
0:32 - Mindset shift: Millionaires rely on multiple streams of income.
1:03 - Strategic laziness: Optimizing time and automating tasks.
1:33 - Being strategic about goals and outcomes.
2:03 - Applying strategic laziness to business and focusing on what really matters.
2:36 - Developing an entrepreneurial diagnostic mindset to identify problems and solutions.
3:06 - Recognizing problems in everyday life as potential business ideas.
4:08 - Embracing a growth mindset: Everything is figureoutable.
4:39 - Accelerating learning by asking the right people for help.
5:10 - The importance of making friends and networking both in real life and online.
6:10 - Leveraging the power of Twitter to connect with like-minded individuals and improve business growth.
7:13 - The benefits of reading books and gaining wisdom from successful individuals.
8:47 - Making financial literacy a priority to understand money management and investments
```

- Tuning attempt #2: 8 words constraint (work better well)

```
0:00 - Introduction to habits for becoming a millionaire
0:32 - Mindset shift: multiple income streams are key
1:03 - Embrace strategic laziness to optimize time
1:33 - Focus on the outcome and efficient tasks
2:03 - Entrepreneurial mindset: identify problems and solutions
2:36 - Embrace growth mindset: everything is figureoutable
3:06 - Learn from the right people, ask for help
3:37 - Making friends and networking on Twitter
4:08 - Value of reading books and acquiring wisdom
5:10 - Financial literacy is essential for success
```

Let's further squeeze for fun

- Tuning attempt #3: 5 words constraint (work better well)

```
0:00 - Mindset shift for financial success
0:32 - Strategic laziness and time optimization
1:03 - Develop an entrepreneurial diagnostic mindset
1:33 - Having a growth mindset
2:03 - Being strategically lazy in achieving goals
2:36 - Recognizing problems and creating solutions
3:06 - Everything is figureoutable
4:39 - Asking the right people for help
5:10 - Making friends in real life and on the internet
6:10 - Reading books for wisdom and knowledge
9:19 - Acquiring financial literacy for success
```

- Tuning attempt #4: 3 words constraint (work better well)
  For some reason it didn't listen to you now

```
0:00 - Financial success requires multiple streams of income.
0:32 - Strategic laziness optimizes time and productivity.
1:33 - Be strategically lazy and focus on the end goal.
2:03 - Approach business strategically and avoid wasting time.
3:06 - Develop an entrepreneurial mindset and identify problems to solve.
4:39 - Embrace a growth mindset and believe that everything is figureoutable.
5:40 - Leverage your network and seek help from the right people.
6:42 - Build both real-life and internet friendships, especially on Twitter.
7:44 - Reading books accelerates learning and provides valuable wisdom.
9:51 - Acquire financial literacy and take control of your financial life
```

## 20230617 Enhancement for summary

Not concise enough

Original

```
Summary:
- This video discusses the challenges faced by individuals with ADHD in terms of organization, focus, and productivity.
- It emphasizes the importance of understanding and supporting ADHD individuals rather than labeling them negatively.
- The video provides strategies to manage ADHD symptoms, such as establishing connections, setting measurable goals, creating a structured environment, prioritizing quality sleep, engaging in regular exercise, and achieving a flow state.
- It highlights how the right support and guidance can transform ADHD from a hindrance to an asset, enabling individuals to achieve success and fulfillment.
- The video discusses the gender disparities in the diagnosis of ADHD, particularly among females.
- It points out that females tend to be the most undiagnosed group due to their symptoms not including hyperactivity or disruption.
- The video emphasizes that understanding these distinctions helps to break down the myths and stigma associated with ADHD.
- It notes that ADHD is not an inability or disability but rather a different way of thinking, with the potential for extraordinary achievements.
- The video encourages individuals with ADHD to embrace their creative and energetic nature, as well as their entrepreneurial spirit, and embrace challenges.
- It stresses the importance of having the right tools and support in place to harness the power of one’s brain and reach their full potential.
- The video aims to provide guidance on managing ADHD and concludes by expressing a hope for viewers to utilize their own brilliance to make the world a better place.
```


- Tuning attempt #1: Formatted with summary, highlight. Unconstrainted content

```
Summary:
This video discusses eight surprising habits that helped the speaker become a millionaire. The habits include having multiple streams of income, embracing strategic laziness, developing an entrepreneurial mindset, adopting a growth mindset, seeking help from the right people, making friends in real life and on the internet, reading a lot of books, and acquiring financial literacy.

Highlights:
- Having multiple streams of income and not relying solely on a day job is key to financial success.
- Strategic laziness involves optimizing time and automating tasks to work smarter, not harder.
- Developing an entrepreneurial mindset means identifying problems and finding solutions.
- Adopting a growth mindset and believing that everything is figureoutable can lead to success.
- Seeking help from the right people and networking is important for accelerating learning and growth.
- Making friends in real life and online, particularly through Twitter, can lead to valuable connections and opportunities.
- Reading books is essential for gaining wisdom and accelerating personal development.
- Acquiring financial literacy is crucial for understanding saving, investing, and how money works
```

- Tuning attempt #2: Formatted with summary, highlight. Constrainted content (5 bullet points, <20 words)

```
Summary: The video discusses eight surprising habits that helped the speaker become a millionaire, including having multiple streams of income, being strategically lazy to save time, developing an entrepreneurial and growth mindset, seeking help from the right people, making connections on Twitter, reading books, and acquiring financial literacy.

Highlights:
- Multiple streams of income and avoiding reliance on a day job are crucial for financial success.
- Strategic laziness involves optimizing time and automating tasks to increase productivity.
- An entrepreneurial mindset involves identifying problems and creating solutions.
- Having a growth mindset and believing everything is figureoutable can overcome obstacles.
- Networking and making connections on Twitter can lead to valuable opportunities
```


- Tuning attempt #3: Formatted with summary, highlight. Constrainted content (5 bullet points, <20 words). add Emoji

```
Summary: The video discusses eight surprising habits that helped the speaker become a millionaire. These habits include having multiple streams of income, strategic time management, an entrepreneurial mindset, a growth mindset, seeking help from others, making connections online, extensive reading, and financial literacy.

Highlights:
- 💰 Most millionaires have multiple streams of income, not reliant on trading time for money.
- ⏰ Being strategic with time and automating processes can save valuable time.
- 🚀 Developing an entrepreneurial mindset involves identifying and solving problems for profit.
- 🌱 Adopting a growth mindset and believing everything is figureoutable helps overcome obstacles.
- 🤝 Leveraging the support and knowledge of others can accelerate success.
```

