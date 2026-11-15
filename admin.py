
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
import json
import html
import secrets
import threading
import smtplib
import ssl
import shutil

from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, render_template_string
from werkzeug.serving import make_server

from approval_service import (
    send_approval_email,
    get_base_url,
    process_approval_action,
    generate_action_token
)


class Admin:

    def __init__(self, root, login_success_callback=None):

        self.root = root
        self.login_success_callback = login_success_callback

        self.root.geometry("1100x600+200+100")
        self.root.title("Admin Login")
        self.root.resizable(False, False)

        # LOAD CONFIGURATION
        self.base_dir = Path(__file__).resolve().parent
        load_dotenv(self.base_dir / ".env")

        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "student")
        }

        # GMAIL CONFIGURATION
        self.admin_email = os.getenv(
            "ADMIN_EMAIL", "ochaurasiya786@gmail.com"
        )

        self.smtp_email = os.getenv(
            "SMTP_EMAIL", self.admin_email
        )

        self.smtp_app_password = os.getenv(
            "SMTP_APP_PASSWORD", ""
        )

        # NGROK CONFIGURATION
        self.ngrok_auth_token = os.getenv(
            "NGROK_AUTHTOKEN", ""
        )

        self.ngrok_path = os.getenv(
            "NGROK_PATH", ""
        ).strip().strip('"')

        self.web_port = int(
            os.getenv("WEB_ACTION_PORT", "5000")
        )

        self.poll_seconds = max(
            15, int(os.getenv("POLL_SECONDS", "30"))
        )

        self.public_base_url = None
        self.web_server = None
        self.ngrok_tunnel = None
        self.web_app = None
        self.ngrok_module = None
        self.pyngrok_config = None

        self.web_tokens = {}
        self.web_tokens_lock = threading.Lock()

        self.notification_lock = threading.Lock()
        self.notification_in_progress = set()

        self.polling_active = True
        self.polling_after_id = None

        self.notified_file = (
            self.base_dir / "gmail_notified_requests.json"
        )

        self.notified_request_ids = self._load_notified_ids()

        # DATABASE CONNECTION
        try:

            self.conn = mysql.connector.connect(
                **self.db_config
            )

            self.my_cursor = self.conn.cursor()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to connect with MySQL.\n\n{e}",
                parent=self.root
            )

            self.root.destroy()
            return

        # START WEB ACTION SERVER
        self._start_web_action_server()

        # ADMIN LOGIN
        self.admin_login_screen()

        # CLOSE WINDOW
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # LOAD NOTIFIED REQUEST IDS
    def _load_notified_ids(self):

        try:

            if self.notified_file.exists():

                data = json.loads(
                    self.notified_file.read_text(
                        encoding="utf-8"
                    )
                )

                return set(int(value) for value in data)

        except Exception as e:

            print("Notification history error:", e)

        return set()

    # SAVE NOTIFICATION HISTORY
    def _save_notified_ids(self):

        try:

            self.notified_file.write_text(
                json.dumps(
                    sorted(self.notified_request_ids),
                    indent=2
                ),
                encoding="utf-8"
            )

        except Exception as e:

            print("Unable to save notification history:", e)

    # CONFIGURE WEB ACTION LISTENER / SERVER
    def _start_web_action_server(self):
        # 1. Check if Cloud Backend BASE_URL is configured (e.g. Render hosting)
        configured_url = os.getenv("BASE_URL") or os.getenv("RENDER_EXTERNAL_URL")
        if configured_url:
            self.public_base_url = configured_url.strip().rstrip("/")
            print(f"Admin Panel using Cloud Backend URL for approval links: {self.public_base_url}")
            return

        # 2. Check if local backend port is set
        local_backend_url = f"http://127.0.0.1:{self.web_port}"

        # 3. Optional Ngrok tunnel for local testing
        if self.ngrok_auth_token:
            try:
                from pyngrok import ngrok
                from pyngrok.conf import PyngrokConfig

                self.ngrok_module = ngrok
                ngrok_exe = self.ngrok_path or shutil.which("ngrok")
                if ngrok_exe and Path(ngrok_exe).is_file():
                    self.pyngrok_config = PyngrokConfig(ngrok_path=str(ngrok_exe))
                    ngrok.set_auth_token(
                        self.ngrok_auth_token,
                        pyngrok_config=self.pyngrok_config
                    )
                    self.ngrok_tunnel = ngrok.connect(
                        addr=self.web_port,
                        proto="http",
                        pyngrok_config=self.pyngrok_config
                    )
                    self.public_base_url = self.ngrok_tunnel.public_url.rstrip("/")
                    print(f"Ngrok tunnel connected: {self.public_base_url}")
                    return
            except Exception as e:
                print(f"Ngrok connection skipped ({e}). Falling back to local backend URL.")

        self.public_base_url = local_backend_url
        print(f"Admin Panel using backend URL: {self.public_base_url}")

    # CREATE SIGNED ACTION LINK
    def _create_web_action_link(self, request_id, action_name):
        base_url = self.public_base_url or get_base_url()
        token = generate_action_token(request_id, action_name)
        return (f"{base_url}/action/{token}", token)

    # SEND EMAIL NOTIFICATION FOR NEW REQUESTS
    def _notify_new_requests(self, rows):

        if not self.public_base_url:
            return

        if not self.smtp_app_password:
            return

        for row in rows:

            request_id = int(row[0])

            with self.notification_lock:

                if (
                    request_id in self.notified_request_ids
                    or request_id in self.notification_in_progress
                ):
                    continue

                self.notification_in_progress.add(request_id)

            threading.Thread(
                target=self._send_request_email,
                args=(row,),
                daemon=True
            ).start()

    # SEND GMAIL
    def _send_request_email(self, row):

        request_id = int(row[0])

        try:
            base_url = self.public_base_url or get_base_url()
            success, msg = send_approval_email(
                row,
                base_url=base_url,
                admin_email=self.admin_email,
                smtp_email=self.smtp_email,
                smtp_app_password=self.smtp_app_password
            )

            if success:
                with self.notification_lock:
                    self.notified_request_ids.add(request_id)
                    self._save_notified_ids()
                print(f"Approval email sent for request #{request_id}")
            else:
                print(f"Failed to email request #{request_id}: {msg}")

        except Exception as e:
            print(f"Could not email request #{request_id}: {e}")

        finally:
            with self.notification_lock:
                self.notification_in_progress.discard(request_id)

    # PROCESS WEB APPROVE / REJECT
    def _process_web_request(self, request_id, action_name):
        res = process_approval_action(request_id, action_name, self.db_config)
        if not res.get("success"):
            raise ValueError(res.get("message", "Action failed"))
        return res.get("message", "Action completed")

    # AUTOMATIC POLLING
    def _schedule_polling(self):

        if not self.polling_active:
            return

        try:

            self.polling_after_id = self.root.after(
                self.poll_seconds * 1000,
                self._poll_pending_requests
            )

        except Exception:

            pass

    def _poll_pending_requests(self):

        try:

            if (
                self.polling_active
                and hasattr(self, "student_table")
                and self.student_table.winfo_exists()
            ):

                self.fetch_requests()

        except Exception as e:

            print("Automatic refresh error:", e)

        self._schedule_polling()

    # ADMIN LOGIN SCREEN
    def admin_login_screen(self):

        self.login_frame = Frame(self.root)
        self.login_frame.pack(expand=True)

        title = Label(
            self.login_frame,
            text="ADMIN LOGIN",
            font=("times new roman", 28, "bold")
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=30
        )

        Label(
            self.login_frame,
            text="Username",
            font=("times new roman", 16, "bold")
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=15
        )

        self.username_entry = Entry(
            self.login_frame,
            font=("times new roman", 15),
            width=25
        )

        self.username_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=15
        )

        Label(
            self.login_frame,
            text="Password",
            font=("times new roman", 16, "bold")
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=15
        )

        self.password_entry = Entry(
            self.login_frame,
            font=("times new roman", 15),
            width=25,
            show="*"
        )

        self.password_entry.grid(
            row=2,
            column=1,
            padx=15,
            pady=15
        )

        login_btn = Button(
            self.login_frame,
            text="LOGIN",
            command=self.admin_login,
            width=18,
            font=("times new roman", 14, "bold"),
            bg="#4f81bd",
            fg="white",
            activebackground="#3d6fa8",
            activeforeground="white",
            cursor="hand2"
        )

        login_btn.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=25
        )

        self.username_entry.focus()

    # CHECK ADMIN LOGIN
    def admin_login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:

            messagebox.showerror(
                "Error",
                "Please enter username.",
                parent=self.root
            )
            return

        if not password:

            messagebox.showerror(
                "Error",
                "Please enter password.",
                parent=self.root
            )
            return

        try:

            self.my_cursor.execute(
                """
                SELECT Admin_ID
                FROM admin
                WHERE Username=%s
                AND Password=%s
                """,
                (username, password)
            )

            admin = self.my_cursor.fetchone()

            if admin:

                self.login_frame.destroy()
                self.approval_panel()

                if self.login_success_callback:

                    try:
                        self.login_success_callback()
                    except Exception as e:
                        print("Login callback error:", e)

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid Admin Username or Password.",
                    parent=self.root
                )

                self.password_entry.delete(0, END)

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to verify admin.\n\n{e}",
                parent=self.root
            )

    # ADMIN APPROVAL PANEL
    def approval_panel(self):

        self.root.title("Admin Approval Panel")

        title = Label(
            self.root,
            text="STUDENT REGISTRATION APPROVAL",
            font=("times new roman", 25, "bold")
        )

        title.pack(pady=20)

        frame = Frame(self.root)

        frame.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "Request_ID",
            "Student_ID",
            "Student_Name",
            "Dep",
            "Course",
            "Year",
            "Semester",
            "Roll",
            "Status"
        )

        self.student_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        for col in columns:

            self.student_table.heading(
                col,
                text=col
            )

        widths = {
            "Request_ID": 90,
            "Student_ID": 100,
            "Student_Name": 150,
            "Dep": 120,
            "Course": 100,
            "Year": 100,
            "Semester": 100,
            "Roll": 100,
            "Status": 100
        }

        for col, width in widths.items():

            self.student_table.column(
                col,
                width=width,
                anchor=CENTER
            )

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#cfe2f3")],
            foreground=[("selected", "black")]
        )

        self.student_table.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient=VERTICAL,
            command=self.student_table.yview
        )

        scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        self.student_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.student_table.bind(
            "<<TreeviewSelect>>",
            self.on_row_select
        )

        button_frame = Frame(self.root)
        button_frame.pack(pady=15)

        approve_btn = Button(
            button_frame,
            text="APPROVE",
            command=self.approve_student,
            width=15,
            font=("times new roman", 13, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#388E3C",
            activeforeground="white",
            cursor="hand2"
        )

        approve_btn.grid(row=0, column=0, padx=10)

        reject_btn = Button(
            button_frame,
            text="REJECT",
            command=self.reject_student,
            width=15,
            font=("times new roman", 13, "bold"),
            bg="#f44336",
            fg="white",
            activebackground="#c62828",
            activeforeground="white",
            cursor="hand2"
        )

        reject_btn.grid(row=0, column=1, padx=10)

        refresh_btn = Button(
            button_frame,
            text="REFRESH",
            command=self.fetch_requests,
            width=15,
            font=("times new roman", 13, "bold"),
            bg="#4f81bd",
            fg="white",
            activebackground="#3d6fa8",
            activeforeground="white",
            cursor="hand2"
        )

        refresh_btn.grid(row=0, column=2, padx=10)

        logout_btn = Button(
            button_frame,
            text="LOGOUT",
            command=self.logout,
            width=15,
            font=("times new roman", 13, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            cursor="hand2"
        )

        logout_btn.grid(row=0, column=3, padx=10)

        self.fetch_requests()
        self._schedule_polling()

    # ROW SELECT
    def on_row_select(self, event=None):

        selected = self.student_table.selection()

        if selected:

            item = self.student_table.item(selected[0])
            values = item.get("values")

            if values:

                print(
                    "Selected Request ID:",
                    values[0]
                )

    # FETCH PENDING REQUESTS
    def fetch_requests(self):

        if not hasattr(self, "student_table"):
            return

        try:

            for item in self.student_table.get_children():

                self.student_table.delete(item)

            self.my_cursor.execute(
                """
                SELECT
                    Request_ID,
                    Student_ID,
                    Student_Name,
                    Dep,
                    Course,
                    Year,
                    Semester,
                    Roll,
                    Status
                FROM student_requests
                WHERE Status='Pending'
                ORDER BY Request_ID DESC
                """
            )

            rows = self.my_cursor.fetchall()

            self._notify_new_requests(rows)

            for row in rows:

                self.student_table.insert(
                    "",
                    END,
                    values=row
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to fetch requests.\n\n{e}",
                parent=self.root
            )

    # GET SELECTED REQUEST
    def get_selected_request(self):

        selected = self.student_table.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a student request.",
                parent=self.root
            )

            return None

        item = self.student_table.item(selected[0])
        values = item.get("values")

        if not values:

            messagebox.showerror(
                "Error",
                "Invalid student request selected.",
                parent=self.root
            )

            return None

        return values[0]

    # APPROVE STUDENT
    def approve_student(self):

        request_id = self.get_selected_request()

        if request_id is None:
            return

        connection = None
        cursor = None

        try:

            connection = mysql.connector.connect(
                **self.db_config
            )

            connection.start_transaction()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Dep, Course, Year, Semester,
                       Student_ID, Student_Name, Division,
                       Roll, Gender, DOB, Email, Phone,
                       Address, Teacher, PhotoSample
                FROM student_requests
                WHERE Request_ID=%s
                AND Status='Pending'
                FOR UPDATE
                """,
                (request_id,)
            )

            student = cursor.fetchone()

            if not student:

                raise ValueError(
                    "Request not found or already processed."
                )

            student_id = student[4]

            cursor.execute(
                """
                SELECT Student_ID
                FROM student
                WHERE Student_ID=%s
                """,
                (student_id,)
            )

            if cursor.fetchone():

                raise ValueError(
                    "This Student ID already exists."
                )

            confirm = messagebox.askyesno(
                "Approve Student",
                f"Do you want to approve this student?\n\n"
                f"Student ID: {student_id}\n"
                f"Student Name: {student[5]}",
                parent=self.root
            )

            if not confirm:

                connection.rollback()
                return

            cursor.execute(
                """
                INSERT INTO student
                (
                    Dep, Course, Year, Semester,
                    Student_ID, Student_Name, Division,
                    Roll, Gender, DOB, Email, Phone,
                    Address, Teacher, PhotoSample
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                 %s,%s,%s,%s,%s)
                """,
                student
            )

            cursor.execute(
                """
                UPDATE student_requests
                SET Status='Approved'
                WHERE Request_ID=%s
                AND Status='Pending'
                """,
                (request_id,)
            )

            if cursor.rowcount != 1:

                raise ValueError(
                    "Request already processed."
                )

            connection.commit()

            messagebox.showinfo(
                "Approved",
                "Student registration approved successfully.\n\n"
                "The student is now available in the Student table.",
                parent=self.root
            )

            self.fetch_requests()

        except mysql.connector.Error as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to approve student.\n\n{e}",
                parent=self.root
            )

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Error",
                str(e),
                parent=self.root
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # REJECT STUDENT
    def reject_student(self):

        request_id = self.get_selected_request()

        if request_id is None:
            return

        connection = None
        cursor = None

        try:

            connection = mysql.connector.connect(
                **self.db_config
            )

            connection.start_transaction()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Student_ID, Student_Name
                FROM student_requests
                WHERE Request_ID=%s
                AND Status='Pending'
                FOR UPDATE
                """,
                (request_id,)
            )

            student = cursor.fetchone()

            if not student:

                raise ValueError(
                    "Request not found or already processed."
                )

            confirm = messagebox.askyesno(
                "Reject Student",
                f"Do you want to reject this request?\n\n"
                f"Student ID: {student[0]}\n"
                f"Student Name: {student[1]}",
                parent=self.root
            )

            if not confirm:

                connection.rollback()
                return

            cursor.execute(
                """
                UPDATE student_requests
                SET Status='Rejected'
                WHERE Request_ID=%s
                AND Status='Pending'
                """,
                (request_id,)
            )

            if cursor.rowcount != 1:

                raise ValueError(
                    "Request already processed."
                )

            connection.commit()

            messagebox.showinfo(
                "Rejected",
                "Student registration request rejected.",
                parent=self.root
            )

            self.fetch_requests()

        except mysql.connector.Error as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to reject request.\n\n{e}",
                parent=self.root
            )

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Error",
                str(e),
                parent=self.root
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # LOGOUT
    def logout(self):

        confirm = messagebox.askyesno(
            "Logout",
            "Do you want to logout?",
            parent=self.root
        )

        if not confirm:
            return

        # STOP AUTOMATIC POLLING
        self.polling_active = False

        if self.polling_after_id:

            try:
                self.root.after_cancel(
                    self.polling_after_id
                )
            except Exception:
                pass

            self.polling_after_id = None

        # DESTROY ALL WIDGETS
        for widget in self.root.winfo_children():

            widget.destroy()

        # SHOW LOGIN SCREEN
        self.root.title("Admin Login")

        self.polling_active = True

        self.admin_login_screen()

    # CLOSE WINDOW
    def close_window(self):

        self.polling_active = False

        if self.polling_after_id:

            try:
                self.root.after_cancel(
                    self.polling_after_id
                )
            except Exception:
                pass

        # STOP FLASK SERVER
        try:

            if self.web_server:

                self.web_server.shutdown()
                self.web_server.server_close()

        except Exception as e:

            print("Web server shutdown error:", e)

        # DISCONNECT NGROK
        try:

            if self.ngrok_tunnel and self.ngrok_module:

                self.ngrok_module.disconnect(
                    self.ngrok_tunnel.public_url,
                    pyngrok_config=self.pyngrok_config
                )

        except Exception as e:

            print("Ngrok shutdown error:", e)

        # CLOSE DATABASE
        try:

            if hasattr(self, "my_cursor"):
                self.my_cursor.close()

        except Exception:
            pass

        try:

            if hasattr(self, "conn"):
                self.conn.close()

        except Exception:
            pass

        self.root.destroy()


# MAIN
if __name__ == "__main__":

    root = Tk()

    obj = Admin(root)

    root.mainloop()
