import os
import threading
import time
import webbrowser

from digester.gradio_ui_service import GradioUIService
from digester.util import get_config

os.makedirs("analyzer_logs", exist_ok=True)


def opentab_with_delay(port):
    def open():
        time.sleep(2)
        webbrowser.open_new_tab(f"http://localhost:{port}/?__theme=dark")

    threading.Thread(target=open, name="open-browser", daemon=True).start()


if __name__ == '__main__':
    config = get_config()
    port = config["gradio"]["port"]
    opentab_with_delay(port)
    demo = GradioUIService.get_gradio_ui()
    demo.queue(concurrency_count=config['gradio']['concurrent']).launch(
        server_name="0.0.0.0", server_port=port,
        share=True
    )
