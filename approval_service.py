import os
import ssl
import html
import smtplib
import threading
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import mysql.connector
from mysql.connector import pooling

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

ACTION_SALT = "face-attendance-student-approval"

# Thread-safe database connection pool for ultra-fast queries
_db_pool = None
_db_pool_lock = threading.Lock()


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
    global _db_pool
    if config is not None:
        return mysql.connector.connect(**config)

    if _db_pool is None:
        with _db_pool_lock:
            if _db_pool is None:
                cfg = get_db_config()
                try:
                    _db_pool = pooling.MySQLConnectionPool(
                        pool_name="face_app_pool",
                        pool_size=5,
                        pool_reset_session=True,
                        **cfg
                    )
                except Exception as e:
                    print("Connection pool initialization fallback:", e)
                    return mysql.connector.connect(**cfg)

    try:
        return _db_pool.get_connection()
    except Exception:
        # Fallback to direct connection if pool is momentarily busy
        return mysql.connector.connect(**get_db_config())


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

            # Dispatch automated email response to student
            student_email = row[10]
            if student_email and "@" in str(student_email):
                import threading
                threading.Thread(
                    target=send_student_decision_email,
                    args=(student_email, student_name, student_id, "approve", request_id),
                    daemon=True
                ).start()

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

            # Dispatch automated email response to student
            student_email = row[10]
            if student_email and "@" in str(student_email):
                import threading
                threading.Thread(
                    target=send_student_decision_email,
                    args=(student_email, student_name, student_id, "reject", request_id),
                    daemon=True
                ).start()

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


def send_email_via_http_api(to_email, subject, html_content, plain_content=""):
    """
    Sends email over HTTPS (Port 443) which is 100% open on Render Free Tier.
    Supports Resend API, Brevo API, and Google Apps Script Webhooks.
    """
    import urllib.request
    import json

    # 1. Google Apps Script Webhook (Direct from your own Gmail account over HTTPS)
    gmail_webhook_url = os.getenv("GMAIL_WEBHOOK_URL", "").strip()
    if gmail_webhook_url:
        try:
            req = urllib.request.Request(
                gmail_webhook_url,
                data=json.dumps({
                    "to": to_email,
                    "subject": subject,
                    "htmlBody": html_content,
                    "body": plain_content
                }).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as res:
                if res.status in (200, 201, 302):
                    return True, "Email sent via Google Apps Script Webhook (Port 443)."
        except Exception as e:
            print("Webhook email error:", e)

    # 2. Resend API (Free 100 emails/day, Port 443)
    resend_api_key = os.getenv("RESEND_API_KEY", "").strip()
    if resend_api_key:
        try:
            from_email = os.getenv("RESEND_FROM", "onboarding@resend.dev")
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps({
                    "from": from_email,
                    "to": [to_email],
                    "subject": subject,
                    "html": html_content
                }).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {resend_api_key}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as res:
                if res.status in (200, 201):
                    return True, "Email sent via Resend API (Port 443)."
        except Exception as e:
            print("Resend API error:", e)

    # 3. Brevo API (Free 300 emails/day, Port 443)
    brevo_api_key = os.getenv("BREVO_API_KEY", "").strip()
    if brevo_api_key:
        try:
            sender_email = os.getenv("SMTP_EMAIL", "ochaurasiya786@gmail.com")
            req = urllib.request.Request(
                "https://api.brevo.com/v3/smtp/email",
                data=json.dumps({
                    "sender": {"email": sender_email, "name": "Attendance Admin"},
                    "to": [{"email": to_email}],
                    "subject": subject,
                    "htmlContent": html_content
                }).encode("utf-8"),
                headers={
                    "api-key": brevo_api_key,
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as res:
                if res.status in (200, 201):
                    return True, "Email sent via Brevo API (Port 443)."
        except Exception as e:
            print("Brevo API error:", e)

    return False, "No HTTPS email provider configured."


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

    admin_email = admin_email or os.getenv("ADMIN_EMAIL") or "ochaurasiya786@gmail.com"
    smtp_email = smtp_email or os.getenv("SMTP_EMAIL") or admin_email
    smtp_app_password = smtp_app_password or os.getenv("SMTP_APP_PASSWORD") or "fxil mqhs tjbg matl"

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

    # 1. Try HTTPS API if configured (Port 443 is unblocked on Render Free Tier)
    http_ok, http_msg = send_email_via_http_api(admin_email, msg["Subject"], html_content, plain_content)
    if http_ok:
        return True, f"Approval notification email sent via HTTPS for request #{request_id}."

    # 2. Try Standard SMTP (Works on local PC or paid hosting)
    try:
        clean_password = smtp_app_password.replace(" ", "")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=12) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.login(smtp_email, clean_password)
            server.send_message(msg)
        return True, f"Approval notification email sent for request #{request_id}."
    except Exception as e:
        err_msg = f"Failed to send email: {str(e)}"
        if "101" in str(e) or "unreachable" in str(e).lower():
            print("Notice: Render Free Tier blocks outbound SMTP ports 587/465. To send emails from Render, use an HTTPS email API (RESEND_API_KEY / BREVO_API_KEY / GMAIL_WEBHOOK_URL) or manage requests via Admin Panel.")
        else:
            print(err_msg)
        return False, err_msg


def send_student_decision_email(student_email, student_name, student_id, action, request_id=None, smtp_email=None, smtp_app_password=None):
    """
    Sends an automated notification email directly to the student when their registration is Approved or Rejected.
    """
    if not student_email or "@" not in str(student_email):
        return False, "No valid student email provided."

    smtp_email = smtp_email or os.getenv("SMTP_EMAIL") or "ochaurasiya786@gmail.com"
    smtp_app_password = smtp_app_password or os.getenv("SMTP_APP_PASSWORD") or "fxil mqhs tjbg matl"

    action = str(action).lower().strip()
    is_approved = (action == "approve")

    subject = f"{'🎉 Registration Approved' if is_approved else '⚠️ Registration Update'}: Student ID #{student_id} ({student_name})"
    status_text = "APPROVED" if is_approved else "REJECTED"
    badge_bg = "#10b981" if is_approved else "#ef4444"
    heading_text = "Your Registration Has Been Approved!" if is_approved else "Your Registration Was Not Approved"
    message_text = (
        "Congratulations! Your student registration has been reviewed and approved by the department administrator. Your profile is now active in the system, and your face is eligible for automated attendance."
        if is_approved else
        "Your student registration request has been reviewed by the department administrator and was not approved. Please contact the department office if you need further clarification."
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = str(student_email).strip()

    plain_content = f"""Dear {student_name},

{heading_text}

Status: {status_text}
Student ID: {student_id}
Request ID: #{request_id or 'N/A'}

{message_text}

Thank you,
AI Face Recognition Attendance Management System
"""
    msg.set_content(plain_content)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; margin: 0; padding: 24px; color: #1f2937;">
        <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
            <div style="background: linear-gradient(135deg, #071426, #1e3a8a); color: white; padding: 24px; text-align: center;">
                <h2 style="margin: 0; font-size: 20px;">AI Face Recognition Attendance System</h2>
                <p style="margin: 6px 0 0; opacity: 0.85; font-size: 13px;">Khwaja Moinuddin Chishti Language University</p>
            </div>
            <div style="padding: 24px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <span style="display: inline-block; background: {badge_bg}; color: white; font-weight: bold; font-size: 12px; padding: 6px 16px; border-radius: 20px; letter-spacing: 0.5px;">
                        {status_text}
                    </span>
                    <h3 style="color: #111827; margin: 14px 0 6px; font-size: 18px;">{heading_text}</h3>
                    <p style="color: #4b5563; font-size: 14px; line-height: 1.5; margin: 0;">{message_text}</p>
                </div>
                <div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                    <table style="width: 100%; font-size: 14px; color: #374151; border-collapse: collapse;">
                        <tr><td style="padding: 5px 0; color: #6b7280; width: 130px;">Student Name:</td><td style="padding: 5px 0; font-weight: bold;">{student_name}</td></tr>
                        <tr><td style="padding: 5px 0; color: #6b7280;">Student ID:</td><td style="padding: 5px 0; font-weight: bold;">{student_id}</td></tr>
                        <tr><td style="padding: 5px 0; color: #6b7280;">Status:</td><td style="padding: 5px 0; font-weight: bold; color: {badge_bg};">{status_text}</td></tr>
                    </table>
                </div>
                <div style="text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6; padding-top: 14px;">
                    This is an automated notification from the Attendance Management System.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    # 1. Try HTTPS API if configured
    http_ok, http_msg = send_email_via_http_api(student_email, msg["Subject"], html_content, plain_content)
    if http_ok:
        return True, f"Decision email sent via HTTPS to student {student_email}."

    # 2. Try Standard SMTP
    try:
        clean_password = smtp_app_password.replace(" ", "")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=12) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.login(smtp_email, clean_password)
            server.send_message(msg)
        return True, f"Decision email sent to student {student_email}."
    except Exception as e:
        err_msg = f"Failed to send decision email: {str(e)}"
        if "101" not in str(e) and "unreachable" not in str(e).lower():
            print(err_msg)
        return False, err_msg


def send_student_submission_confirmation(student_email, student_name, student_id, request_id, smtp_email=None, smtp_app_password=None):
    """
    Sends an automated confirmation email to the student immediately after they submit registration.
    """
    if not student_email or "@" not in str(student_email):
        return False, "No valid student email provided."

    smtp_email = smtp_email or os.getenv("SMTP_EMAIL") or "ochaurasiya786@gmail.com"
    smtp_app_password = smtp_app_password or os.getenv("SMTP_APP_PASSWORD") or "fxil mqhs tjbg matl"

    subject = f"Registration Submitted: Request #{request_id} ({student_name})"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = str(student_email).strip()

    plain_content = f"""Dear {student_name},

Your registration request #{request_id} for Student ID {student_id} has been submitted successfully!

Status: PENDING ADMIN APPROVAL

An approval notification has been sent to the Department Administrator. Once approved, your profile will be activated in the attendance system.

Thank you,
AI Face Recognition Attendance Management System
"""
    msg.set_content(plain_content)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; margin: 0; padding: 24px; color: #1f2937;">
        <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
            <div style="background: linear-gradient(135deg, #071426, #1e3a8a); color: white; padding: 24px; text-align: center;">
                <h2 style="margin: 0; font-size: 20px;">AI Face Recognition Attendance System</h2>
                <p style="margin: 6px 0 0; opacity: 0.85; font-size: 13px;">Khwaja Moinuddin Chishti Language University</p>
            </div>
            <div style="padding: 24px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <span style="display: inline-block; background: #3b82f6; color: white; font-weight: bold; font-size: 12px; padding: 6px 16px; border-radius: 20px; letter-spacing: 0.5px;">
                        SUBMITTED
                    </span>
                    <h3 style="color: #111827; margin: 14px 0 6px; font-size: 18px;">Registration Submitted Successfully</h3>
                    <p style="color: #4b5563; font-size: 14px; line-height: 1.5; margin: 0;">
                        Your registration has been forwarded to the Administrator for verification and approval.
                    </p>
                </div>
                <div style="background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                    <table style="width: 100%; font-size: 14px; color: #374151; border-collapse: collapse;">
                        <tr><td style="padding: 5px 0; color: #6b7280; width: 130px;">Request ID:</td><td style="padding: 5px 0; font-weight: bold;">#{request_id}</td></tr>
                        <tr><td style="padding: 5px 0; color: #6b7280;">Student Name:</td><td style="padding: 5px 0; font-weight: bold;">{student_name}</td></tr>
                        <tr><td style="padding: 5px 0; color: #6b7280;">Student ID:</td><td style="padding: 5px 0; font-weight: bold;">{student_id}</td></tr>
                        <tr><td style="padding: 5px 0; color: #6b7280;">Status:</td><td style="padding: 5px 0; font-weight: bold; color: #f59e0b;">Pending Admin Approval</td></tr>
                    </table>
                </div>
                <div style="text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6; padding-top: 14px;">
                    You will receive another email as soon as your registration is approved.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    # 1. Try HTTPS API if configured
    http_ok, http_msg = send_email_via_http_api(student_email, msg["Subject"], html_content, plain_content)
    if http_ok:
        return True, f"Submission confirmation email sent via HTTPS to student {student_email}."

    # 2. Try Standard SMTP
    try:
        clean_password = smtp_app_password.replace(" ", "")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=12) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.login(smtp_email, clean_password)
            server.send_message(msg)
        return True, f"Submission confirmation email sent to student {student_email}."
    except Exception as e:
        err_msg = f"Failed to send confirmation email: {str(e)}"
        if "101" not in str(e) and "unreachable" not in str(e).lower():
            print(err_msg)
        return False, err_msg

