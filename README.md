# DigestEverythingGPT

DigestEverythingGPT provides world-class content summarization/query tool that leverages ChatGPT/LLMs to help users
quickly understand essential information from various forms of content, such as podcasts, YouTube videos, and PDF
documents.

The prompt engineering is **chained and tuned** so that is result is of high quality and fast. It is not a simple single
query and response tool.

# Showcases

**Example of summary**

- "OpenAssistant RELEASED! The world's best open-source Chat AI!" (https://www.youtube.com/watch?v=ddG2fM9i4Kk)

![final_full_summary](/img/final_full_summary.png)

**DigestEverythingGPT's final output will adopt to video type.**

- For example, for the video "17 cheap purchases that save me
  time" (https://www.youtube.com/watch?v=f7Lfukf0IKY&t=3s&ab_channel=AliAbdaal)

- it shown the summary with and specific 17 things correctly.

![n_things_example](/img/n_things_example.png)

**LLM Loading in progress screen - chained prompt engineering, batched inference, etc.**

![in_process](/img/in_process.png)

**Support for multiple languages** regardless of video language

![multi_language](/img/multi_language.png)

# Live website

[TODO]

# Features

- **Content Summarization**:
    - Automatically generate concise summaries of various types of content, allowing users to save time and make
      informed decisions for in-depth engagement.
    - Chained/Batched/Advanced prompt engineering for great quality/faster results.
- **Interactive "Ask" Feature** (in progress):
    - Users can pose questions to the tool and receive answers extracted from specific sections within the full content.
- **Cross-Medium Support**:
    - DigestEverythingGPT is designed to work with a wide range of content mediums.
    - Currently, the tool supports
        - YouTube videos [beta]
        - podcasts (in progress)
        - PDF documents (in progress)

# Installation

Use python 3.10+ (tested in 3.10.8). Install using requirement.txt then launch gradio UI using main.py

```
pip install -r requirements.txt
python main.py
```

# License

DigestEverything-GPT is licensed under the MIT License.

