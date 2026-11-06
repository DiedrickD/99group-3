"""Optional text chat interface. Each turn is independent; no chat is persisted."""
import argparse
from lky.chat import Chatbot, render, DISCLOSURE


def build_app(backend="notes"):
    import gradio as gr
    bot = Chatbot(backend=backend)

    def respond(message, history):
        # The history is display-only, avoiding accidental attribution of earlier user claims.
        if not message.strip():
            return "Please enter a question."
        return render(bot.answer(message))

    return gr.ChatInterface(respond, type="messages", title="What Would Lee Kuan Yew Do?",
                            description=DISCLOSURE + f" Backend: {backend}. Each turn is independent.",
                            examples=["Why maintain national reserves?", "Why was English useful as a working language?",
                                      "How might national reserves buffer a crisis in 2026?",
                                      "What speech did Lee give about ChatGPT in 2024?"],
                            analytics_enabled=False).queue(default_concurrency_limit=1, max_size=8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["notes", "base", "lora"], default="notes")
    parser.add_argument("--share", action="store_true", help="Create an explicitly temporary Gradio public link")
    args = parser.parse_args()
    build_app(args.backend).launch(share=args.share, server_name="127.0.0.1", max_threads=4)
