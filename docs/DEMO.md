# Temporary live text chat

**Try the trained adapter with RAG:**
[Open the live chatbot](https://3baba5f3e0cf4f2513.gradio.live).

Created and tested on **6 November 2026**. An unauthenticated HTTP request and
a real `/chat` request succeeded; the recorded response is in
[`reports/demo-verification.json`](../reports/demo-verification.json).

This is a temporary Gradio share link. Gradio reports a maximum tunnel lifetime
of one week, and it can stop sooner if the local server exits, this computer
sleeps, or connectivity changes. It is not permanent hosting.

For a permanent review link, use [the recorded chat examples](CHAT_EXAMPLES.md).
To create a new temporary demo on a GPU, use the final cell of the
[Colab notebook](https://colab.research.google.com/github/DiedrickD/99group-3/blob/main/notebooks/train_colab.ipynb).

This experimental 0.5B adapter can make factual errors despite valid citations;
[the quality review](QUALITY_REVIEW.md) documents observed failures. Replies
are historical reconstructions, not authentic quotations. Each turn is independent.
