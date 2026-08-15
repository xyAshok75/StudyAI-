from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from openai import OpenAI


# OpenAI client
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


class StudyAI(App):

    def build(self):

        Window.fullscreen = True

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="StudyAI 🤖",
            font_size=32,
            size_hint_y=None,
            height=60
        )

        subtitle = Label(
            text="Your AI Study Assistant",
            font_size=18,
            size_hint_y=None,
            height=40
        )

        self.question = TextInput(
            hint_text="Apna question likho...",
            multiline=True,
            size_hint_y=None,
            height=120
        )

        ask_button = Button(
            text="ASK AI 🤖",
            size_hint_y=None,
            height=60
        )

        self.answer = Label(
            text="AI ka answer yahan dikhega...",
            font_size=18,
            halign="left",
            valign="top"
        )

        self.answer.bind(
            width=lambda instance, value:
            setattr(instance, "text_size", (value, None))
        )

        ask_button.bind(on_press=self.ask_ai)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(self.question)
        layout.add_widget(ask_button)
        layout.add_widget(self.answer)

        return layout


    def ask_ai(self, instance):

        question = self.question.text.strip()

        if not question:
            self.answer.text = "Pehle question likho."
            return

        self.answer.text = "AI soch raha hai... 🤔"

        try:

            response = client.responses.create(
                model="llama-3.1-8b-instant",
                input=(
                    "You are StudyAI, a smart AI study assistant. "
                    "Explain concepts clearly and step-by-step. "
                    "Use simple language suitable for students. "
                    "If the student writes in Hindi or Hinglish, answer in Hindi/Hinglish. "
                    "For numerical questions, show the steps and final answer. "
                    "Be accurate and educational.\n\n" + question
                )
            )

            self.answer.text = response.output_text

        except Exception as e:

            self.answer.text = "Error: " + str(e)


if __name__ == "__main__":
    StudyAI().run()

