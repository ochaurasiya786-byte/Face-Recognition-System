import os
import ssl
import html
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import mysql.connector

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

ACTION_SALT = "face-attendance-student-approval"


def get_secret_key():
    return os.getenv("SECRET_KEY", "face-attendance-secure-token-secret-2026")


def get_db_config():
    port_val = os.getenv("DB_PORT", "3306")
    try:
        port = int(port_val)
    except (ValueError, TypeError):
        port = 3306

    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "Omkar@7518"),
        "database": os.getenv("DB_NAME", "student"),
        "port": port
    }

    ssl_ca = os.getenv("DB_SSL_CA")
    if ssl_ca and os.path.exists(ssl_ca):
        config["ssl_ca"] = ssl_ca
        config["ssl_verify_cert"] = True
    elif (
        os.getenv("DB_SSL_MODE", "").lower() in ("required", "true", "1")
        or "aivencloud.com" in config["host"]
    ):
        config["ssl_disabled"] = False
        config["ssl_verify_cert"] = False

    return config


def get_db_connection(config=None):
    if config is None:
        config = get_db_config()
    return mysql.connector.connect(**config)


def get_base_url(explicit_url=None):
    if explicit_url:
        return explicit_url.rstrip("/")
    env_url = (
        os.getenv("BASE_URL")
        or os.getenv("RENDER_EXTERNAL_URL")
        or ""
    ).strip().rstrip("/")
    if env_url:
        return env_url
    return "http://127.0.0.1:5000"


def generate_action_token(request_id, action, secret_key=None):
    if secret_key is None:
        secret_key = get_secret_key()
    serializer = URLSafeTimedSerializer(secret_key, salt=ACTION_SALT)
    return serializer.dumps({
        "id": int(request_id),
        "act": str(action).lower().strip()
    })


def verify_action_token(token, max_age_seconds=604800, secret_key=None):
    """
    Verifies a token. Defaults to 7 days validity (604,800 seconds).
    Returns (success_bool, data_dict_or_error_message).
    """
    if secret_key is None:
        secret_key = get_secret_key()
    serializer = URLSafeTimedSerializer(secret_key, salt=ACTION_SALT)
    try:
        data = serializer.loads(token, max_age=max_age_seconds)
        request_id = data.get("id")
        action = data.get("act")
        if not request_id or action not in ("approve", "reject"):
            return False, "Malformed token payload."
        return True, {"request_id": int(request_id), "action": action}
    except SignatureExpired:
        return False, "This action link has expired."
    except BadSignature:
        return False, "Invalid action link signature."
    except Exception as e:
        return False, f"Token verification error: {str(e)}"


def get_request_by_id(request_id, db_config=None):
    """
    Fetches a student request by Request_ID.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection(db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT Request_ID, Dep, Course, Year, Semester,
                   Student_ID, Student_Name, Division, Roll,
                   Gender, DOB, Email, Phone, Address,
                   Teacher, PhotoSample, Status
            FROM student_requests
            WHERE Request_ID = %s
            LIMIT 1
            """,
            (int(request_id),)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching request #{request_id}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def process_approval_action(request_id, action, db_config=None):
    """
    Executes the approval or rejection of a student request atomically in MySQL.
    """
    request_id = int(request_id)
    action = str(action).lower().strip()
    if action not in ("approve", "reject"):
        return {
            "success": False,
            "status": "invalid_action",
            "message": f"Unsupported action '{action}'."
        }

    conn = None
    cursor = None
    try:
        conn = get_db_connection(db_config)
        conn.start_transaction()
        cursor = conn.cursor()

        # Lock the request row
        cursor.execute(
            """
            SELECT Dep, Course, Year, Semester,
                   Student_ID, Student_Name, Division,
                   Roll, Gender, DOB, Email, Phone,
                   Address, Teacher, PhotoSample, Status
            FROM student_requests
            WHERE Request_ID = %s
            FOR UPDATE
            """,
            (request_id,)
        )
        row = cursor.fetchone()

        if not row:
            conn.rollback()
            return {
                "success": False,
                "status": "not_found",
                "message": f"Request #{request_id} does not exist."
            }

        status = row[15]
        student_id = str(row[4])
        student_name = str(row[5])

        if status != "Pending":
            conn.rollback()
            return {
                "success": False,
                "status": "already_processed",
                "current_status": status,
                "student_id": student_id,
                "student_name": student_name,
                "message": f"Request #{request_id} ({student_name}) has already been {status}."
            }

        if action == "approve":
            # Check if student already exists in student table
            cursor.execute(
                "SELECT Student_ID FROM student WHERE Student_ID = %s LIMIT 1",
                (student_id,)
            )
            if cursor.fetchone():
                conn.rollback()
                return {
                    "success": False,
                    "status": "duplicate_student",
                    "student_id": student_id,
                    "student_name": student_name,
                    "message": f"Student ID '{student_id}' is already registered in the student database."
                }

            # Insert into student table
            student_data = row[:15]
            cursor.execute(
                """
                INSERT INTO student
                (
                    Dep, Course, Year, Semester,
                    Student_ID, Student_Name, Division,
                    Roll, Gender, DOB, Email, Phone,
                    Address, Teacher, PhotoSample
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                student_data
            )

            # Update request status to Approved
            cursor.execute(
                """
                UPDATE student_requests
                SET Status = 'Approved'
                WHERE Request_ID = %s AND Status = 'Pending'
                """,
                (request_id,)
            )

            conn.commit()
            return {
                "success": True,
                "status": "approved",
                "student_id": student_id,
                "student_name": student_name,
                "message": f"Student {student_name} (ID: {student_id}) has been successfully approved and enrolled."
            }

        elif action == "reject":
            cursor.execute(
                """
                UPDATE student_requests
                SET Status = 'Rejected'
                WHERE Request_ID = %s AND Status = 'Pending'
                """,
                (request_id,)
            )

            conn.commit()
            return {
                "success": True,
                "status": "rejected",
                "student_id": student_id,
                "student_name": student_name,
                "message": f"Registration request #{request_id} for {student_name} has been rejected."
            }

    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return {
            "success": False,
            "status": "database_error",
            "message": f"Database error during processing: {str(e)}"
        }
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def send_approval_email(
    request_data,
    base_url=None,
    admin_email=None,
    smtp_email=None,
    smtp_app_password=None
):
    """
    Sends an approval request email to the admin with 1-click Accept & Reject links.
    request_data can be a tuple/list (from DB cursor) or a dict.
    """
    if isinstance(request_data, (list, tuple)):
        # Mapping matching admin.py / student_requests schema
        request_id = int(request_data[0])
        dep = str(request_data[1] or "")
        course = str(request_data[2] or "")
        year = str(request_data[3] or "")
        semester = str(request_data[4] or "")
        student_id = str(request_data[5] or "")
        student_name = str(request_data[6] or "")
        roll = str(request_data[8] or "")
        email = str(request_data[11] or "")
        phone = str(request_data[12] or "")
    elif isinstance(request_data, dict):
        request_id = int(request_data.get("Request_ID") or request_data.get("id"))
        dep = str(request_data.get("Dep") or "")
        course = str(request_data.get("Course") or "")
        year = str(request_data.get("Year") or "")
        semester = str(request_data.get("Semester") or "")
        student_id = str(request_data.get("Student_ID") or "")
        student_name = str(request_data.get("Student_Name") or "")
        roll = str(request_data.get("Roll") or "")
        email = str(request_data.get("Email") or "")
        phone = str(request_data.get("Phone") or "")
    else:
        raise ValueError("Invalid request_data format.")

    admin_email = admin_email or os.getenv("ADMIN_EMAIL", "ochaurasiya786@gmail.com")
    smtp_email = smtp_email or os.getenv("SMTP_EMAIL", admin_email)
    smtp_app_password = smtp_app_password or os.getenv("SMTP_APP_PASSWORD", "")

    if not smtp_app_password:
        return False, "SMTP_APP_PASSWORD is not configured in .env."

    resolved_base_url = get_base_url(base_url)

    approve_token = generate_action_token(request_id, "approve")
    reject_token = generate_action_token(request_id, "reject")

    approve_url = f"{resolved_base_url}/action/{approve_token}?auto=1"
    reject_url = f"{resolved_base_url}/action/{reject_token}?auto=1"
    review_url = f"{resolved_base_url}/action/{approve_token}"

    msg = EmailMessage()
    msg["Subject"] = f"Action Required: Student Registration #{request_id} - {student_name}"
    msg["From"] = smtp_email
    msg["To"] = admin_email

    plain_content = (
        f"Student Registration Approval Required\n\n"
        f"Request ID: #{request_id}\n"
        f"Student Name: {student_name}\n"
        f"Student ID: {student_id}\n"
        f"Department: {dep}\n"
        f"Course: {course} ({year}, Sem {semester})\n"
        f"Roll Number: {roll}\n\n"
        f"To ACCEPT and approve immediately:\n{approve_url}\n\n"
        f"To REJECT immediately:\n{reject_url}\n\n"
        f"Or review before deciding:\n{review_url}\n"
    )
    msg.set_content(plain_content)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Student Registration Request</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: #f3f4f6;
                color: #1f2937;
                margin: 0;
                padding: 24px;
            }}
            .container {{
                max-width: 560px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 14px rgba(0,0,0,0.08);
                border: 1px solid #e5e7eb;
            }}
            .header {{
                background: linear-gradient(135deg, #1e3a8a, #2563eb);
                color: white;
                padding: 24px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 20px;
                font-weight: 700;
            }}
            .header p {{
                margin: 6px 0 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .content {{
                padding: 24px;
            }}
            .details-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 16px 0;
            }}
            .details-table td {{
                padding: 10px 12px;
                border-bottom: 1px solid #f3f4f6;
                font-size: 14px;
            }}
            .details-table td.label {{
                color: #6b7280;
                font-weight: 600;
                width: 35%;
            }}
            .details-table td.value {{
                color: #111827;
                font-weight: 500;
            }}
            .actions {{
                margin: 28px 0 16px;
                text-align: center;
            }}
            .btn {{
                display: inline-block;
                padding: 14px 28px;
                margin: 6px 8px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 700;
                text-decoration: none;
                text-align: center;
                transition: all 0.2s ease;
            }}
            .btn-accept {{
                background-color: #16a34a;
                color: #ffffff !important;
            }}
            .btn-reject {{
                background-color: #dc2626;
                color: #ffffff !important;
            }}
            .review-link {{
                display: block;
                text-align: center;
                margin-top: 14px;
                font-size: 13px;
                color: #4b5563;
                text-decoration: underline;
            }}
            .footer {{
                background: #f9fafb;
                padding: 16px 24px;
                text-align: center;
                border-top: 1px solid #e5e7eb;
                font-size: 12px;
                color: #9ca3af;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Student Registration Approval</h1>
                <p>New approval request for Face Recognition System</p>
            </div>
            <div class="content">
                <p style="margin-top:0;font-size:15px;line-height:1.5;">
                    A student has submitted their profile for registration. Please review the details below:
                </p>

                <table class="details-table">
                    <tr>
                        <td class="label">Request ID</td>
                        <td class="value"><strong>#{request_id}</strong></td>
                    </tr>
                    <tr>
                        <td class="label">Student Name</td>
                        <td class="value"><strong>{html.escape(student_name)}</strong></td>
                    </tr>
                    <tr>
                        <td class="label">Student ID</td>
                        <td class="value">{html.escape(student_id)}</td>
                    </tr>
                    <tr>
                        <td class="label">Department</td>
                        <td class="value">{html.escape(dep)}</td>
                    </tr>
                    <tr>
                        <td class="label">Course & Year</td>
                        <td class="value">{html.escape(course)} ({html.escape(year)}, Sem {html.escape(semester)})</td>
                    </tr>
                    <tr>
                        <td class="label">Roll Number</td>
                        <td class="value">{html.escape(roll)}</td>
                    </tr>
                    <tr>
                        <td class="label">Email / Phone</td>
                        <td class="value">{html.escape(email or 'N/A')} / {html.escape(phone or 'N/A')}</td>
                    </tr>
                </table>

                <div class="actions">
                    <a href="{approve_url}" class="btn btn-accept" target="_blank">
                        &#10004; ACCEPT &amp; APPROVE
                    </a>
                    <a href="{reject_url}" class="btn btn-reject" target="_blank">
                        &#10006; REJECT
                    </a>
                </div>

                <a href="{review_url}" class="review-link" target="_blank">
                    Or open full review page with confirmation
                </a>
            </div>
            <div class="footer">
                <p style="margin:0 0 4px;">Host: {html.escape(resolved_base_url)}</p>
                <p style="margin:0;">Works directly from your mobile or desktop email app 24/7.</p>
            </div>
        </div>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    try:
        clean_password = smtp_app_password.replace(" ", "")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.login(smtp_email, clean_password)
            server.send_message(msg)
        return True, f"Approval notification email sent for request #{request_id}."
    except Exception as e:
        err_msg = f"Failed to send email: {str(e)}"
        print(err_msg)
        return False, err_msg

