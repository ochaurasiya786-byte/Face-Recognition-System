from tkinter import *
from tkinter import ttk
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# CHATBOT
class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Attendance System - Chatbot")
        self.root.resizable(False, False)
        self.root.configure(bg="#eef2f5")

        # COLORS
        self.green = "#087f23"
        self.dark_green = "#056b1d"
        self.light_green = "#eaf6ed"
        self.bg = "#eef2f5"
        self.white = "#ffffff"
        self.text = "#202124"
        self.gray = "#6b7280"
        self.border = "#d9dee3"

        # OPENAI
        self.client = None

        if OpenAI is not None:
            api_key = os.getenv("OPENAI_API_KEY")

            if api_key:
                self.client = OpenAI(api_key=api_key)

        # HEADER
        header = Frame(self.root, bg=self.white)
        header.place(x=0, y=0, width=1366, height=88)

        Label(
            header,
            text="FACE RECOGNITION",
            font=("Segoe UI", 27, "bold"),
            bg=self.white,
            fg=self.green,
            anchor="w"
        ).place(x=32, y=5, width=500, height=42)

        Label(
            header,
            text="ATTENDANCE SYSTEM",
            font=("Segoe UI", 13, "bold"),
            bg=self.white,
            fg=self.gray,
            anchor="w"
        ).place(x=34, y=48, width=300, height=25)

        Label(
            header,
            text="AI CHATBOT",
            font=("Segoe UI", 18, "bold"),
            bg=self.green,
            fg=self.white
        ).place(x=1135, y=18, width=190, height=44)

        # MAIN TITLE
        Label(
            self.root,
            text="How can we help you?",
            font=("Segoe UI", 25, "bold"),
            bg=self.bg,
            fg=self.text
        ).place(x=0, y=105, width=1366, height=45)

        Label(
            self.root,
            text="Choose an option below to get assistance with your attendance system.",
            font=("Segoe UI", 11),
            bg=self.bg,
            fg=self.gray
        ).place(x=0, y=150, width=1366, height=30)

        # CARDS
        self.create_card(
            90, 205, "CHAT", "ASK CHATBOT",
            "Ask questions about the complete project.",
            "Open Chatbot", "💬"
        )

        self.create_card(
            705, 205, "STUDENT", "STUDENT HELP",
            "Get help with student details and records.",
            "Student Help", "👨‍🎓"
        )

        self.create_card(
            90, 450, "ATTENDANCE", "ATTENDANCE HELP",
            "Learn how attendance is recorded and managed.",
            "Attendance Help", "📋"
        )

        self.create_card(
            705, 450, "SYSTEM", "SYSTEM HELP",
            "Get assistance with system features and workflow.",
            "System Help", "⚙"
        )

        # FOOTER
        Label(
            self.root,
            text="Face Recognition Attendance System  •  AI Chatbot Assistant",
            font=("Segoe UI", 9),
            bg=self.bg,
            fg=self.gray
        ).place(x=0, y=742, width=1366, height=20)

    # CREATE CARD
    def create_card(self, x, y, tag, title, description, button_text, icon):
        card = Frame(
            self.root,
            bg=self.white,
            bd=1,
            relief=SOLID,
            highlightthickness=0
        )
        card.place(x=x, y=y, width=570, height=205)

        Frame(
            card,
            bg=self.green
        ).place(x=0, y=0, width=7, height=205)

        icon_bg = Frame(
            card,
            bg=self.light_green
        )
        icon_bg.place(x=28, y=25, width=72, height=72)

        Label(
            icon_bg,
            text=icon,
            font=("Segoe UI Emoji", 30),
            bg=self.light_green,
            fg=self.green
        ).place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(
            card,
            text=tag,
            font=("Segoe UI", 9, "bold"),
            bg=self.white,
            fg=self.green
        ).place(x=125, y=25)

        Label(
            card,
            text=title,
            font=("Segoe UI", 19, "bold"),
            bg=self.white,
            fg=self.text
        ).place(x=125, y=47)

        Label(
            card,
            text=description,
            font=("Segoe UI", 10),
            bg=self.white,
            fg=self.gray,
            anchor="w"
        ).place(x=125, y=80, width=400, height=35)

        Button(
            card,
            text=button_text,
            font=("Segoe UI", 10, "bold"),
            bg=self.green,
            fg=self.white,
            activebackground=self.dark_green,
            activeforeground=self.white,
            cursor="hand2",
            bd=0,
            relief=FLAT,
            padx=18,
            command=lambda: self.open_chatbot(title)
        ).place(x=125, y=130, width=145, height=38)

    # CHATBOT WINDOW
    def open_chatbot(self, mode):
        chat_window = Toplevel(self.root)
        chat_window.geometry("720x650+320+60")
        chat_window.title(mode + " - AI Assistant")
        chat_window.resizable(False, False)
        chat_window.configure(bg=self.bg)
        chat_window.transient(self.root)

        # Separate conversation for every chatbot window
        conversation = []

        # CHAT HEADER
        header = Frame(chat_window, bg=self.green)
        header.place(x=0, y=0, width=720, height=78)

        Label(
            header,
            text="●",
            font=("Segoe UI", 17),
            bg=self.green,
            fg="#9df0af"
        ).place(x=25, y=21)

        Label(
            header,
            text="AI Assistant",
            font=("Segoe UI", 19, "bold"),
            bg=self.green,
            fg=self.white
        ).place(x=50, y=13)

        Label(
            header,
            text=mode,
            font=("Segoe UI", 9),
            bg=self.green,
            fg="#d8f5de"
        ).place(x=51, y=43)

        # CHAT AREA
        chat_frame = Frame(
            chat_window,
            bg=self.white,
            bd=1,
            relief=SOLID
        )
        chat_frame.place(x=20, y=95, width=680, height=455)

        scrollbar = ttk.Scrollbar(
            chat_frame,
            orient=VERTICAL
        )
        scrollbar.pack(side=RIGHT, fill=Y)

        chat_box = Text(
            chat_frame,
            font=("Segoe UI", 11),
            bg=self.white,
            fg=self.text,
            bd=0,
            wrap=WORD,
            padx=18,
            pady=15,
            state=DISABLED,
            yscrollcommand=scrollbar.set
        )
        chat_box.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=chat_box.yview)

        chat_box.tag_configure(
            "sender",
            font=("Segoe UI", 9, "bold"),
            foreground=self.green
        )

        chat_box.tag_configure(
            "message",
            font=("Segoe UI", 11),
            foreground=self.text
        )

        # WELCOME
        welcome = (
            "Hello! 👋\n"
            "I am your AI Assistant.\n"
            "Ask me anything about this Face Recognition Attendance System."
        )

        self.add_message(chat_box, "AI Assistant", welcome)

        # INPUT AREA
        input_frame = Frame(
            chat_window,
            bg=self.bg
        )
        input_frame.place(x=20, y=565, width=680, height=55)

        user_entry = Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg=self.white,
            fg=self.text,
            insertbackground=self.green,
            bd=1,
            relief=SOLID
        )
        user_entry.place(x=0, y=0, width=565, height=45)

        # SEND FUNCTION
        def send_message(event=None):
            question = user_entry.get().strip()

            if not question:
                return

            self.add_message(chat_box, "You", question)

            user_entry.delete(0, END)
            user_entry.config(state=DISABLED)

            send_button.config(
                state=DISABLED,
                text="Thinking..."
            )

            chat_window.update_idletasks()

            # AI request
            answer = self.get_ai_answer(
                question,
                mode,
                conversation
            )

            self.add_message(
                chat_box,
                "AI Assistant",
                answer
            )

            user_entry.config(state=NORMAL)

            send_button.config(
                state=NORMAL,
                text="Send  ➤"
            )

            user_entry.focus()

        # SEND BUTTON
        send_button = Button(
            input_frame,
            text="Send  ➤",
            font=("Segoe UI", 10, "bold"),
            bg=self.green,
            fg=self.white,
            activebackground=self.dark_green,
            activeforeground=self.white,
            cursor="hand2",
            bd=0,
            command=send_message
        )

        send_button.place(
            x=575,
            y=0,
            width=105,
            height=45
        )

        Label(
            chat_window,
            text="Press Enter to send",
            font=("Segoe UI", 8),
            bg=self.bg,
            fg=self.gray
        ).place(x=20, y=625)

        user_entry.bind("<Return>", send_message)
        user_entry.focus()

    # ADD MESSAGE
    def add_message(self, chat_box, sender, message):
        chat_box.config(state=NORMAL)

        chat_box.insert(END, sender + "\n", "sender")
        chat_box.insert(END, message + "\n\n", "message")

        chat_box.config(state=DISABLED)
        chat_box.see(END)

    # AI ANSWER
    def get_ai_answer(self, question, mode, conversation):
        # If API is not configured, give a useful local response.
        if self.client is None:
            return (
                "AI connection is not configured yet.\n\n"
                "Please install the OpenAI package and set your "
                "OPENAI_API_KEY environment variable.\n\n"
                "Then restart the application."
            )

        system_instruction = f"""
You are the AI Assistant inside a Face Recognition Attendance System.

Current help section: {mode}

Project context:
- The application is a student management and face-recognition attendance system.
- The GUI is built with Python Tkinter.
- Face processing uses OpenCV.
- Student information can be stored in MySQL.
- Face datasets are collected and trained before recognition.
- A trained classifier can be used for face recognition.
- Attendance can be stored in a CSV file.
- The project may contain Student Management, Dataset, Training,
  Face Recognition, Attendance and Help/Chatbot modules.

Rules:
1. Answer the user's question naturally; do not require an exact predefined question.
2. Prefer information relevant to this project.
3. If the question is unrelated to the project, politely say that you are
   mainly designed to help with this project, but answer briefly when useful.
4. Do not invent exact file names, database credentials, table structures,
   buttons or implementation details that were not provided.
5. Keep answers clear and practical.
6. For troubleshooting, give step-by-step checks.
7. You can understand English, Hindi and Hinglish questions.
8. Do not claim that you performed an action in the user's computer.
"""

        try:
            # Keep the conversation small enough for a desktop chatbot.
            recent_history = conversation[-10:]

            input_messages = []

            for item in recent_history:
                input_messages.append(item)

            input_messages.append({
                "role": "user",
                "content": question
            })

            response = self.client.responses.create(
                model="gpt-5.6-luna",
                instructions=system_instruction,
                input=input_messages,
                max_output_tokens=500
            )

            answer = response.output_text.strip()

            if not answer:
                answer = "I couldn't generate an answer. Please try again."

            conversation.append({
                "role": "user",
                "content": question
            })

            conversation.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        except Exception as e:
            error_text = str(e)

            if "api_key" in error_text.lower() or "authentication" in error_text.lower():
                return (
                    "AI authentication failed.\n\n"
                    "Please check that your OPENAI_API_KEY is correctly "
                    "configured and restart the application."
                )

            if "quota" in error_text.lower() or "billing" in error_text.lower():
                return (
                    "The AI service could not process the request because "
                    "the API account may have no available quota or billing."
                )

            if "connection" in error_text.lower() or "network" in error_text.lower():
                return (
                    "I couldn't connect to the AI service.\n\n"
                    "Please check your internet connection and try again."
                )

            return (
                "Sorry, I couldn't connect to the AI service right now.\n\n"
                "Please try again in a moment."
            )


# MAIN
if __name__ == "__main__":
    root = Tk()
    obj = Chatbot(root)
    root.mainloop()