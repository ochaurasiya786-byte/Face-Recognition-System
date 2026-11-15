"""
Initialize or migrate tables to the Cloud MySQL Database (Aiven / Remote).
Run this script once after updating your .env file with Aiven credentials:
    python init_cloud_db.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv(Path(__file__).resolve().parent / ".env")

from approval_service import get_db_connection, get_db_config

def init_database():
    cfg = get_db_config()
    print("=" * 60)
    print("CLOUD DATABASE INITIALIZER")
    print("=" * 60)
    print(f"Connecting to: {cfg['host']}:{cfg['port']}")
    print(f"Database:      {cfg['database']}")
    print(f"User:          {cfg['user']}")
    print("-" * 60)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("Connected successfully to Cloud MySQL!")

        # 1. Admin Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                Admin_ID INT NOT NULL AUTO_INCREMENT,
                Username VARCHAR(50) NOT NULL,
                Password VARCHAR(100) NOT NULL,
                PRIMARY KEY (Admin_ID),
                UNIQUE KEY Username (Username)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("Table 'admin' verified.")

        # 2. Student Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                Dep VARCHAR(50) DEFAULT NULL,
                Course VARCHAR(50) DEFAULT NULL,
                Year VARCHAR(20) DEFAULT NULL,
                Semester VARCHAR(20) DEFAULT NULL,
                Student_ID INT DEFAULT NULL,
                Student_Name VARCHAR(50) DEFAULT NULL,
                Division VARCHAR(20) DEFAULT NULL,
                Roll VARCHAR(20) DEFAULT NULL,
                Gender VARCHAR(20) DEFAULT NULL,
                DOB VARCHAR(20) DEFAULT NULL,
                Email VARCHAR(50) DEFAULT NULL,
                Phone VARCHAR(20) DEFAULT NULL,
                Address VARCHAR(100) DEFAULT NULL,
                Teacher VARCHAR(50) DEFAULT NULL,
                PhotoSample VARCHAR(10) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("Table 'student' verified.")

        # 3. Student Requests Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_requests (
                Request_ID INT NOT NULL AUTO_INCREMENT,
                Dep VARCHAR(100) DEFAULT NULL,
                Course VARCHAR(100) DEFAULT NULL,
                Year VARCHAR(50) DEFAULT NULL,
                Semester VARCHAR(50) DEFAULT NULL,
                Student_ID VARCHAR(50) DEFAULT NULL,
                Student_Name VARCHAR(100) DEFAULT NULL,
                Division VARCHAR(50) DEFAULT NULL,
                Roll VARCHAR(50) DEFAULT NULL,
                Gender VARCHAR(50) DEFAULT NULL,
                DOB VARCHAR(50) DEFAULT NULL,
                Email VARCHAR(100) DEFAULT NULL,
                Phone VARCHAR(50) DEFAULT NULL,
                Address VARCHAR(255) DEFAULT NULL,
                Teacher VARCHAR(100) DEFAULT NULL,
                PhotoSample VARCHAR(50) DEFAULT 'No',
                Status VARCHAR(20) DEFAULT 'Pending',
                PRIMARY KEY (Request_ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("Table 'student_requests' verified.")

        # Insert default Admin if missing
        cursor.execute("SELECT COUNT(*) FROM admin WHERE Username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO admin (Username, Password) VALUES (%s, %s)",
                ("admin", "Admin@123")
            )
            conn.commit()
            print("Default admin created: Username='admin', Password='Admin@123'")

        conn.commit()
        print("-" * 60)
        print("SUCCESS: Your cloud database is initialized and ready to use!")
        print("=" * 60)

    except Exception as e:
        print(f"Error connecting or initializing cloud database: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    init_database()

