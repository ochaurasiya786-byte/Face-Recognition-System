import os
import html
from flask import Flask, request, jsonify, render_template_string
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
    get_base_url
)

# Load environment configuration
load_dotenv()

app = Flask(__name__)

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
                Dep
            FROM student
            WHERE Student_ID=%s
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

# HOME & HEALTH CHECKS

@app.route("/")
def home():
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

    # If GET and auto execution is not requested, show the review/confirmation card
    is_auto = (
        request.args.get("auto") in ("1", "true", "yes")
        or request.args.get("confirm") in ("1", "true", "yes")
    )

    if request.method == "GET" and not is_auto:
        return render_template_string(
            ACTION_CONFIRM_TEMPLATE,
            req=req,
            action=action,
            action_upper=action_upper,
            color="#16a34a" if action == "approve" else "#dc2626"
        )

    # Process action in MySQL transaction
    result = process_approval_action(request_id, action)
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

        current_time = datetime.now().time()

        start_time = datetime.strptime(
            START_TIME,
            "%H:%M"
        ).time()

        end_time = datetime.strptime(
            END_TIME,
            "%H:%M"
        ).time()

        if (
            current_time < start_time
            or current_time >= end_time
        ):

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

        current_time = datetime.now().time()

        start_time = datetime.strptime(
            START_TIME,
            "%H:%M"
        ).time()

        end_time = datetime.strptime(
            END_TIME,
            "%H:%M"
        ).time()

        if (
            current_time < start_time
            or current_time >= end_time
        ):

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