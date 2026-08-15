import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from context import TWIN_SYSTEM_PROMPT
from styles import CSS, EXAMPLES, JS
from tools import handle_tool_calls, tools

load_dotenv(override=True)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4-mini")

# Stops a misbehaving model from looping on tool calls forever.
MAX_TOOL_ROUNDS = 5

openai = OpenAI()

SYSTEM = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    messages = SYSTEM + history + [{"role": "user", "content": message}]

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            response = openai.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
            )
            choice = response.choices[0]

            if choice.finish_reason != "tool_calls":
                return choice.message.content

            # The assistant turn that requested the tools has to go back into
            # the history, otherwise the tool results have nothing to attach to.
            messages.append(choice.message)
            messages.extend(handle_tool_calls(choice.message.tool_calls))

        return "Sorry, I got stuck in a loop there. Mind asking that again?"

    except OpenAIError as exc:
        print(f"[openai error] {exc}", flush=True)
        return "Something broke on my end talking to the model. Try again in a moment?"


if __name__ == "__main__":
    demo = gr.ChatInterface(
        chat,
        chatbot=gr.Chatbot(show_label=False, height=520, elem_id="dt-chatbot"),
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI Twin about my career",
    )

    demo.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        # Render assigns a port and expects the process to bind 0.0.0.0.
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
        # Render's Python runtime has no Node, so Gradio's SSR can't start.
        ssr_mode=False,
    )
