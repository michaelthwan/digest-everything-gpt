import os

from digester.gradio_ui_service import GradioUIService
from digester.util import get_config

os.makedirs("analyzer_logs", exist_ok=True)

if __name__ == '__main__':
    config = get_config()
    demo = GradioUIService.get_gradio_ui()
    demo.queue(concurrency_count=config['gradio']['concurrent']).launch(share=True)
