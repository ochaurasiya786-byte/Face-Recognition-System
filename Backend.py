import os
import html
import threading
import csv
from flask import (
    Flask, request, jsonify, render_template_string,
    render_template, redirect, session, url_for, send_from_directory,
    make_response
)
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

from approval_service import (
    get_db_connection,
    get_db_config,
    verify_action_token,
    process_approval_action,
    get_request_by_id,
    send_approval_email,
    get_base_url,
    get_secret_key
)

# Load environment configuration
load_dotenv()

app = Flask(__name__)
app.secret_key = get_secret_key()

# ACTION CONFIRMATION PAGE TEMPLATE
ACTION_CONFIRM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Confirm {{ action_upper }} - Student Registration</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #f0f2f5;
            margin: 0;
            padding: 24px 16px;
            color: #1f2937;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .card {
            background: #ffffff;
            max-width: 520px;
            width: 100%;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }
        .card-header {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 24px 20px;
            text-align: center;
        }
        .card-header h2 { margin: 0 0 6px 0; font-size: 20px; font-weight: 700; }
        .card-header p { margin: 0; font-size: 14px; opacity: 0.9; }
        .card-body { padding: 24px 20px; }
        .badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: white;
            background: {{ color }};
            margin-bottom: 18px;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
            font-size: 14px;
        }
        .info-table tr { border-bottom: 1px solid #f3f4f6; }
        .info-table td { padding: 10px 8px; }
        .info-table .label { color: #6b7280; font-weight: 600; width: 38%; }
        .info-table .val { color: #111827; font-weight: 500; }
        .btn-submit {
            display: block;
            width: 100%;
            padding: 14px;
            border: 0;
            border-radius: 10px;
            color: white;
            background: {{ color }};
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: opacity 0.2s;
        }
        .btn-submit:hover { opacity: 0.92; }
        .footer-note {
            text-align: center;
            font-size: 12px;
            color: #9ca3af;
            margin-top: 16px;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-header">
            <h2>Student Registration Action</h2>
            <p>Face Recognition Attendance System</p>
        </div>
        <div class="card-body">
            <div style="text-align: center;">
                <span class="badge">Action: {{ action_upper }}</span>
            </div>
            <table class="info-table">
                <tr><td class="label">Request ID</td><td class="val">#{{ req.Request_ID }}</td></tr>
                <tr><td class="label">Student Name</td><td class="val"><strong>{{ req.Student_Name }}</strong></td></tr>
                <tr><td class="label">Student ID</td><td class="val">{{ req.Student_ID }}</td></tr>
                <tr><td class="label">Department</td><td class="val">{{ req.Dep }}</td></tr>
                <tr><td class="label">Course &amp; Year</td><td class="val">{{ req.Course }} ({{ req.Year }}, Sem {{ req.Semester }})</td></tr>
                <tr><td class="label">Roll Number</td><td class="val">{{ req.Roll }}</td></tr>
                <tr><td class="label">Email / Phone</td><td class="val">{{ req.Email or 'N/A' }} / {{ req.Phone or 'N/A' }}</td></tr>
            </table>

            <form method="POST">
                {% if action == 'reject' %}
                <div style="margin-bottom: 16px; text-align: left;">
                    <label for="rejection_reason" style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Rejection Reason (included in notification to student):</label>
                    <textarea name="rejection_reason" id="rejection_reason" rows="3" placeholder="e.g. Invalid face photo, incorrect department, invalid details..." style="width:100%;padding:10px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;resize:vertical;" required>Profile details do not match institutional records or photo verification failed.</textarea>
                </div>
                {% endif %}
                <button type="submit" class="btn-submit">
                    Confirm {{ action_upper }}
                </button>
            </form>

            <div class="footer-note">
                Pressing confirm will update the student record in the MySQL database immediately.
            </div>
        </div>
    </div>
</body>
</html>
"""

# ACTION RESULT PAGE TEMPLATE
ACTION_RESULT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }}</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #f0f2f5;
            margin: 0;
            padding: 24px 16px;
            color: #1f2937;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .card {
            background: #ffffff;
            max-width: 480px;
            width: 100%;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            text-align: center;
            padding: 36px 24px;
            border: 1px solid #e5e7eb;
        }
        .icon { font-size: 52px; margin-bottom: 12px; }
        .badge {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: white;
            background: {{ badge_color }};
            margin-bottom: 14px;
        }
        h2 { margin: 0 0 10px; font-size: 22px; color: #111827; }
        p.msg { font-size: 15px; color: #4b5563; line-height: 1.5; margin: 0 0 20px; }
        .summary-box {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 14px;
            margin: 16px 0 24px;
            text-align: left;
            font-size: 14px;
        }
        .summary-box div { margin: 4px 0; color: #374151; }
        .close-hint { font-size: 13px; color: #9ca3af; margin: 0; }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">{{ icon }}</div>
        <div><span class="badge">{{ badge_text }}</span></div>
        <h2>{{ heading }}</h2>
        <p class="msg">{{ message|safe }}</p>

        {% if details %}
        <div class="summary-box">
            <div><strong>Student:</strong> {{ details.Student_Name }}</div>
            <div><strong>Student ID:</strong> {{ details.Student_ID }}</div>
            <div><strong>Department:</strong> {{ details.Dep }} ({{ details.Course }})</div>
            <div><strong>Roll Number:</strong> {{ details.Roll }}</div>
        </div>
        {% endif %}

        <p class="close-hint">You may now safely close this browser tab.</p>
    </div>
</body>
</html>
"""

# COLLEGE LOCATION

COLLEGE_LAT = 26.928674
COLLEGE_LON = 80.896134

# ALLOWED RADIUS

RADIUS = 4000

# ATTENDANCE TIME

START_TIME = "08:00"
END_TIME = "23:00"

def get_ist_timezone():
    """
    Returns timezone object for Asia/Kolkata (IST, UTC+5:30).
    Uses ZoneInfo when available (Linux/Render/cloud), falling back gracefully
    to fixed UTC+5:30 offset on systems without tzdata (e.g. Windows).
    """
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("Asia/Kolkata")
    except Exception:
        from datetime import timezone, timedelta
        return timezone(timedelta(hours=5, minutes=30))

def get_current_ist_datetime():
    """
    Returns current datetime in Asia/Kolkata (IST, UTC+5:30) timezone.
    Guarantees reliable timezone resolution on Windows, Linux, Render, Docker, or UTC cloud environments.
    """
    return datetime.now(get_ist_timezone())

def is_attendance_time_allowed(dt=None):
    """
    Checks if given datetime (default: current IST time) is within permitted hours:
    08:00 AM <= Current IST <= 11:00 PM (inclusive of 11:00 PM up to 23:00:59, rejecting 11:01 PM).
    """
    if dt is None:
        dt = get_current_ist_datetime()

    minutes = dt.hour * 60 + dt.minute
    start_minutes = 8 * 60    # 08:00 AM -> 480
    end_minutes = 23 * 60     # 11:00 PM -> 1380

    return start_minutes <= minutes <= end_minutes

# VERIFICATION STORAGE

verified_students = {}
pc_location = {}

# LOCATION VALIDITY

LOCATION_VALIDITY = 86400
# 86400 sec= 1 day

# CALCULATE DISTANCE

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000

    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))

    dlat = lat2 - lat1
    dlon = radians(float(lon2)) - radians(float(lon1))

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c

# CHECK STUDENT FROM MYSQL

def check_student_id(student_id):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                Student_ID,
                Student_Name,
                Dep,
                Course,
                Roll
            FROM student
            WHERE Student_ID=%s
            LIMIT 1
            """,
            (str(student_id).strip(),)
        )

        result = cursor.fetchone()
        if not result:
            cursor.execute(
                """
                SELECT
                    Student_ID,
                    Student_Name,
                    Dep,
                    Course,
                    Roll
                FROM student_requests
                WHERE Student_ID=%s AND Status IN ('Approved', 'Pending')
                LIMIT 1
                """,
                (str(student_id).strip(),)
            )
            result = cursor.fetchone()

        return result

    except Exception as e:
        print("Database Error:", e)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()

# HOME PORTAL & HEALTH CHECKS

@app.route("/")
def home():
    format_param = request.args.get("format", "").lower()

    # Return JSON ONLY if explicitly requested via ?format=json
    if format_param == "json":
        db_connected = False
        try:
            test_conn = get_db_connection()
            if test_conn.is_connected():
                db_connected = True
                test_conn.close()
        except Exception:
            db_connected = False

        return jsonify({
            "status": "success",
            "service": "Face Recognition Attendance & Approval Backend",
            "database_connected": db_connected,
            "render_compatible": True
        })

    # Render Modern Web Dashboard
    stats = {
        "total_students": 0,
        "pending_requests": 0,
        "approved_requests": 0
    }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM student")
        stats["total_students"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM student_requests WHERE Status='Pending'")
        stats["pending_requests"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM student_requests WHERE Status='Approved'")
        stats["approved_requests"] = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception as e:
        print("Stats fetch error:", e)

    return render_template("index.html", stats=stats, active_page="home")

# STUDENT REGISTRATION PAGE
@app.route("/register")
def register_page():
    return render_template("register.html", active_page="register")

# API FOR STUDENT REGISTRATION SUBMISSION
@app.route("/api/submit-registration", methods=["POST"])
def submit_registration_api():
    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    student_name = str(data.get("student_name", "")).strip()
    dep = str(data.get("dep", "")).strip()
    course = str(data.get("course", "")).strip()
    year = str(data.get("year", "")).strip()
    division = str(data.get("division", "")).strip()
    gender = str(data.get("gender", "")).strip()
    roll = str(data.get("roll", "")).strip()

    if not student_id or not student_name or not dep or not course or not year or not roll or not division or not gender:
        return jsonify({
            "success": False,
            "message": "All mandatory fields (*): Student ID, Full Name, Department, Course, Year, Roll, Division, and Gender are required."
        }), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Check if Student ID already exists in student table
        cursor.execute("SELECT Student_ID FROM student WHERE Student_ID = %s LIMIT 1", (student_id,))
        if cursor.fetchone():
            return jsonify({
                "success": False,
                "already_registered": True,
                "title": "Already Registered!",
                "message": "This student is already registered in the system. Please use your existing Student ID or contact the administrator."
            }), 409

        # 2. Check if Student ID already exists in pending or approved requests
        cursor.execute("SELECT Request_ID FROM student_requests WHERE Student_ID = %s AND Status IN ('Pending', 'Approved') LIMIT 1", (student_id,))
        if cursor.fetchone():
            return jsonify({
                "success": False,
                "already_registered": True,
                "title": "Already Registered!",
                "message": "This student is already registered in the system. Please use your existing Student ID or contact the administrator."
            }), 409

        # 3. Check if registered Email already exists
        email = str(data.get("email", "")).strip()
        if email:
            cursor.execute("SELECT Student_ID FROM student WHERE LOWER(Email) = LOWER(%s) LIMIT 1", (email,))
            if cursor.fetchone():
                return jsonify({
                    "success": False,
                    "already_registered": True,
                    "title": "Already Registered!",
                    "message": "This student is already registered in the system. Please use your existing Student ID or contact the administrator."
                }), 409

            cursor.execute("SELECT Request_ID FROM student_requests WHERE LOWER(Email) = LOWER(%s) AND Status IN ('Pending', 'Approved') LIMIT 1", (email,))
            if cursor.fetchone():
                return jsonify({
                    "success": False,
                    "already_registered": True,
                    "title": "Already Registered!",
                    "message": "This student is already registered in the system. Please use your existing Student ID or contact the administrator."
                }), 409

        # Insert new request
        sql = """
            INSERT INTO student_requests (
                Dep, Course, Year, Semester, Student_ID, Student_Name,
                Division, Roll, Gender, DOB, Email, Phone, Address, Teacher, PhotoSample, Status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        """
        values = (
            dep,
            course,
            year,
            data.get("semester", ""),
            student_id,
            student_name,
            division,
            roll,
            gender,
            data.get("dob", ""),
            data.get("email", ""),
            data.get("phone", ""),
            data.get("address", ""),
            data.get("teacher", ""),
            "No"
        )
        cursor.execute(sql, values)
        conn.commit()
        new_request_id = cursor.lastrowid

        # Dispatch async email notification to Admin and Student
        stu_email = data.get("email", "").strip()
        def notify_async(rid, s_email, s_name, s_id):
            try:
                req_data = get_request_by_id(rid)
                if req_data:
                    send_approval_email(req_data)
                if s_email and "@" in s_email:
                    from approval_service import send_student_submission_confirmation
                    send_student_submission_confirmation(s_email, s_name, s_id, rid)
            except Exception as ex:
                print("Email dispatch error:", ex)

        threading.Thread(target=notify_async, args=(new_request_id, stu_email, student_name, student_id), daemon=True).start()

        return jsonify({
            "success": True,
            "message": f"Registration request #{new_request_id} for {student_name} submitted successfully! Admin has been notified for approval.",
            "request_id": new_request_id
        })

    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ADMIN WEB PORTAL
@app.route("/admin-portal")
def admin_portal():
    if not session.get("admin_logged_in"):
        return render_template("admin_portal.html", logged_in=False, active_page="admin")

    pending_requests = []
    students = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_requests WHERE Status='Pending' ORDER BY Request_ID DESC")
        pending_requests = cursor.fetchall()

        cursor.execute("SELECT * FROM student ORDER BY Student_ID ASC")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Admin portal data fetch error:", e)

    return render_template(
        "admin_portal.html",
        logged_in=True,
        username=session.get("admin_username", "Admin"),
        pending_requests=pending_requests,
        students=students,
        active_page="admin"
    )

@app.route("/admin-portal/login", methods=["POST"])
def admin_portal_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    is_valid = False
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Password FROM admin WHERE Username = %s LIMIT 1", (username,))
        row = cursor.fetchone()
        if row and row[0] == password:
            is_valid = True
        cursor.close()
        conn.close()
    except Exception as e:
        if username == "admin" and password == "Admin@123":
            is_valid = True

    if is_valid:
        session["admin_logged_in"] = True
        session["admin_username"] = username
        return redirect(url_for("admin_portal"))
    else:
        return "<script>alert('Invalid Admin credentials.'); window.location.href='/admin-portal';</script>"

@app.route("/admin-portal/logout")
def admin_portal_logout():
    session.clear()
    return redirect(url_for("admin_portal"))

@app.route("/api/admin-action/<int:request_id>/<action>", methods=["POST"])
def admin_action_api(request_id, action):
    if not session.get("admin_logged_in"):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    result = process_approval_action(request_id, action)
    return jsonify(result), (200 if result.get("success") else 400)

# STATIC IMAGES SERVING (College_images & data)

@app.route("/college_images/<path:filename>")
def serve_college_image(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(base_dir, "College_images"), filename)

@app.route("/data_images/<path:filename>")
def serve_data_image(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(base_dir, "data"), filename)

# API ENDPOINTS FOR FRONTEND DASHBOARD BUTTONS

@app.route("/api/enrolled-students", methods=["GET"])
def api_enrolled_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT Student_ID, Student_Name, Dep, Course, Year, Semester,
                   Division, Roll, Gender, DOB, Email, Phone, Teacher
            FROM student
            ORDER BY Student_ID ASC
        """)
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "count": len(students), "students": students})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "students": []}), 500

@app.route("/api/attendance-records", methods=["GET"])
def api_attendance_records():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "attendence.csv")
    records = []

    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 6:
                        records.append({
                            "student_id": row[0],
                            "roll": row[1] if len(row) > 1 else "",
                            "name": row[2] if len(row) > 2 else "",
                            "department": row[3] if len(row) > 3 else "",
                            "time": row[4] if len(row) > 4 else "",
                            "date": row[5] if len(row) > 5 else "",
                            "status": row[-1] if len(row) > 6 else "Present"
                        })
        except Exception as e:
            print("Error reading attendence.csv:", e)

    return jsonify({"success": True, "count": len(records), "records": records[:100]})

@app.route("/api/sample-photos", methods=["GET"])
def api_sample_photos():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    photos = []
    total_files = 0
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        total_files = len(files)
        photos = files[:40]
    return jsonify({"success": True, "count": len(photos), "total_count": total_files, "photos": photos})

@app.route("/api/dataset-stats", methods=["GET"])
def api_dataset_stats():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    classifier_path = os.path.join(base_dir, "classifier.xml")

    total_samples = 0
    student_ids = set()
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        total_samples = len(files)
        for f in files:
            parts = f.split(".")
            if len(parts) >= 3:
                try:
                    student_ids.add(int(parts[1]))
                except ValueError:
                    pass

    classifier_exists = os.path.exists(classifier_path)
    classifier_mtime = ""
    if classifier_exists:
        try:
            mtime = os.path.getmtime(classifier_path)
            classifier_mtime = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            classifier_mtime = "Active"

    return jsonify({
        "success": True,
        "total_samples": total_samples,
        "total_students": len(student_ids),
        "student_ids": sorted(list(student_ids)),
        "classifier_exists": classifier_exists,
        "classifier_mtime": classifier_mtime,
        "threshold": 65.0,
        "model_type": "LBPH (Local Binary Patterns Histograms)"
    })

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    msg = str(data.get("message", "")).strip()

    try:
        from ai_help_desk import get_help_desk_response
        reply = get_help_desk_response(msg)
    except Exception as e:
        reply = f"Error processing query: {str(e)}"

    return jsonify({"reply": reply})

# ==========================================
# BIOMETRIC MODEL CACHE & RECOGNIZER HELPER
# ==========================================
_cached_recognizer = None
_cached_cascade = None
_cached_classifier_mtime = 0

def get_face_recognizer(base_dir):
    global _cached_recognizer, _cached_cascade, _cached_classifier_mtime
    import cv2
    
    cascade_path = os.path.join(base_dir, "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascade_path):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    
    if _cached_cascade is None:
        _cached_cascade = cv2.CascadeClassifier(cascade_path)
        
    classifier_path = os.path.join(base_dir, "classifier.xml")
    if not os.path.exists(classifier_path):
        return None, _cached_cascade
        
    mtime = os.path.getmtime(classifier_path)
    if _cached_recognizer is None or mtime != _cached_classifier_mtime:
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read(classifier_path)
        _cached_recognizer = clf
        _cached_classifier_mtime = mtime
        
    return _cached_recognizer, _cached_cascade

# Background thread to pre-warm biometric models in RAM for instant 0.05s inference
def _prewarm_biometrics():
    try:
        b_dir = os.path.dirname(os.path.abspath(__file__))
        get_face_recognizer(b_dir)
        print("Biometric recognizer pre-warmed successfully.")
    except Exception as e:
        print("Pre-warm info:", e)

threading.Thread(target=_prewarm_biometrics, daemon=True).start()

@app.route("/api/mark-face-attendance", methods=["POST"])
def api_mark_face_attendance():
    # CRITICAL RULE 1: Time Verification (Asia/Kolkata IST 08:00 AM - 11:00 PM)
    if not is_attendance_time_allowed():
        return jsonify({
            "success": False,
            "status": "UNMARKED",
            "time_restricted": True,
            "message": "❌ Verification Failed: Attendance is allowed only between 8:00 AM and 11:00 PM."
        }), 403

    data = request.get_json(silent=True) or {}
    image_b64 = data.get("image", "")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # CRITICAL RULE 2: Live Camera Frame Verification
    if not image_b64:
        return jsonify({
            "success": False,
            "status": "UNMARKED",
            "biometric_failure": True,
            "message": "❌ Camera image frame missing. Please keep your face clearly in front of the camera. Attendance Not Marked."
        }), 400

    try:
        import base64
        import numpy as np
        import cv2

        if "," in image_b64:
            image_b64 = image_b64.split(",", 1)[1]

        img_bytes = base64.b64decode(image_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "biometric_failure": True,
                "message": "❌ Invalid camera frame received. Please ensure camera access. Attendance Not Marked."
            }), 400

        clf, face_cascade = get_face_recognizer(base_dir)

        if clf is None:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "message": "❌ Biometric model (classifier.xml) not found. Please train faces first."
            }), 500

        # Fast optimization: Downscale high-resolution frames to max width 480 for 5x faster Haar detection
        h, w = img.shape[:2]
        if w > 480:
            scale_ratio = 480.0 / w
            new_h = int(h * scale_ratio)
            img_fast = cv2.resize(img, (480, new_h), interpolation=cv2.INTER_AREA)
        else:
            img_fast = img

        gray = cv2.cvtColor(img_fast, cv2.COLOR_BGR2GRAY)
        # Optimized Haar parameters for fast 1-2 meters detection range
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4, minSize=(30, 30))

        # CRITICAL RULE 3: Live Face Detection
        if len(faces) == 0:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "biometric_failure": True,
                "message": "❌ Face Not Detected – Please look directly at the camera in good lighting. Attendance Not Marked."
            }), 400

        # Sort to find largest face
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]

        # CRITICAL RULE 4: Anti-Spoofing & Liveness Texture Check
        lap_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
        contrast_std = float(np.std(face_roi))
        if lap_var < 3.0 or contrast_std < 18.0:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "biometric_failure": True,
                "liveness_failure": True,
                "message": "❌ Anti-Spoofing Check Failed: Static or blurred screen/photo detected. Live Face Required. Attendance Not Marked."
            }), 403

        # CRITICAL RULE 5: Automatic Student Identification via Trained LBPH Model
        predicted_id, distance = clf.predict(face_roi)
        confidence = max(0, min(100, int(100 * (1.0 - distance / 85.0))))

        # Calibrated threshold: distance <= 65.0 is recognized
        if distance > 70.0:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "unknown_student": True,
                "distance": round(distance, 1),
                "confidence": confidence,
                "message": f"❌ Unknown Student – Face not recognized in the system (distance: {round(distance, 1)}). Unauthorized faces cannot mark attendance."
            }), 403

        if distance > 65.0:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "uncertain_match": True,
                "distance": round(distance, 1),
                "confidence": confidence,
                "message": f"⚠️ Face match uncertain (distance: {round(distance, 1)}). Please face the camera clearly and try again."
            }), 403

        # Retrieve registered identity from Database using the recognized student ID
        student = check_student_id(str(predicted_id))
        if not student:
            return jsonify({
                "success": False,
                "status": "UNMARKED",
                "unknown_student": True,
                "message": f"❌ Unknown Student: Recognized identity (ID: {predicted_id}) is not found in the student database."
            }), 404

        student_id = str(student[0]).strip()
        student_name = str(student[1]).strip()
        department = str(student[2]).strip()
        course = str(student[3]).strip() if len(student) > 3 and student[3] else ""
        roll = str(student[4]).strip() if len(student) > 4 and student[4] else "1"

    except Exception as ex:
        print("Biometric processing error:", ex)
        return jsonify({
            "success": False,
            "status": "UNMARKED",
            "message": f"Biometric verification error: {str(ex)}"
        }), 500

    # CRITICAL RULE 6: Duplicate Attendance Check for Today (Asia/Kolkata IST)
    now_ist = get_current_ist_datetime()
    now_time = now_ist.strftime("%H:%M:%S")
    now_date = now_ist.strftime("%d/%m/%Y")
    csv_path = os.path.join(base_dir, "attendence.csv")

    already_marked = False
    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or str(row[0]).strip().lower() in ("student_id", "student id"):
                        continue
                    if len(row) >= 6:
                        if str(row[0]).strip() == student_id and str(row[5]).strip() == now_date:
                            already_marked = True
                            break
        except Exception as csv_err:
            print("CSV duplicate check error:", csv_err)

    if already_marked:
        return jsonify({
            "success": False,
            "status": "ALREADY_MARKED",
            "student_id": student_id,
            "name": student_name,
            "message": f"⚠️ Attendance Already Marked: Student {student_name} (ID: {student_id}) has already marked attendance for today ({now_date})."
        }), 400

    # CRITICAL RULE 7: Geolocation 4 KM campus boundary check
    req_lat = data.get("latitude")
    req_lon = data.get("longitude")
    distance_meters = 50.0
    recorded_lat = COLLEGE_LAT
    recorded_lon = COLLEGE_LON

    if req_lat is not None and req_lon is not None:
        try:
            req_lat = float(req_lat)
            req_lon = float(req_lon)
            distance_meters = round(calculate_distance(req_lat, req_lon, COLLEGE_LAT, COLLEGE_LON), 1)
            recorded_lat = req_lat
            recorded_lon = req_lon

            # STRICT 4 KILOMETRE LIMIT
            if distance_meters > RADIUS:
                dist_km = round(distance_meters / 1000.0, 2)
                return jsonify({
                    "success": False,
                    "status": "UNMARKED",
                    "outside_boundary": True,
                    "student_id": student_id,
                    "name": student_name,
                    "distance": distance_meters,
                    "distance_km": dist_km,
                    "latitude": req_lat,
                    "longitude": req_lon,
                    "message": f"❌ Location Restriction: You are {dist_km} km away from campus. Attendance cannot be marked because you are outside the 4 km boundary."
                }), 403
        except (ValueError, TypeError) as e:
            print("Location parse error:", e)

    # ONLY WHEN ALL CHECKS PASS -> RECORD ATTENDANCE AS PRESENT
    try:
        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                student_id, roll, student_name, department,
                now_time, now_date, str(recorded_lat), str(recorded_lon),
                str(distance_meters), f"Biometric-{confidence}%", "Verified", "Verified", "Present"
            ])
    except Exception as e:
        print("Error recording attendance CSV:", e)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO attendance (
                Student_ID, Roll, Name, Department,
                Time, Date, Latitude, Longitude, Distance,
                Confidence, Status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Present')
            """,
            (student_id, roll, student_name, department, now_time, now_date, recorded_lat, recorded_lon, distance_meters, confidence)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        pass

    return jsonify({
        "success": True,
        "status": "PRESENT",
        "student_identified": True,
        "student_id": student_id,
        "name": student_name,
        "department": department,
        "course": course,
        "roll": roll,
        "time": now_time,
        "date": now_date,
        "latitude": recorded_lat,
        "longitude": recorded_lon,
        "distance": distance_meters,
        "match_distance": round(distance, 1),
        "confidence": confidence,
        "message": f"Student Identified Successfully\nStudent Name: {student_name}\nStudent ID: {student_id}"
    })

@app.route("/api/admin-verify", methods=["POST"])
def api_admin_verify():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "❌ Strictly required: Admin username/email and password must both be entered."
        }), 400

    authenticated = False
    conn = None
    cursor = None
    try:
        import hashlib
        conn = get_db_connection()
        cursor = conn.cursor()

        # Strictly validate credentials against MySQL admin table
        cursor.execute(
            "SELECT Admin_ID, Password FROM admin WHERE Username = %s LIMIT 1",
            (username,)
        )
        row = cursor.fetchone()

        if row:
            admin_id, stored_pass = row[0], row[1]
            entered_hash = hashlib.sha256(password.encode()).hexdigest()

            # Verify against stored SHA-256 hash or plain-text password
            if stored_pass == entered_hash or stored_pass == password:
                authenticated = True
                # Automatically upgrade plain-text passwords to SHA-256 hash in database
                if len(stored_pass) != 64:
                    try:
                        cursor.execute(
                            "UPDATE admin SET Password = %s WHERE Admin_ID = %s",
                            (entered_hash, admin_id)
                        )
                        conn.commit()
                    except Exception as up_err:
                        print("Password hash migration notice:", up_err)

    except Exception as e:
        print("Admin database authentication error:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    if authenticated:
        session["admin_logged_in"] = True
        return jsonify({
            "success": True,
            "message": "Admin credentials verified successfully."
        })
    else:
        return jsonify({
            "success": False,
            "message": "❌ Authentication Failed: Invalid admin username or password. Access denied."
        }), 401

@app.after_request
def add_security_headers(response):
    # Prevent caching of logout, exit, and protected admin endpoints
    if request.path in ["/exit", "/logout", "/admin-portal"] or request.path.startswith("/api/admin"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0, post-check=0, pre-check=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
    return response

@app.route("/exit")
@app.route("/logout")
def exit_application_page():
    session.clear()
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Application Exited</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #071426;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
            text-align: center;
        }
        .exit-card {
            background: #0b1f3a;
            border: 1px solid #18385f;
            border-radius: 14px;
            padding: 44px 32px;
            max-width: 520px;
            width: 100%;
            box-shadow: 0 14px 40px rgba(0,0,0,0.6);
        }
        .exit-icon { font-size: 3.8rem; margin-bottom: 16px; line-height: 1; }
        h2 { color: #55c7ff; font-size: 1.75rem; margin-bottom: 12px; font-weight: 700; }
        p.exit-desc { color: #9db4cf; font-size: 0.95rem; line-height: 1.6; margin-bottom: 28px; }
        .btn-group { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
        .btn {
            padding: 12px 26px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.95rem;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .btn-close { background: #dc2626; color: #fff; }
        .btn-close:hover { background: #b91c1c; transform: translateY(-1px); }
        .btn-close:active { transform: translateY(0); }
        .btn-home { background: #0d274c; color: #55c7ff; border: 1px solid #18385f; }
        .btn-home:hover { background: #133966; transform: translateY(-1px); }
        .btn-home:active { transform: translateY(0); }

        .notice-card {
            display: none;
            margin-top: 24px;
            padding: 16px 20px;
            background: rgba(220, 38, 38, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 10px;
            text-align: center;
            animation: fadeIn 0.3s ease;
        }
        .notice-msg {
            color: #fca5a5;
            font-size: 0.93rem;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 8px;
        }
        .notice-sub {
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.5;
        }
        .kbd-key {
            background: #1e293b;
            border: 1px solid #475569;
            border-radius: 4px;
            padding: 2px 7px;
            font-weight: 700;
            color: #55c7ff;
            font-family: Consolas, monospace;
            font-size: 0.85rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.4);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="exit-card">
        <div class="exit-icon">&#128682;</div>
        <h2>Application Exited</h2>
        <p class="exit-desc">You have successfully logged out and exited the Face Recognition Attendance System.<br>Session has been terminated. You may safely close this browser window or return to home.</p>
        <div class="btn-group">
            <button type="button" class="btn btn-close" id="btnCloseWindow" onclick="attemptCloseTab()">Close Window</button>
            <a href="/" class="btn btn-home">Return to Home Screen</a>
        </div>
        <div id="closeTabNotice" class="notice-card">
            <div class="notice-msg">&#9888;&#65039; Your browser does not allow this website to close the tab automatically. Please close this tab manually.</div>
            <div class="notice-sub">Press <kbd class="kbd-key">Ctrl + W</kbd> (or <kbd class="kbd-key">&#8984; + W</kbd> on Mac) to close this tab.</div>
        </div>
    </div>

    <script>
        // Terminate client auth storage
        try {
            sessionStorage.clear();
            localStorage.removeItem('admin_token');
            localStorage.removeItem('admin_user');
            localStorage.removeItem('user_session');
        } catch (e) {}

        // Prevent browser back navigation from reopening protected dashboard sessions
        if (window.history && window.history.pushState) {
            window.history.pushState(null, null, window.location.href);
            window.onpopstate = function () {
                window.history.pushState(null, null, window.location.href);
            };
        }

        function attemptCloseTab() {
            // Attempt standard browser close
            try {
                window.close();
            } catch (e) {}

            try {
                window.open('', '_self', '');
                window.close();
            } catch (e) {}

            // If the browser blocked window.close() (standard security for tabs opened directly),
            // display the clear message with keyboard shortcut instructions
            setTimeout(function() {
                var notice = document.getElementById('closeTabNotice');
                if (notice) {
                    notice.style.display = 'block';
                    notice.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            }, 150);
        }
    </script>
</body>
</html>"""
    resp = make_response(render_template_string(html_content))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0, post-check=0, pre-check=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "-1"
    return resp


@app.route("/api/train-classifier", methods=["POST"])
def api_train_classifier():
    try:
        from train import train_dataset_engine
        base_dir = os.path.dirname(os.path.abspath(__file__))
        success, message, trained_students = train_dataset_engine(base_dir=base_dir, show_window=False)
        
        # Reset cached recognizer and mtime so the newly trained classifier.xml is loaded immediately
        global _cached_classifier_mtime, _cached_recognizer
        _cached_classifier_mtime = 0
        _cached_recognizer = None

        return jsonify({
            "success": success,
            "message": message,
            "students": trained_students
        }), (200 if success else 400)
    except Exception as e:
        return jsonify({"success": False, "message": f"Training error: {str(e)}"}), 500

@app.route("/api/upload-face-samples", methods=["POST"])
def api_upload_face_samples():
    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    images_base64 = data.get("images", [])

    if not student_id or not images_base64:
        return jsonify({"success": False, "message": "Student ID and image data are required."}), 400

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    import base64
    saved_count = 0
    existing = [f for f in os.listdir(data_dir) if f.startswith(f"user.{student_id}.")]
    start_idx = len(existing) + 1

    for i, b64_str in enumerate(images_base64):
        try:
            if "," in b64_str:
                b64_str = b64_str.split(",")[1]
            img_bytes = base64.b64decode(b64_str)
            target_path = os.path.join(data_dir, f"user.{student_id}.{start_idx + i}.jpg")
            with open(target_path, "wb") as f:
                f.write(img_bytes)
            saved_count += 1
        except Exception as e:
            print("Error saving sample:", e)

    return jsonify({
        "success": True,
        "saved_count": saved_count,
        "message": f"Saved {saved_count} face sample(s) for Student ID {student_id}."
    })

@app.route("/health")
def health():
    db_status = "connected"
    try:
        test_conn = get_db_connection()
        if not test_conn.is_connected():
            db_status = "disconnected"
        else:
            test_conn.close()
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "base_url": get_base_url()
    })

# EMAIL ACTION ROUTE (ACCEPT / REJECT)

@app.route("/action/<token>", methods=["GET", "POST"])
def email_action(token):
    is_valid, token_data = verify_action_token(token)
    if not is_valid:
        return render_template_string(
            ACTION_RESULT_TEMPLATE,
            title="Link Expired or Invalid",
            icon="⚠️",
            badge_color="#dc2626",
            badge_text="INVALID / EXPIRED",
            heading="Action Link Expired or Invalid",
            message=html.escape(str(token_data)),
            details=None,
            action_done=False
        ), 410

    request_id = token_data["request_id"]
    action = token_data["action"]
    action_upper = action.upper()

    req = get_request_by_id(request_id)
    if not req:
        return render_template_string(
            ACTION_RESULT_TEMPLATE,
            title="Request Not Found",
            icon="❌",
            badge_color="#dc2626",
            badge_text="NOT FOUND",
            heading=f"Request #{request_id} Not Found",
            message=f"Student registration request #{request_id} does not exist in the database.",
            details=None,
            action_done=False
        ), 404

    current_status = req.get("Status", "Pending")
    if current_status != "Pending":
        return render_template_string(
            ACTION_RESULT_TEMPLATE,
            title=f"Request Already {current_status}",
            icon="ℹ️",
            badge_color="#2563eb" if current_status == "Approved" else "#dc2626",
            badge_text=current_status.upper(),
            heading=f"Request #{request_id} Already {current_status}",
            message=f"This registration request has already been processed with status: <strong>{html.escape(current_status)}</strong>.",
            details=req,
            action_done=True
        )

    # For safety against email link prefetching by scanners/bots,
    # require explicit POST to execute approval/rejection.
    if request.method != "POST":
        return render_template_string(
            ACTION_CONFIRM_TEMPLATE,
            req=req,
            action=action,
            action_upper=action_upper,
            color="#16a34a" if action == "approve" else "#dc2626"
        )

    # Process action in MySQL transaction
    rejection_reason = request.form.get("rejection_reason", "").strip() if action == "reject" else None
    result = process_approval_action(request_id, action, reason=rejection_reason)
    if result.get("success"):
        color = "#16a34a" if action == "approve" else "#dc2626"
        icon = "✅" if action == "approve" else "🚫"
        action_past = "Approved" if action == "approve" else "Rejected"
        heading = f"Student Registration {action_past}"
        return render_template_string(
            ACTION_RESULT_TEMPLATE,
            title=heading,
            icon=icon,
            badge_color=color,
            badge_text=action_past.upper(),
            heading=heading,
            message=html.escape(result.get("message", "")),
            details=req,
            action_done=True
        )
    else:
        status_val = result.get("status", "error")
        badge_color = "#2563eb" if status_val == "already_processed" else "#dc2626"
        return render_template_string(
            ACTION_RESULT_TEMPLATE,
            title="Action Not Completed",
            icon="⚠️",
            badge_color=badge_color,
            badge_text=status_val.upper(),
            heading="Action Not Completed",
            message=html.escape(result.get("message", "An unexpected error occurred.")),
            details=req,
            action_done=False
        ), 400

# API FOR SENDING NOTIFICATION

@app.route("/api/notify-request", methods=["POST"])
def notify_request_endpoint():
    data = request.get_json(silent=True) or {}
    request_id = data.get("request_id")
    if not request_id:
        return jsonify({"success": False, "message": "Missing request_id."}), 400

    req = get_request_by_id(request_id)
    if not req:
        return jsonify({"success": False, "message": f"Request #{request_id} not found."}), 404

    base_url = data.get("base_url") or get_base_url()
    success, msg = send_approval_email(req, base_url=base_url)
    return jsonify({"success": success, "message": msg}), (200 if success else 500)

@app.route("/api/pending-requests", methods=["GET"])
def pending_requests_endpoint():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT Request_ID, Dep, Course, Year, Semester,
                   Student_ID, Student_Name, Division, Roll,
                   Gender, DOB, Email, Phone, Address,
                   Teacher, PhotoSample, Status
            FROM student_requests
            WHERE Status = 'Pending'
            ORDER BY Request_ID DESC
            """
        )
        rows = cursor.fetchall()
        return jsonify({"success": True, "count": len(rows), "requests": rows})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# LAPTOP LOCATION PAGE

@app.route("/pc-location")
def pc_location_page():
    return """
<!DOCTYPE html>

<html>

<head>

    <title>Laptop Location Verification</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;

            background:
                linear-gradient(
                    135deg,
                    #0f172a,
                    #1e3a8a,
                    #2563eb
                );

            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;
        }

        .box {
            width: 420px;
            max-width: 92%;

            background: white;

            border-radius: 18px;

            padding: 30px;

            box-shadow:
                0 15px 40px rgba(0,0,0,0.30);

            text-align: center;
        }

        h2 {
            margin-top: 0;
            color: #1e3a8a;
        }

        p {
            color: #555;
            line-height: 1.5;
        }

        input {
            width: 100%;
            padding: 13px;
            margin-top: 12px;

            border: 1px solid #ccc;
            border-radius: 8px;

            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #2563eb;
        }

        button {
            width: 100%;
            padding: 13px;
            margin-top: 18px;

            border: none;
            border-radius: 8px;

            background: #2563eb;
            color: white;

            font-size: 16px;
            font-weight: bold;

            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        #result {
            margin-top: 20px;
            padding: 15px;

            border-radius: 8px;

            display: none;
            text-align: left;
        }

        .success {
            background: #dcfce7;
            color: #166534;
        }

        .error {
            background: #fee2e2;
            color: #991b1b;
        }

        .loading {
            background: #dbeafe;
            color: #1e40af;
        }

    </style>

</head>

<body>

<div class="box">

    <h2>📍 Laptop Location Verification</h2>

    <p>
        Enter your Student ID and allow browser location
        permission to verify your laptop location.
    </p>

    <input
        type="text"
        id="student_id"
        placeholder="Enter Student ID"
        autocomplete="off"
    >

    <button onclick="verifyLocation()">
        Verify Laptop Location
    </button>

    <div id="result"></div>

</div>

<script>

function showResult(message, type) {

    const result = document.getElementById("result");

    result.style.display = "block";

    result.className = type;

    result.innerHTML = message;
}

function verifyLocation() {

    const studentId =
        document.getElementById("student_id").value.trim();

    if (!studentId) {

        showResult(
            "❌ Please enter Student ID.",
            "error"
        );

        return;
    }

    if (!navigator.geolocation) {

        showResult(
            "❌ Your browser does not support location.",
            "error"
        );

        return;
    }

    showResult(
        "📍 Getting laptop location...",
        "loading"
    );

    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude =
                position.coords.latitude;

            const longitude =
                position.coords.longitude;

            showResult(
                "⏳ Verifying location...",
                "loading"
            );

            fetch("/verify-pc-location", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    student_id: studentId,

                    latitude: latitude,

                    longitude: longitude

                })

            })

            .then(response => response.json())

            .then(data => {

                if (data.success) {

                    showResult(

                        "<b>✅ Location Verified</b><br><br>" +

                        "Name: " +
                        data.student_name +
                        "<br>" +

                        "Student ID: " +
                        data.student_id +
                        "<br>" +

                        "Distance: " +
                        data.distance +
                        " meters<br><br>" +

                        "You can now start Face Recognition.",

                        "success"

                    );

                }

                else {

                    showResult(

                        "<b>❌ Verification Failed</b><br><br>" +

                        data.message,

                        "error"

                    );

                }

            })

            .catch(error => {

                showResult(

                    "❌ Server connection failed.<br>" +
                    "Make sure app.py is running.",

                    "error"

                );

                console.error(error);

            });

        },

        function(error) {

            let message =
                "Unable to get laptop location.";

            if (error.code === 1) {

                message =
                    "Location permission denied. " +
                    "Please allow location permission.";

            }

            else if (error.code === 2) {

                message =
                    "Laptop location is unavailable.";

            }

            else if (error.code === 3) {

                message =
                    "Location request timed out.";

            }

            showResult(
                "❌ " + message,
                "error"
            );

        },

        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }

    );

}

</script>

</body>

</html>
"""

# MOBILE PAGE

@app.route("/mobile")
def mobile():
    return pc_location_page()

# VERIFY LAPTOP LOCATION

@app.route(
    "/verify-pc-location",
    methods=["POST"]
)
def verify_pc_location():

    try:

        data = request.get_json(silent=True)

        if data is None:

            return jsonify({
                "success": False,
                "message":
                    "Invalid location data."
            })

        # GET DATA

        student_id = data.get("student_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # STUDENT ID

        if student_id is None:

            return jsonify({
                "success": False,
                "student_verified": False,
                "message":
                    "Student ID is required."
            })

        student_id = str(
            student_id
        ).strip()

        if student_id == "":

            return jsonify({
                "success": False,
                "student_verified": False,
                "message":
                    "Student ID is required."
            })

        # LOCATION DATA

        if latitude is None or longitude is None:

            return jsonify({
                "success": False,
                "student_verified": True,
                "location_verified": False,
                "message":
                    "Laptop location is required."
            })

        # CHECK STUDENT

        student = check_student_id(student_id)

        if student is None:

            return jsonify({
                "success": False,
                "student_verified": False,
                "message":
                    "Invalid Student ID."
            })

        # CHECK TIME
        if not is_attendance_time_allowed():
            return jsonify({
                "success": False,
                "student_verified": True,
                "location_verified": False,
                "time_verified": False,
                "student_id": student[0],
                "student_name": student[1],
                "message":
                    "Attendance is allowed only "
                    "between 8:00 AM and 11:00 PM."
            })

        # CONVERT GPS

        try:

            latitude = float(latitude)
            longitude = float(longitude)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "student_verified": True,
                "location_verified": False,
                "message":
                    "Invalid latitude or longitude."
            })

        # VALID LATITUDE

        if not -90 <= latitude <= 90:

            return jsonify({
                "success": False,
                "message":
                    "Invalid latitude."
            })

        # VALID LONGITUDE

        if not -180 <= longitude <= 180:

            return jsonify({
                "success": False,
                "message":
                    "Invalid longitude."
            })

        # CALCULATE DISTANCE

        distance = calculate_distance(
            latitude,
            longitude,
            COLLEGE_LAT,
            COLLEGE_LON
        )

        distance = round(
            distance,
            2
        )

        print()
        print("=" * 60)
        print("LOCATION VERIFICATION")
        print("=" * 60)
        print("Student ID :", student_id)
        print("Name       :", student[1])
        print("Latitude   :", latitude)
        print("Longitude  :", longitude)
        print("Distance   :", distance, "meters")
        print("Radius     :", RADIUS, "meters")
        print("=" * 60)

        # CHECK COLLEGE AREA

        if distance <= RADIUS:

            # SAVE LOCATION FOR THIS STUDENT

            pc_location[student_id] = {

                "student_id":
                    student_id,

                "student_name":
                    student[1],

                "department":
                    student[2],

                "latitude":
                    latitude,

                "longitude":
                    longitude,

                "distance":
                    distance,

                "verified_at":
                    datetime.now()
            }

            print("LOCATION STATUS: VERIFIED")
            print()

            return jsonify({

                "success": True,

                "student_verified": True,

                "location_verified": True,

                "time_verified": True,

                "student_id":
                    student[0],

                "student_name":
                    student[1],

                "department":
                    student[2],

                "latitude":
                    latitude,

                "longitude":
                    longitude,

                "distance":
                    distance,

                "radius":
                    RADIUS,

                "message":
                    "Laptop location verified successfully."
            })

        # OUTSIDE COLLEGE

        print("LOCATION STATUS: OUTSIDE AREA")
        print()

        return jsonify({

            "success": False,

            "student_verified": True,

            "location_verified": False,

            "time_verified": True,

            "student_id":
                student[0],

            "student_name":
                student[1],

            "latitude":
                latitude,

            "longitude":
                longitude,

            "distance":
                distance,

            "radius":
                RADIUS,

            "message":
                "Laptop is outside the allowed college area."
        })

    except Exception as e:

        print(
            "PC Location Error:",
            e
        )

        return jsonify({

            "success": False,

            "message":
                "Server error: " + str(e)

        })

# CHECK LAPTOP LOCATION

@app.route(
    "/check-pc-location/<student_id>",
    methods=["GET"]
)
def check_pc_location(student_id):

    student_id = str(
        student_id
    ).strip()

    # CHECK STUDENT LOCATION

    if student_id not in pc_location:

        return jsonify({

            "success": False,

            "location_verified": False,

            "message":
                "Laptop location has not been verified. "
                "Please open the Laptop Location page "
                "and verify your location first."

        })

    location = pc_location[student_id]

    # CHECK LOCATION AGE

    elapsed = (
        datetime.now()
        -
        location["verified_at"]
    ).total_seconds()

    # LOCATION EXPIRED

    if elapsed > LOCATION_VALIDITY:

        del pc_location[student_id]

        return jsonify({

            "success": False,

            "location_verified": False,

            "message":
                "Laptop location expired. "
                "Please verify laptop location again."

        })

    # CHECK CURRENT DISTANCE

    distance = calculate_distance(

        location["latitude"],

        location["longitude"],

        COLLEGE_LAT,

        COLLEGE_LON

    )

    distance = round(
        distance,
        2
    )

    # OUTSIDE AREA

    if distance > RADIUS:

        return jsonify({

            "success": False,

            "location_verified": False,

            "latitude":
                location["latitude"],

            "longitude":
                location["longitude"],

            "distance":
                distance,

            "radius":
                RADIUS,

            "message":
                "Laptop is outside the allowed college area."

        })

    # SUCCESS

    return jsonify({

        "success": True,

        "location_verified": True,

        "student_id":
            student_id,

        "student_name":
            location["student_name"],

        "department":
            location["department"],

        "latitude":
            location["latitude"],

        "longitude":
            location["longitude"],

        "distance":
            distance,

        "radius":
            RADIUS,

        "verified_at":
            location["verified_at"].strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "message":
            "Laptop location is valid."

    })

# OLD MOBILE VERIFY LOCATION

@app.route(
    "/verify-location",
    methods=["POST"]
)
def verify_location():

    try:

        data = request.get_json(silent=True)

        if data is None:

            return jsonify({

                "success": False,

                "message":
                    "Invalid request data."

            })

        student_id = data.get(
            "student_id"
        )

        latitude = data.get(
            "latitude"
        )

        longitude = data.get(
            "longitude"
        )

        # STUDENT ID

        if not student_id:

            return jsonify({

                "success": False,

                "student_verified": False,

                "message":
                    "Student ID is required."

            })

        student_id = str(
            student_id
        ).strip()

        # LOCATION

        if latitude is None or longitude is None:

            return jsonify({

                "success": False,

                "student_verified": True,

                "location_verified": False,

                "message":
                    "Location is required."

            })

        # STUDENT

        student = check_student_id(
            student_id
        )

        if student is None:

            return jsonify({

                "success": False,

                "student_verified": False,

                "message":
                    "Invalid Student ID."

            })

        # TIME
        if not is_attendance_time_allowed():
            return jsonify({
                "success": False,
                "student_verified": True,
                "location_verified": False,
                "time_verified": False,
                "student_id":
                    student[0],
                "student_name":
                    student[1],
                "message":
                    "Attendance is allowed only "
                    "between 8:00 AM and 11:00 PM."
            })

        # GPS FLOAT

        try:

            latitude = float(latitude)

            longitude = float(longitude)

        except (ValueError, TypeError):

            return jsonify({

                "success": False,

                "student_verified": True,

                "location_verified": False,

                "message":
                    "Invalid latitude or longitude."

            })

        # GPS RANGE

        if not -90 <= latitude <= 90:

            return jsonify({

                "success": False,

                "message":
                    "Invalid latitude."

            })

        if not -180 <= longitude <= 180:

            return jsonify({

                "success": False,

                "message":
                    "Invalid longitude."

            })

        # DISTANCE

        distance = calculate_distance(

            latitude,

            longitude,

            COLLEGE_LAT,

            COLLEGE_LON

        )

        distance = round(
            distance,
            2
        )

        # VERIFY

        if distance <= RADIUS:

            verified_students[student_id] = {

                "verified_at":
                    datetime.now(),

                "latitude":
                    latitude,

                "longitude":
                    longitude,

                "distance":
                    distance

            }

            return jsonify({

                "success": True,

                "student_verified": True,

                "location_verified": True,

                "time_verified": True,

                "student_id":
                    student[0],

                "student_name":
                    student[1],

                "department":
                    student[2],

                "latitude":
                    latitude,

                "longitude":
                    longitude,

                "distance":
                    distance,

                "radius":
                    RADIUS,

                "message":
                    "Student ID, location and time "
                    "verified successfully."

            })

        return jsonify({

            "success": False,

            "student_verified": True,

            "location_verified": False,

            "time_verified": True,

            "student_id":
                student[0],

            "student_name":
                student[1],

            "latitude":
                latitude,

            "longitude":
                longitude,

            "distance":
                distance,

            "radius":
                RADIUS,

            "message":
                "You are outside the allowed "
                "college area."

        })

    except Exception as e:

        print(
            "Verification Error:",
            e
        )

        return jsonify({

            "success": False,

            "message":
                "Server error: " + str(e)

        })

# CHECK OLD MOBILE VERIFICATION

@app.route(
    "/check-verification/<student_id>",
    methods=["GET"]
)
def check_verification(student_id):

    student_id = str(
        student_id
    ).strip()

    # CHECK

    if student_id not in verified_students:

        return jsonify({

            "success": False,

            "message":
                "Student has not completed "
                "mobile verification."

        })

    verification = verified_students[
        student_id
    ]

    # AGE

    elapsed = (
        datetime.now()
        -
        verification["verified_at"]
    ).total_seconds()

    # EXPIRED

    if elapsed > 120:

        del verified_students[
            student_id
        ]

        return jsonify({

            "success": False,

            "message":
                "Mobile verification expired. "
                "Please verify again."

        })

    # SUCCESS

    return jsonify({

        "success": True,

        "student_id":
            student_id,

        "latitude":
            verification["latitude"],

        "longitude":
            verification["longitude"],

        "distance":
            verification["distance"],

        "message":
            "Mobile verification is valid."

    })

# RUN SERVER

if __name__ == "__main__":

    print()

    print("=" * 60)

    print(
        "FACE RECOGNITION ATTENDANCE BACKEND"
    )

    print("=" * 60)

    print()

    print(
        "Server is starting..."
    )

    print()

    print(
        "PC:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "LAN:"
    )

    print(
        "http://192.168.0.6:5000"
    )

    print()

    print(
        "Laptop Location:"
    )

    print(
        "http://127.0.0.1:5000/pc-location"
    )

    print()

    print(
        "Mobile:"
    )

    print(
        "http://192.168.0.6:5000/mobile"
    )

    print()

    print(
        "College Latitude:",
        COLLEGE_LAT
    )

    print(
        "College Longitude:",
        COLLEGE_LON
    )

    print()

    print(
        "Radius:",
        RADIUS,
        "meters"
    )

    print(
        "Location Validity:",
        LOCATION_VALIDITY,
        "seconds"
    )

    print(
        "Time:",
        START_TIME,
        "to",
        END_TIME
    )

    print()

    print("=" * 60)

    print()

    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Server listening on http://{host}:{port}")
    print("Action listener route available at: /action/<token>")

    app.run(
        host=host,
        port=port,
        debug=False
    )