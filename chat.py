from tkinter import *
from tkinter import ttk
import os
import threading

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


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

        # GEMINI API
        self.client = None
        self.model_name = None
        self.available_model_names = []

        if genai is not None:

            api_key = os.getenv("GEMINI_API_KEY")

            if api_key:

                try:
                    self.client = genai.Client(
                        api_key=api_key,
                        http_options=types.HttpOptions(timeout=30000)
                    )

                except Exception as e:
                    print("Gemini initialization error:", e)

        # HEADER
        header = Frame(
            self.root,
            bg=self.white,
            bd=1,
            relief=SOLID,
            highlightbackground=self.border,
            highlightthickness=1
        )

        header.place(x=0, y=0, width=1366, height=88)

        face_title = Label(
            header,
            text="FACE RECOGNITION",
            font=("Segoe UI", 27, "bold"),
            bg=self.white,
            fg=self.green,
            anchor="w"
        )

        face_title.place(x=32, y=5, width=500, height=42)

        attendance_title = Label(
            header,
            text="ATTENDANCE SYSTEM",
            font=("Segoe UI", 13, "bold"),
            bg=self.white,
            fg=self.gray,
            anchor="w"
        )

        attendance_title.place(x=34, y=48, width=300, height=25)

        ai_header = Label(
            header,
            text="AI CHATBOT",
            font=("Segoe UI", 18, "bold"),
            bg=self.green,
            fg=self.white,
            bd=2,
            relief=RAISED,
            cursor="hand2"
        )

        ai_header.place(x=1135, y=18, width=190, height=44)

        def ai_header_enter(event):

            ai_header.config(
                bg="#0a9d2d",
                relief=RAISED,
                bd=3
            )

        def ai_header_leave(event):

            ai_header.config(
                bg=self.green,
                relief=RAISED,
                bd=2
            )

        def ai_header_press(event):

            ai_header.config(
                bg=self.dark_green,
                relief=SUNKEN,
                bd=4
            )

        def ai_header_release(event):

            ai_header.config(
                bg="#0a9d2d",
                relief=RAISED,
                bd=3
            )

        ai_header.bind("<Enter>", ai_header_enter)
        ai_header.bind("<Leave>", ai_header_leave)
        ai_header.bind("<ButtonPress-1>", ai_header_press)
        ai_header.bind("<ButtonRelease-1>", ai_header_release)

        # MAIN TITLE
        main_title = Label(
            self.root,
            text="How can we help you?",
            font=("Segoe UI", 25, "bold"),
            bg=self.bg,
            fg=self.text
        )

        main_title.place(x=0, y=105, width=1366, height=45)

        subtitle = Label(
            self.root,
            text="Choose an option below to get assistance with your attendance system.",
            font=("Segoe UI", 11),
            bg=self.bg,
            fg=self.gray
        )

        subtitle.place(x=0, y=150, width=1366, height=30)

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
        footer = Label(
            self.root,
            text="Face Recognition Attendance System  •  AI Chatbot Assistant",
            font=("Segoe UI", 9),
            bg=self.bg,
            fg=self.gray
        )

        footer.place(x=0, y=742, width=1366, height=20)

    # CREATE CARD
    def create_card(
        self, x, y, tag, title, description, button_text, icon
    ):

        card = Frame(
            self.root,
            bg=self.white,
            bd=2,
            relief=RAISED,
            highlightbackground=self.border,
            highlightcolor=self.border,
            highlightthickness=1
        )

        card.place(x=x, y=y, width=570, height=205)

        green_bar = Frame(card, bg=self.green)
        green_bar.place(x=0, y=0, width=7, height=205)

        icon_bg = Frame(
            card,
            bg=self.light_green,
            bd=1,
            relief=SOLID,
            highlightbackground="#c9e8d0",
            highlightthickness=1
        )

        icon_bg.place(x=28, y=25, width=72, height=72)

        icon_label = Label(
            icon_bg,
            text=icon,
            font=("Segoe UI Emoji", 30),
            bg=self.light_green,
            fg=self.green
        )

        icon_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        tag_label = Label(
            card,
            text=tag,
            font=("Segoe UI", 9, "bold"),
            bg=self.white,
            fg=self.green
        )

        tag_label.place(x=125, y=25)

        title_label = Label(
            card,
            text=title,
            font=("Segoe UI", 19, "bold"),
            bg=self.white,
            fg=self.text
        )

        title_label.place(x=125, y=47)

        description_label = Label(
            card,
            text=description,
            font=("Segoe UI", 10),
            bg=self.white,
            fg=self.gray,
            anchor="w"
        )

        description_label.place(x=125, y=80, width=400, height=35)

        action_button = Button(
            card,
            text=button_text,
            font=("Segoe UI", 10, "bold"),
            bg=self.green,
            fg=self.white,
            activebackground=self.dark_green,
            activeforeground=self.white,
            cursor="hand2",
            bd=2,
            relief=RAISED,
            highlightthickness=0,
            padx=18,
            command=lambda: self.open_chatbot(title)
        )

        action_button.place(x=125, y=130, width=145, height=38)

        # CARD HOVER EFFECT
        def card_enter(event):

            card.config(
                bg="#f9fffb",
                relief=RAISED,
                bd=3,
                highlightbackground="#22a447",
                highlightcolor="#22a447",
                highlightthickness=2
            )

            icon_bg.config(
                bg="#d9f4df",
                relief=RAISED,
                bd=2
            )

            icon_label.config(
                bg="#d9f4df",
                fg="#056b1d"
            )

            tag_label.config(
                bg="#f9fffb",
                fg="#056b1d"
            )

            title_label.config(
                bg="#f9fffb",
                fg="#087f23"
            )

            description_label.config(bg="#f9fffb")

            action_button.config(
                bg="#0a9d2d",
                relief=RAISED,
                bd=3
            )

        def card_leave(event):

            card.config(
                bg=self.white,
                relief=RAISED,
                bd=2,
                highlightbackground=self.border,
                highlightcolor=self.border,
                highlightthickness=1
            )

            icon_bg.config(
                bg=self.light_green,
                relief=SOLID,
                bd=1
            )

            icon_label.config(
                bg=self.light_green,
                fg=self.green
            )

            tag_label.config(
                bg=self.white,
                fg=self.green
            )

            title_label.config(
                bg=self.white,
                fg=self.text
            )

            description_label.config(bg=self.white)

            action_button.config(
                bg=self.green,
                relief=RAISED,
                bd=2
            )

        def card_press(event):

            card.config(
                relief=SUNKEN,
                bd=4,
                highlightbackground="#056b1d",
                highlightcolor="#056b1d"
            )

            action_button.config(
                bg=self.dark_green,
                relief=SUNKEN,
                bd=3
            )

        def card_release(event):

            card.config(
                relief=RAISED,
                bd=3,
                highlightbackground="#22a447",
                highlightcolor="#22a447"
            )

            action_button.config(
                bg="#0a9d2d",
                relief=RAISED,
                bd=3
            )

        # CARD EVENTS
        for widget in (
            card, icon_bg, icon_label,
            tag_label, title_label, description_label
        ):

            widget.bind("<Enter>", card_enter)
            widget.bind("<Leave>", card_leave)

        for widget in (card, icon_bg, icon_label):

            widget.bind("<ButtonPress-1>", card_press)
            widget.bind("<ButtonRelease-1>", card_release)

        # BUTTON HOVER
        def button_enter(event):

            if action_button["state"] == NORMAL:

                action_button.config(
                    bg="#0a9d2d",
                    relief=RAISED,
                    bd=3
                )

        def button_leave(event):

            if action_button["state"] == NORMAL:

                action_button.config(
                    bg=self.green,
                    relief=RAISED,
                    bd=2
                )

        def button_press(event):

            if action_button["state"] == NORMAL:

                action_button.config(
                    bg=self.dark_green,
                    relief=SUNKEN,
                    bd=4
                )

        def button_release(event):

            if action_button["state"] == NORMAL:

                action_button.config(
                    bg="#0a9d2d",
                    relief=RAISED,
                    bd=3
                )

        action_button.bind("<Enter>", button_enter)
        action_button.bind("<Leave>", button_leave)
        action_button.bind("<ButtonPress-1>", button_press)
        action_button.bind("<ButtonRelease-1>", button_release)

    # CHATBOT WINDOW
    def open_chatbot(self, mode):

        chat_window = Toplevel(self.root)
        chat_window.geometry("720x650+320+60")
        chat_window.title(mode + " - AI Assistant")
        chat_window.resizable(False, False)
        chat_window.configure(bg=self.bg)
        chat_window.transient(self.root)

        # SEPARATE CONVERSATION FOR EACH WINDOW
        conversation = []

        # CHAT HEADER
        header = Frame(
            chat_window,
            bg=self.green,
            bd=1,
            relief=SOLID
        )

        header.place(x=0, y=0, width=720, height=78)

        status = Label(
            header,
            text="●",
            font=("Segoe UI", 17),
            bg=self.green,
            fg="#9df0af"
        )

        status.place(x=25, y=21)

        ai_title = Label(
            header,
            text="AI Assistant",
            font=("Segoe UI", 19, "bold"),
            bg=self.green,
            fg=self.white
        )

        ai_title.place(x=50, y=13)

        mode_label = Label(
            header,
            text=mode,
            font=("Segoe UI", 9),
            bg=self.green,
            fg="#d8f5de"
        )

        mode_label.place(x=51, y=43)

        # HEADER HOVER
        def chat_header_enter(event):

            header.config(bg="#0a9d2d", relief=RAISED, bd=2)
            status.config(bg="#0a9d2d")
            ai_title.config(bg="#0a9d2d")
            mode_label.config(bg="#0a9d2d")

        def chat_header_leave(event):

            header.config(bg=self.green, relief=SOLID, bd=1)
            status.config(bg=self.green)
            ai_title.config(bg=self.green)
            mode_label.config(bg=self.green)

        header.bind("<Enter>", chat_header_enter)
        header.bind("<Leave>", chat_header_leave)

        # CHAT AREA
        chat_frame = Frame(
            chat_window,
            bg=self.white,
            bd=2,
            relief=SOLID,
            highlightbackground=self.border,
            highlightcolor=self.border,
            highlightthickness=1
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

        # WELCOME MESSAGE
        welcome = (
            "Hello! 👋\n"
            "I am your AI Assistant.\n"
            "Ask me anything about this Face Recognition Attendance System."
        )

        self.add_message(chat_box, "AI Assistant", welcome)

        # INPUT AREA
        input_frame = Frame(chat_window, bg=self.bg)
        input_frame.place(x=20, y=565, width=680, height=55)

        user_entry = Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg=self.white,
            fg=self.text,
            insertbackground=self.green,
            bd=2,
            relief=SOLID,
            highlightthickness=1,
            highlightbackground=self.border,
            highlightcolor=self.green
        )

        user_entry.place(x=0, y=0, width=565, height=45)

        # ENTRY FOCUS EFFECT
        def entry_focus(event):

            user_entry.config(
                bd=2,
                highlightbackground=self.green,
                highlightcolor=self.green
            )

        def entry_unfocus(event):

            user_entry.config(
                bd=2,
                highlightbackground=self.border,
                highlightcolor=self.border
            )

        user_entry.bind("<FocusIn>", entry_focus)
        user_entry.bind("<FocusOut>", entry_unfocus)

        # SEND FUNCTION - RUN API REQUEST IN BACKGROUND
        def send_message(event=None):

            question = user_entry.get().strip()

            if not question:
                return "break"

            self.add_message(chat_box, "You", question)

            user_entry.delete(0, END)
            user_entry.config(state=DISABLED)

            send_button.config(state=DISABLED, text="Thinking...")

            def request_answer():

                try:
                    answer = self.get_ai_answer(
                        question, mode, conversation
                    )

                except Exception as error:
                    answer = f"Chatbot error: {error}"

                # Tkinter widgets must only be updated from the main thread.
                def show_answer():

                    if not chat_window.winfo_exists():
                        return

                    self.add_message(
                        chat_box, "AI Assistant", answer
                    )

                    user_entry.config(state=NORMAL)

                    send_button.config(
                        state=NORMAL,
                        text="Send  ➤"
                    )

                    user_entry.focus()

                try:
                    chat_window.after(0, show_answer)

                except TclError:
                    pass

            threading.Thread(
                target=request_answer,
                daemon=True
            ).start()

            return "break"

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
            bd=2,
            relief=RAISED,
            highlightthickness=0,
            command=send_message
        )

        send_button.place(x=575, y=0, width=105, height=45)

        # SEND BUTTON 3D EFFECT
        def send_enter(event):

            if send_button["state"] == NORMAL:

                send_button.config(
                    bg="#0a9d2d",
                    relief=RAISED,
                    bd=3
                )

        def send_leave(event):

            if send_button["state"] == NORMAL:

                send_button.config(
                    bg=self.green,
                    relief=RAISED,
                    bd=2
                )

        def send_press(event):

            if send_button["state"] == NORMAL:

                send_button.config(
                    bg=self.dark_green,
                    relief=SUNKEN,
                    bd=4
                )

        def send_release(event):

            if send_button["state"] == NORMAL:

                send_button.config(
                    bg="#0a9d2d",
                    relief=RAISED,
                    bd=3
                )

        send_button.bind("<Enter>", send_enter)
        send_button.bind("<Leave>", send_leave)
        send_button.bind("<ButtonPress-1>", send_press)
        send_button.bind("<ButtonRelease-1>", send_release)

        # HELP TEXT
        help_text = Label(
            chat_window,
            text="Press Enter to send",
            font=("Segoe UI", 8),
            bg=self.bg,
            fg=self.gray
        )

        help_text.place(x=20, y=625)

        user_entry.bind("<Return>", send_message)
        user_entry.focus()

    # ADD MESSAGE
    def add_message(self, chat_box, sender, message):

        chat_box.config(state=NORMAL)

        chat_box.insert(
            END,
            sender + "\n",
            "sender"
        )

        chat_box.insert(
            END,
            str(message) + "\n\n",
            "message"
        )

        chat_box.config(state=DISABLED)
        chat_box.see(END)

    # AI ANSWER
    def get_ai_answer(self, question, mode, conversation):

        # API NOT CONFIGURED
        if self.client is None:

            if genai is None:

                return (
                    "Google GenAI package is not installed.\n\n"
                    "Install it using this command:\n"
                    "pip install -U google-genai"
                )

            return (
                "Gemini AI connection is not configured.\n\n"
                "Set your GEMINI_API_KEY environment variable "
                "and restart the application."
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
1. Answer the user's question naturally.
2. Prefer information relevant to this project.
3. If the question is unrelated to the project, politely say that you
   are mainly designed to help with this project, but answer briefly when useful.
4. Do not invent exact file names, database credentials, table structures,
   buttons or implementation details that were not provided.
5. Keep answers clear and practical.
6. For troubleshooting, give step-by-step checks.
7. Understand English, Hindi and Hinglish questions.
8. Do not claim that you performed an action on the user's computer.
"""

        try:

            # CONVERT CHAT HISTORY
            recent_history = conversation[-10:]

            input_messages = []

            for item in recent_history:

                role = (
                    "model"
                    if item.get("role") == "assistant"
                    else "user"
                )

                input_messages.append({
                    "role": role,
                    "parts": [{
                        "text": item.get("content", "")
                    }]
                })

            # ADD CURRENT QUESTION
            input_messages.append({
                "role": "user",
                "parts": [{
                    "text": question
                }]
            })

            # DISCOVER MODELS AVAILABLE TO THIS API KEY
            if not self.model_name:

                available_models = list(
                    self.client.models.list()
                )

                supported_models = []

                for model_info in available_models:

                    full_name = getattr(
                        model_info, "name", ""
                    ) or ""

                    actions = getattr(
                        model_info,
                        "supported_actions",
                        None
                    ) or []

                    if (
                        full_name
                        and (
                            "generateContent" in actions
                            or "generate_content" in actions
                        )
                    ):

                        model_id = full_name.removeprefix("models/")

                        supported_models.append(model_id)

                if not supported_models:

                    raise RuntimeError(
                        "No text-generation models were returned for this API key. "
                        "Check the API key and model access in Google AI Studio."
                    )

                # PREFER FLASH MODELS
                supported_models.sort(
                    key=lambda name: (
                        "flash" not in name.lower(),
                        name.lower()
                    )
                )

                print("\nGemini models available for this API key:")

                for available_name in supported_models:
                    print(" -", available_name)

                self.available_model_names = supported_models

            # TRY AVAILABLE MODELS
            models_to_try = (
                [self.model_name]
                if self.model_name
                else self.available_model_names
            )

            response = None
            last_model_error = None

            for model_id in models_to_try:

                try:

                    print("Trying Gemini model:", model_id)

                    response = self.client.models.generate_content(

                        model=model_id,

                        contents=input_messages,

                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            max_output_tokens=400,
                            temperature=0.4
                        )
                    )

                    self.model_name = model_id

                    print(
                        "Gemini model selected successfully:",
                        model_id
                    )

                    break

                except Exception as model_error:

                    model_error_text = str(model_error).lower()

                    is_model_error = any(
                        term in model_error_text
                        for term in (
                            "not found",
                            "404",
                            "model",
                            "unsupported"
                        )
                    )

                    if self.model_name or not is_model_error:
                        raise

                    last_model_error = model_error

                    print(
                        "Model failed; trying the next available model:",
                        model_error
                    )

            if response is None:

                raise RuntimeError(
                    "None of the models listed for this API key could generate a response. "
                    f"Last model error: {last_model_error}"
                )

            # GET ANSWER
            answer = (response.text or "").strip()

            if not answer:

                answer = (
                    "I couldn't generate an answer. Please try again."
                )

            # SAVE CONVERSATION
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
            lower_error = error_text.lower()

            # AUTHENTICATION ERROR
            if any(term in lower_error for term in (
                "api_key",
                "api key",
                "authentication",
                "unauthenticated",
                "permission denied",
                "401",
                "403"
            )):

                return (
                    "Gemini API authentication failed.\n\n"
                    "Please check your GEMINI_API_KEY and make sure "
                    "the key is valid."
                )

            # QUOTA ERROR
            if any(term in lower_error for term in (
                "quota",
                "billing",
                "resource_exhausted",
                "429"
            )):

                return (
                    "Gemini could not process the request because the "
                    "API quota may be exhausted or the usage limit "
                    "may have been reached.\n\n"
                    "Check your Google AI Studio API usage and limits."
                )

            # NETWORK ERROR
            if any(term in lower_error for term in (
                "connection",
                "network",
                "timeout"
            )):

                return (
                    "I couldn't connect to Gemini.\n\n"
                    "Please check your internet connection and try again."
                )

            # MODEL ERROR
            if any(term in lower_error for term in (
                "not found",
                "404",
                "model"
            )):

                return (
                    "Gemini could not use a model available to this API key.\n\n"
                    "The app checks the models returned by your API key. "
                    "Please check the VS Code Terminal for the available model names "
                    "and the detailed error.\n\n"
                    f"Details: {error_text}"
                )

            return (
                "Sorry, Gemini couldn't process the request right now.\n\n"
                f"Error details: {error_text}"
            )


# MAIN
if __name__ == "__main__":

    root = Tk()

    obj = Chatbot(root)

    root.mainloop()