"""
AI Help Desk Assistant Knowledge Base & Intelligent Query Engine
Contains comprehensive project documentation across Sections A-F,
accurately distinguishing implemented algorithms (Haar Cascade + LBPH)
from theoretical alternatives (CNN / Deep Learning).
"""

import re

# Comprehensive Knowledge Base Entries
KNOWLEDGE_BASE = [
    # ==========================================
    # SECTION A: PROJECT INTRODUCTION
    # ==========================================
    {
        "id": "what_is_system",
        "category": "Project Introduction",
        "keywords": ["what is an ai-based", "what is this project", "face recognition attendance system", "about this project", "system overview", "project introduction"],
        "title": "What is an AI-Based Face Recognition Attendance System?",
        "answer": (
            "<strong>AI-Based Face Recognition Attendance System</strong> is an automated, contactless biometric "
            "attendance management platform. It uses computer vision and machine learning algorithms (specifically "
            "<strong>Haar Cascade</strong> for face detection and <strong>LBPH</strong> for face recognition) to "
            "verify a student's facial biometrics in real-time via camera, validate their physical campus location via GPS "
            "geofencing, and record attendance securely in a cloud MySQL database without manual paper roll-calls."
        )
    },
    {
        "id": "main_objective",
        "category": "Project Introduction",
        "keywords": ["main objective", "goal of project", "aim of this project", "purpose of project", "objective"],
        "title": "What is the main objective of this project?",
        "answer": (
            "<strong>Main Objectives:</strong><br>"
            "<ul>"
            "<li><strong>Automate Biometric Attendance:</strong> Eliminate manual paper attendance registers and roll-call time loss.</li>"
            "<li><strong>Prevent Proxy & Fraud:</strong> Guarantee only the genuine student can mark their attendance using 1:1 facial biometric matching and anti-spoofing liveness checks.</li>"
            "<li><strong>Location Verification:</strong> Enforce a 4 km campus geofence to ensure physical presence inside college boundaries.</li>"
            "<li><strong>Instant Transparency:</strong> Provide students and faculty with immediate digital attendance logs and real-time administrative oversight.</li>"
            "</ul>"
        )
    },
    {
        "id": "problems_solved",
        "category": "Project Introduction",
        "keywords": ["problems does this project solve", "problems solved", "why needed", "traditional attendance problems", "paper attendance issues"],
        "title": "What problems does this project solve?",
        "answer": (
            "<strong>Problems Solved:</strong><br>"
            "<ul>"
            "<li><strong>Proxy Attendance:</strong> Stops students from answering roll-calls or signing attendance sheets for absent friends.</li>"
            "<li><strong>Time Wastage:</strong> Saves 10–15 minutes per lecture previously spent calling 60+ student names manually.</li>"
            "<li><strong>Human Error & Tampering:</strong> Prevents altered paper sheets, lost registers, or inaccurate manual data entry.</li>"
            "<li><strong>Buddy Punching / Card Sharing:</strong> Unlike RFID cards or passwords that can be handed to a friend, biological face biometrics cannot be shared.</li>"
            "</ul>"
        )
    },
    {
        "id": "how_system_works",
        "category": "Project Introduction",
        "keywords": ["how does the complete system work", "how system works", "workflow", "architecture", "working process"],
        "title": "How does the complete system work?",
        "answer": (
            "<strong>System Workflow:</strong><br>"
            "<ol>"
            "<li><strong>Registration:</strong> Student submits details (ID, Name, Dept, Course, Division). Admin approves the request via email/panel.</li>"
            "<li><strong>Sample Capture:</strong> Webcam captures biometric facial crops into the <code>data/</code> folder.</li>"
            "<li><strong>Model Training:</strong> LBPH algorithm processes samples and generates <code>classifier.xml</code>.</li>"
            "<li><strong>Live Verification:</strong> Student opens the scanner, provides Student ID, and faces the camera.</li>"
            "<li><strong>Detection & Matching:</strong> Haar Cascade detects face; LBPH predicts identity and confidence distance (threshold &le; 65.0).</li>"
            "<li><strong>Security & Geofence:</strong> Eye blink liveness and 4 km GPS radius are validated.</li>"
            "<li><strong>Database Recording:</strong> MySQL database logs <code>PRESENT</code> with student ID, name, date, time, and coordinates.</li>"
            "</ol>"
        )
    },
    {
        "id": "advantages",
        "category": "Project Introduction",
        "keywords": ["advantages of automated attendance", "advantages", "benefits", "pros of face recognition"],
        "title": "What are the advantages of automated attendance?",
        "answer": (
            "<strong>Key Advantages:</strong><br>"
            "<ul>"
            "<li><strong>Contactless & Hygienic:</strong> No physical touch required (unlike fingerprint scanners).</li>"
            "<li><strong>High Speed:</strong> Detects and verifies faces within milliseconds.</li>"
            "<li><strong>High Security:</strong> Anti-proxy dual verification (Student ID + live face matching).</li>"
            "<li><strong>Automated Record Keeping:</strong> Instant exportable attendance records in cloud MySQL.</li>"
            "<li><strong>Cost-Effective:</strong> Operates using ordinary webcams and standard CPU hardware without costly specialized sensors.</li>"
            "</ul>"
        )
    },
    {
        "id": "limitations",
        "category": "Project Introduction",
        "keywords": ["limitations of this project", "limitations", "drawbacks", "disadvantages", "weaknesses"],
        "title": "What are the limitations of this project?",
        "answer": (
            "<strong>Project Limitations:</strong><br>"
            "<ul>"
            "<li><strong>Extreme Lighting:</strong> Very dark environments or intense backlighting can impair Haar Cascade face detection.</li>"
            "<li><strong>Extreme Pose Angles:</strong> Frontal cascade requires faces to be oriented within approximately &plusmn;30 degrees of the camera.</li>"
            "<li><strong>Heavy Occlusions:</strong> Complete face masks or dark sunglasses covering key facial landmarks can prevent recognition.</li>"
            "<li><strong>Camera Quality:</strong> Low-resolution cameras (< 480p) or blurry frames reduce LBPH texture pattern quality.</li>"
            "</ul>"
        )
    },

    # ==========================================
    # SECTION B: PROGRAMMING LANGUAGES & TECH STACK
    # ==========================================
    {
        "id": "why_python",
        "category": "Technologies & Stack",
        "keywords": ["why did we use python", "why python", "python role", "python used"],
        "title": "Why did we use Python in this project?",
        "answer": (
            "<strong>Why Python?</strong><br>"
            "Python is the industry-standard language for Artificial Intelligence and Computer Vision. It provides "
            "mature, high-performance bindings for OpenCV (<code>cv2</code>), NumPy for fast multi-dimensional matrix operations, "
            "native database connectors (<code>mysql-connector-python</code>), and lightweight web frameworks like Flask, "
            "allowing rapid development of reliable end-to-end AI applications."
        )
    },
    {
        "id": "why_html_css_js",
        "category": "Technologies & Stack",
        "keywords": ["why did we use html", "why css", "why javascript", "role of frontend", "frontend technologies"],
        "title": "Why did we use HTML, CSS, and JavaScript?",
        "answer": (
            "<strong>Frontend Technologies:</strong><br>"
            "<ul>"
            "<li><strong>HTML5:</strong> Defines semantic page structure, interactive modals, video streaming tags (<code>&lt;video&gt;</code>), and form inputs.</li>"
            "<li><strong>CSS3:</strong> Powers the modern dark navy glassmorphic user interface, responsive grids, hover animations, and status badges.</li>"
            "<li><strong>JavaScript (Vanilla ES6+):</strong> Captures real-time camera frames via WebRTC <code>navigator.mediaDevices</code>, accesses device GPS coordinates via Geolocation API, and exchanges data with backend REST APIs asynchronously via <code>fetch()</code> without page reloads.</li>"
            "</ul>"
        )
    },
    {
        "id": "why_flask",
        "category": "Technologies & Stack",
        "keywords": ["why did we use flask", "why flask", "flask role", "flask framework", "backend framework"],
        "title": "Why did we use Flask?",
        "answer": (
            "<strong>Why Flask?</strong><br>"
            "Flask is a lightweight, high-performance Python WSGI web framework. Unlike heavy frameworks like Django, "
            "Flask provides minimal overhead, gives precise control over HTTP routes, seamlessly handles real-time JSON REST endpoints "
            "(<code>/api/mark-face-attendance</code>, <code>/api/train-classifier</code>), and integrates directly with OpenCV computer vision pipelines."
        )
    },
    {
        "id": "why_opencv",
        "category": "Technologies & Stack",
        "keywords": ["why did we use opencv", "why opencv", "opencv role", "what does opencv do"],
        "title": "Why did we use OpenCV?",
        "answer": (
            "<strong>Why OpenCV?</strong><br>"
            "OpenCV (Open Source Computer Vision Library) is the leading computer vision library in the world. In this project, "
            "it handles image decoding, BGR-to-grayscale conversion, face bounding box localization with Haar Cascades, "
            "histogram texture extraction with the LBPH Face Recognizer module (<code>cv2.face</code>), and anti-spoofing Laplacian variance calculations."
        )
    },
    {
        "id": "why_mysql",
        "category": "Technologies & Stack",
        "keywords": ["why did we use mysql", "why mysql", "database role", "mysql database", "aiven"],
        "title": "Why did we use MySQL?",
        "answer": (
            "<strong>Why MySQL?</strong><br>"
            "MySQL is a reliable, ACID-compliant relational database. It guarantees structured data integrity for "
            "registered students (<code>student</code> table), pending admissions (<code>student_requests</code> table), "
            "admin credentials (<code>admin</code> table), and time-stamped attendance logs (<code>attendance</code> table). "
            "Hosted on Aiven cloud with SSL, it ensures attendance data is accessible securely from any device."
        )
    },
    {
        "id": "role_of_webcam",
        "category": "Technologies & Stack",
        "keywords": ["role of the webcam", "webcam role", "camera role", "why webcam"],
        "title": "What is the role of the webcam?",
        "answer": (
            "<strong>Role of the Webcam:</strong><br>"
            "The webcam acts as the optical biometric input sensor. In the browser, the WebRTC API captures live video streams at "
            "30 frames per second. Individual frames are converted into base64 image snapshots on a hidden canvas and sent to the "
            "server where computer vision algorithms extract facial features in real time."
        )
    },
    {
        "id": "frontend_backend_comm",
        "category": "Technologies & Stack",
        "keywords": ["how frontend and backend communicate", "client-server communication", "rest api communication", "frontend backend communication"],
        "title": "How do frontend and backend communicate?",
        "answer": (
            "<strong>Client-Server Communication:</strong><br>"
            "The system uses standard <strong>RESTful HTTP APIs</strong> with JSON payloads:<br>"
            "<ul>"
            "<li><strong>Frontend to Backend:</strong> JavaScript collects user inputs, GPS coordinates, and base64 image data, sending them via <code>fetch()</code> using HTTP POST.</li>"
            "<li><strong>Backend to Frontend:</strong> Flask processes requests (e.g. OpenCV matching or database queries) and returns JSON responses containing status flags, student data, and verification distances.</li>"
            "<li><strong>No Full Page Reloads:</strong> Dynamic DOM updates keep the user experience smooth and responsive.</li>"
            "</ul>"
        )
    },

    # ==========================================
    # SECTION C: AI & MACHINE LEARNING ALGORITHMS
    # ==========================================
    {
        "id": "face_detection_algorithm",
        "category": "AI & ML Algorithms",
        "keywords": ["which face detection algorithm is used", "face detection algorithm", "face detector used", "what detects face"],
        "title": "Which face detection algorithm is used in our project?",
        "answer": (
            "<strong>Face Detection in this project:</strong><br>"
            "Our system uses <strong>OpenCV's Haar Feature-based Cascade Classifier</strong> (specifically <code>haarcascade_frontalface_default.xml</code>).<br>"
            "It scans grayscale frames at multiple scales using <code>detectMultiScale()</code> to locate the bounding box (x, y, w, h) of human faces in real time."
        )
    },
    {
        "id": "face_recognition_algorithm",
        "category": "AI & ML Algorithms",
        "keywords": ["which face recognition algorithm is used", "face recognition algorithm", "face recognizer used", "what recognizes face"],
        "title": "Which face recognition algorithm is used?",
        "answer": (
            "<strong>Face Recognition in this project:</strong><br>"
            "Our system uses the <strong>LBPH (Local Binary Patterns Histograms) Face Recognizer</strong> (<code>cv2.face.LBPHFaceRecognizer_create()</code>).<br>"
            "It builds spatial texture histograms for each registered face. During attendance, it computes the feature distance between the live face and the enrolled profile."
        )
    },
    {
        "id": "what_is_haar_cascade",
        "category": "AI & ML Algorithms",
        "keywords": ["what is haar cascade", "haar cascade", "how haar cascade works", "viola jones"],
        "title": "What is Haar Cascade?",
        "answer": (
            "<strong>Haar Cascade Classifier:</strong><br>"
            "Proposed by Paul Viola and Michael Jones, Haar Cascade is an effective object detection approach based on machine learning:<br>"
            "<ul>"
            "<li><strong>Haar-like Features:</strong> Evaluates rectangular pixel contrasts (edge, line, and center-surround features).</li>"
            "<li><strong>Integral Image:</strong> Enables calculating the sum of pixel values in rectangular regions in constant time O(1).</li>"
            "<li><strong>AdaBoost:</strong> Selects the most distinctive features and discards redundant ones.</li>"
            "<li><strong>Attentional Cascade:</strong> Applies simpler classifiers early to quickly discard non-face background regions, achieving real-time speed on CPUs.</li>"
            "</ul>"
        )
    },
    {
        "id": "what_is_lbph",
        "category": "AI & ML Algorithms",
        "keywords": ["what is lbph", "local binary patterns histograms", "how lbph works", "lbph algorithm"],
        "title": "What is LBPH (Local Binary Patterns Histograms)?",
        "answer": (
            "<strong>LBPH Algorithm:</strong><br>"
            "LBPH is a powerful, illumination-resilient texture operator used for biometric face recognition:<br>"
            "<ol>"
            "<li><strong>LBP Calculation:</strong> For every 3x3 pixel neighborhood, it thresholds the 8 surrounding neighbors against the center pixel (1 if &ge; center, else 0), forming an 8-bit binary number.</li>"
            "<li><strong>Decimal Mapping:</strong> The 8-bit binary value is converted into a decimal number (0–255).</li>"
            "<li><strong>Spatial Histograms:</strong> The face is divided into a grid of cells (e.g., 8x8), and a local histogram is computed for each cell.</li>"
            "<li><strong>Feature Vector:</strong> All local histograms are concatenated into a single spatial histogram representing the facial biometrics.</li>"
            "<li><strong>Comparison:</strong> Chi-square or Euclidean distance compares the live face against enrolled histograms.</li>"
            "</ol>"
        )
    },
    {
        "id": "computer_vision_ai_ml",
        "category": "AI & ML Algorithms",
        "keywords": ["what is opencv", "what is computer vision", "what is artificial intelligence", "what is machine learning", "ai vs ml"],
        "title": "What is AI, Machine Learning, Computer Vision, and OpenCV?",
        "answer": (
            "<strong>Definitions & Roles:</strong><br>"
            "<ul>"
            "<li><strong>Artificial Intelligence (AI):</strong> The broad science of creating machines capable of mimicking human cognitive tasks like vision, decision-making, and pattern recognition.</li>"
            "<li><strong>Machine Learning (ML):</strong> A subset of AI where algorithms learn patterns from training data (e.g. face samples) rather than being explicitly hardcoded.</li>"
            "<li><strong>Computer Vision (CV):</strong> An AI discipline enabling computers to acquire, process, analyze, and interpret visual data from cameras and digital images.</li>"
            "<li><strong>OpenCV:</strong> The open-source software library providing optimized algorithms for computer vision and image processing.</li>"
            "</ul>"
        )
    },
    {
        "id": "detection_vs_recognition",
        "category": "AI & ML Algorithms",
        "keywords": ["face detection versus face recognition", "detection vs recognition", "difference between detection and recognition"],
        "title": "What is Face Detection versus Face Recognition?",
        "answer": (
            "<strong>Detection vs Recognition:</strong><br>"
            "<ul>"
            "<li><strong>Face Detection (Haar Cascade):</strong> Answers <em>'Where is a human face in the image?'</em> It locates the coordinates of face boundaries but does NOT know who the person is.</li>"
            "<li><strong>Face Recognition (LBPH):</strong> Answers <em>'Whose face is this?'</em> It extracts biometric feature histograms from the detected face and matches them against enrolled identities to verify identity.</li>"
            "</ul>"
        )
    },
    {
        "id": "matching_distance_threshold",
        "category": "AI & ML Algorithms",
        "keywords": ["what is face matching distance", "recognition threshold", "matching distance", "confidence score", "threshold 65"],
        "title": "What is Face Matching Distance and the Recognition Threshold?",
        "answer": (
            "<strong>Matching Distance & Threshold:</strong><br>"
            "<ul>"
            "<li><strong>Distance Metric:</strong> In LBPH, the confidence score represents mathematical <strong>distance</strong> between histogram feature vectors (not percentage). A <strong>lower number means a closer match</strong> (0 = identical).</li>"
            "<li><strong>Calibrated Threshold (65.0):</strong> In our project, the threshold is calibrated at <strong>65.0</strong>. If the distance is &le; 65.0 and matches the student ID, authentication succeeds. If the distance > 65.0, the system rejects the face as an unknown or unauthorized person.</li>"
            "</ul>"
        )
    },
    {
        "id": "training_dataset_model",
        "category": "AI & ML Algorithms",
        "keywords": ["what is model training", "what is a training dataset", "training dataset", "model training"],
        "title": "What is Model Training and a Training Dataset?",
        "answer": (
            "<strong>Training Concepts:</strong><br>"
            "<ul>"
            "<li><strong>Training Dataset:</strong> A collection of facial image samples captured for each student (stored in the <code>data/</code> directory as <code>user.&lt;student_id&gt;.&lt;sample_num&gt;.jpg</code>).</li>"
            "<li><strong>Model Training:</strong> The computational process where OpenCV's LBPH recognizer reads all face samples, converts them into binary patterns, extracts histograms, and compiles them into a single binary knowledge file <code>classifier.xml</code>.</li>"
            "</ul>"
        )
    },
    {
        "id": "grayscale_processing",
        "category": "AI & ML Algorithms",
        "keywords": ["what is grayscale image processing", "why grayscale", "grayscale processing", "color to grayscale"],
        "title": "What is Grayscale Image Processing and why is it used?",
        "answer": (
            "<strong>Grayscale Image Processing:</strong><br>"
            "Grayscale conversion transforms a 3-channel (Blue, Green, Red) image into a single 1-channel luminance image.<br>"
            "<strong>Why used:</strong><br>"
            "<ul>"
            "<li><strong>3x Computational Speed:</strong> Reduces pixel data volume by 66%, speeding up real-time frame processing.</li>"
            "<li><strong>Illumination Invariance:</strong> Facial biometric features depend on structural shadows and gradients, not skin color or tint.</li>"
            "</ul>"
        )
    },
    {
        "id": "anti_spoofing_fraud",
        "category": "AI & ML Algorithms",
        "keywords": ["what is anti-spoofing", "how does the system prevent fake attendance", "prevent proxy", "spoofing", "liveness"],
        "title": "What is Anti-Spoofing and how does the system prevent fake attendance?",
        "answer": (
            "<strong>Anti-Spoofing & Fraud Prevention:</strong><br>"
            "Our system implements multi-layered security:<br>"
            "<ul>"
            "<li><strong>1:1 Student ID Matching:</strong> The live face must match the specific registered Student ID; guessing or mismatching is blocked.</li>"
            "<li><strong>Laplacian Texture Variance:</strong> Evaluates high-frequency sharpness (<code>cv2.Laplacian</code>) to reject low-resolution mobile screen replays or paper photo prints.</li>"
            "<li><strong>Dynamic Eye-Blink Liveness:</strong> Analyzes temporal frame changes to ensure a real, living human is in front of the camera.</li>"
            "<li><strong>4 km Campus Geofencing:</strong> Haversine formula verifies student GPS coordinates are physically within the college radius.</li>"
            "<li><strong>Once-per-Day Limit:</strong> Duplicate attendance records on the same calendar day are prevented.</li>"
            "</ul>"
        )
    },
    {
        "id": "actual_vs_theoretical_algorithms",
        "category": "AI & ML Algorithms",
        "keywords": ["difference between algorithms used and theoretical", "cnn vs lbph", "deep learning vs haar", "is cnn used", "are we using deep learning"],
        "title": "Which algorithms are ACTUALLY implemented vs THEORETICAL alternatives?",
        "answer": (
            "<strong>Codebase Algorithms vs Theoretical Alternatives:</strong><br>"
            "<ul>"
            "<li><strong>ACTUALLY IMPLEMENTED IN SOURCE CODE:</strong><br>"
            "&bull; <em>Face Detection:</em> <strong>Haar Cascade Classifier</strong> (<code>haarcascade_frontalface_default.xml</code>).<br>"
            "&bull; <em>Face Recognition:</em> <strong>LBPH (Local Binary Patterns Histograms)</strong> (<code>cv2.face.LBPHFaceRecognizer</code>).<br>"
            "&bull; <em>Liveness & Blur Detection:</em> <strong>Laplacian Variance</strong> (<code>cv2.Laplacian</code>) and eye-blink optical variance.</li>"
            "<li><strong>THEORETICAL ALTERNATIVES (Not in code):</strong><br>"
            "&bull; <em>Deep Learning / CNNs (FaceNet, ArcFace, ResNet):</em> Theoretical deep neural networks that output 128-d embeddings. While highly invariant, they require GPU acceleration, large model weights (>100MB), and higher latency.<br>"
            "&bull; <em>Eigenfaces (PCA) & Fisherfaces (LDA):</em> Older linear statistical methods sensitive to illumination.<br>"
            "&bull; <em>YOLO-Face / MTCNN:</em> Deep learning detectors requiring heavy computing overhead.</li>"
            "</ul>"
        )
    },

    # ==========================================
    # SECTION D: STUDENT REGISTRATION & FACE TRAINING
    # ==========================================
    {
        "id": "how_student_registers",
        "category": "Registration & Training",
        "keywords": ["how can a new student register", "how can a student id be created", "student registration steps", "how to register"],
        "title": "How can a new student register?",
        "answer": (
            "<strong>Student Registration Steps:</strong><br>"
            "<ol>"
            "<li>Click <strong>Student Details</strong> on the dashboard.</li>"
            "<li>Fill in the mandatory fields: Student ID, Full Name, Department, Course, Year, Roll Number, Division, and Gender.</li>"
            "<li>Submit the registration request. The system saves the application into <code>student_requests</code> in MySQL and sends an approval notification email to the Admin.</li>"
            "<li>Once the Admin approves the request, the student profile is officially enrolled in the <code>student</code> table.</li>"
            "</ol>"
        )
    },
    {
        "id": "capture_face_samples",
        "category": "Registration & Training",
        "keywords": ["how can a new face be captured", "why do we capture multiple face samples", "why are face samples stored", "face capture"],
        "title": "How are face samples captured and why do we capture multiple samples?",
        "answer": (
            "<strong>Face Sample Capture:</strong><br>"
            "<ul>"
            "<li><strong>How captured:</strong> Under <em>Student Details &rarr; Add New Face</em>, enter the registered Student ID, start the camera, and click <em>Capture Samples</em>. Faces are automatically cropped, converted to grayscale, and saved in the <code>data/</code> folder.</li>"
            "<li><strong>Why multiple samples (e.g. 5–50):</strong> Human faces change with minor head tilts, eye movements, expressions, and lighting changes. Multiple samples allow the LBPH algorithm to construct a robust histogram distribution that reliably recognizes the student under varied conditions.</li>"
            "</ul>"
        )
    },
    {
        "id": "how_to_retrain_model",
        "category": "Registration & Training",
        "keywords": ["how do we train the face recognition model", "when should we retrain the model", "what happens if face training fails", "retrain model", "train model"],
        "title": "How and when do we train the Face Recognition model?",
        "answer": (
            "<strong>Model Training Procedure:</strong><br>"
            "<ul>"
            "<li><strong>How to train:</strong> Click <em>&rarr; Go to Train Data to Retrain Model</em> in the Add Face tab or the Train modal. Click <em>Run AI Model Training Now</em>. The backend processes all images in <code>data/</code> and generates an updated <code>classifier.xml</code> file.</li>"
            "<li><strong>When to retrain:</strong> Retrain whenever a new student registers their face samples, or when an existing student captures updated photos.</li>"
            "<li><strong>If training fails:</strong> Ensure the <code>data/</code> folder contains valid image files named in the format <code>user.&lt;id&gt;.&lt;sample&gt;.jpg</code> and that face crops are clearly visible.</li>"
            "</ul>"
        )
    },

    # ==========================================
    # SECTION E: ATTENDANCE MANAGEMENT
    # ==========================================
    {
        "id": "how_attendance_marked",
        "category": "Attendance Management",
        "keywords": ["how is attendance marked", "mark attendance", "how to attend", "attendance process"],
        "title": "How is attendance marked?",
        "answer": (
            "<strong>Marking Attendance:</strong><br>"
            "<ol>"
            "<li>Click <strong>Face Recognition</strong> on the dashboard.</li>"
            "<li>Enter or select your registered Student ID.</li>"
            "<li>Align your face within the camera reticle in good lighting.</li>"
            "<li>The system verifies liveness (eye-blink), confirms campus GPS coordinates, and compares facial biometrics against <code>classifier.xml</code>.</li>"
            "<li>Upon successful verification, attendance is recorded as <code>PRESENT</code> in MySQL and a success confirmation badge is displayed.</li>"
            "</ol>"
        )
    },
    {
        "id": "student_id_face_matching",
        "category": "Attendance Management",
        "keywords": ["how does student id verification work", "face matching work", "face does not match", "can one student mark for another"],
        "title": "How does Student ID verification & face matching work? Can a student mark for another?",
        "answer": (
            "<strong>Strict 1:1 Biometric Matching:</strong><br>"
            "<ul>"
            "<li><strong>Mechanism:</strong> The system extracts the predicted ID from the face histogram and compares it directly with the entered Student ID.</li>"
            "<li><strong>Mismatched Face:</strong> If Student A enters Student B's ID, the predicted ID will not match, or the confidence distance will exceed 65.0. The system rejects the attempt and marks status as <code>UNMARKED</code>.</li>"
            "<li><strong>No Proxy Allowed:</strong> One student CANNOT mark attendance for another student under any circumstances.</li>"
            "</ul>"
        )
    },
    {
        "id": "present_vs_unmarked",
        "category": "Attendance Management",
        "keywords": ["what does present mean", "what does unmarked mean", "present vs unmarked", "attendance status"],
        "title": "What does PRESENT and UNMARKED mean?",
        "answer": (
            "<strong>Attendance Status Meanings:</strong><br>"
            "<ul>"
            "<li><strong>PRESENT:</strong> Biometric facial features matched the registered student ID with confidence distance &le; 65.0, liveness was confirmed, campus geofence was validated, and attendance was committed to the database.</li>"
            "<li><strong>UNMARKED:</strong> Authentication failed due to an unknown face, ID mismatch, being outside the campus geofence, or no face detected. No attendance is granted.</li>"
            "</ul>"
        )
    },
    {
        "id": "duplicate_prevention_storage",
        "category": "Attendance Management",
        "keywords": ["how is duplicate attendance prevented", "how are attendance records stored", "can an administrator view attendance records"],
        "title": "How is duplicate attendance prevented and how are records stored?",
        "answer": (
            "<strong>Records & Duplicate Prevention:</strong><br>"
            "<ul>"
            "<li><strong>Duplicate Prevention:</strong> Before inserting a record, the backend runs an SQL check for existing entries with the same <code>Student_ID</code> and <code>Attendance_Date</code>. If already present, it alerts: <em>'Attendance already marked for today'</em>.</li>"
            "<li><strong>Database Storage:</strong> Stored in the MySQL <code>attendance</code> table with columns: ID, Name, Roll, Dep, Time, Date, Latitude, Longitude, and Status.</li>"
            "<li><strong>Admin Oversight:</strong> Administrators can view live records in the <strong>Attendance</strong> table modal, filter by date/ID, and export to CSV.</li>"
            "</ul>"
        )
    },

    # ==========================================
    # SECTION F: TECHNICAL & PROJECT VIVA QUESTIONS
    # ==========================================
    {
        "id": "why_choose_project",
        "category": "Viva Questions",
        "keywords": ["why did we choose this project", "why this project", "project motivation", "reason for choosing"],
        "title": "Why did we choose this project?",
        "answer": (
            "<strong>Project Motivation:</strong><br>"
            "Traditional attendance in colleges wastes substantial instruction time and is vulnerable to proxy marking and paper register tampering. "
            "We chose this project to build a modern, contactless, AI-driven solution that demonstrates practical Computer Vision (OpenCV), "
            "Machine Learning (LBPH), Cloud Relational Databases (MySQL), and Secure Web Architecture (Flask) solving a real-world campus problem."
        )
    },
    {
        "id": "what_makes_project_ai",
        "category": "Viva Questions",
        "keywords": ["what makes this project ai-based", "what makes this ai", "how is it ai", "ai component"],
        "title": "What makes this project AI-based?",
        "answer": (
            "<strong>AI Components in this System:</strong><br>"
            "<ul>"
            "<li><strong>Machine Learning Feature Extraction:</strong> The system does not compare raw pixels. It learns local micro-texture spatial representations through Local Binary Patterns (LBPH).</li>"
            "<li><strong>Statistical Pattern Classification:</strong> Calculates probability distributions across histogram feature spaces to classify faces into identity classes.</li>"
            "<li><strong>Automated Computer Vision Detection:</strong> Uses an AdaBoost-trained Haar Cascade attentional cascade to detect human faces in variable frames without human intervention.</li>"
            "<li><strong>Anti-Spoofing Computer Vision:</strong> Uses Laplacian second-order derivative frequency analysis for liveness verification.</li>"
            "</ul>"
        )
    },
    {
        "id": "future_scope",
        "category": "Viva Questions",
        "keywords": ["future scope", "future improvements", "enhancement roadmap", "future work"],
        "title": "What is the future scope and enhancement roadmap of this project?",
        "answer": (
            "<strong>Future Enhancements:</strong><br>"
            "<ul>"
            "<li><strong>Multi-Face Group Attendance:</strong> Recognize entire classrooms simultaneously from an overhead IP camera.</li>"
            "<li><strong>Deep Learning Migration (InsightFace / ArcFace):</strong> Integrate lightweight deep neural networks with edge TPU acceleration for extreme angle invariance.</li>"
            "<li><strong>Infrared / 3D Depth Sensing:</strong> Incorporate depth sensors to provide military-grade anti-spoofing against 3D silicone masks.</li>"
            "<li><strong>Automated Absentee Parent SMS:</strong> Connect Twilio / WhatsApp Business API to notify parents if a student is absent.</li>"
            "</ul>"
        )
    }
]

def get_help_desk_response(user_query: str) -> str:
    """
    Intelligently matches the user's question against the knowledge base
    and returns a structured, beginner-friendly, and technically accurate answer.
    """
    if not user_query or not user_query.strip():
        return (
            "Hello! I am your AI Attendance Assistant. Ask me anything about our project, including:<br>"
            "&bull; <strong>AI & ML Algorithms:</strong> Haar Cascade, LBPH, threshold 65.0, anti-spoofing.<br>"
            "&bull; <strong>Tech Stack:</strong> Python, OpenCV, Flask, MySQL, JavaScript.<br>"
            "&bull; <strong>Attendance & Security:</strong> 1:1 ID matching, campus geofencing, proxy prevention.<br>"
            "&bull; <strong>Viva Questions:</strong> Objectives, architecture, and advantages."
        )

    q = user_query.strip().lower()
    clean_q = re.sub(r"[^\w\s]", " ", q)
    tokens = set(clean_q.split())

    # Direct greetings
    if any(greet in tokens for greet in ["hi", "hello", "hey", "greetings"]):
        return (
            "Hello! I am your AI Attendance Assistant. Ask me anything about our project architecture, "
            "face detection (Haar Cascade), recognition (LBPH), threshold settings (65.0), registration, or viva questions!"
        )

    # Developer questions
    if any(k in q for k in ["developer", "creator", "who made", "author", "developed by"]):
        return (
            "This AI-Based Face Recognition Attendance System was developed by "
            "<strong>Omkar Chaurasiya</strong>, Full Stack Developer & AI Enthusiast (B.Tech CSE), "
            "Khwaja Moinuddin Chishti Language University, Lucknow."
        )

    # Scored search against knowledge base
    best_match = None
    highest_score = 0

    for item in KNOWLEDGE_BASE:
        score = 0
        
        # 1. Exact title or ID match
        if item["title"].lower() in q or q in item["title"].lower():
            score += 50
        
        # 2. Check keyword phrases
        for kw in item["keywords"]:
            if kw in q:
                score += 30
            else:
                kw_tokens = set(kw.split())
                overlap = kw_tokens.intersection(tokens)
                if len(overlap) == len(kw_tokens):
                    score += 20
                elif len(overlap) > 1:
                    score += len(overlap) * 5

        if score > highest_score:
            highest_score = score
            best_match = item

    # If confident match found
    if best_match and highest_score >= 15:
        return (
            f"<div style='margin-bottom:6px;'><span style='background:#1e3a8a;color:#93c5fd;padding:2px 8px;border-radius:10px;font-size:0.75rem;font-weight:700;'>{best_match['category']}</span></div>"
            f"<h4 style='color:#55c7ff;margin:4px 0 8px 0;'>{best_match['title']}</h4>"
            f"<div>{best_match['answer']}</div>"
        )

    # Fallback with structured topic guide
    return (
        "I couldn't find an exact match for your question. Here are key topics I can answer in detail:<br>"
        "<ul>"
        "<li><strong>Algorithms:</strong> Ask <em>'Which face recognition algorithm is used?'</em> or <em>'What is LBPH?'</em></li>"
        "<li><strong>Detection:</strong> Ask <em>'What is Haar Cascade?'</em> or <em>'Detection vs recognition'</em></li>"
        "<li><strong>Threshold & Distance:</strong> Ask <em>'What is face matching distance?'</em></li>"
        "<li><strong>Anti-Spoofing:</strong> Ask <em>'How does the system prevent fake attendance?'</em></li>"
        "<li><strong>Tech Stack:</strong> Ask <em>'Why did we use Python, Flask, OpenCV, or MySQL?'</em></li>"
        "<li><strong>Viva Questions:</strong> Ask <em>'Why did we choose this project?'</em> or <em>'What makes it AI-based?'</em></li>"
        "</ul>"
    )
