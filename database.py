import sqlite3


DB_NAME = "admission.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def create_connection():
    return sqlite3.connect(DB_NAME)


# =========================================================
# CREATE / MIGRATE STUDENT TABLE
# =========================================================

def create_student_table():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS STUDENT (

            student_id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_name TEXT NOT NULL,

            date_of_birth TEXT,

            mobile_number TEXT,

            course TEXT,

            marksheet_uploaded INTEGER DEFAULT 0,

            tc_uploaded INTEGER DEFAULT 0,

            aadhaar_uploaded INTEGER DEFAULT 0,

            community_uploaded INTEGER DEFAULT 0,

            documents_verified INTEGER DEFAULT 0,

            token_number TEXT,

            queue_position INTEGER DEFAULT 0,

            assigned_counter INTEGER,

            assigned_mentor TEXT,

            queue_status TEXT DEFAULT 'Waiting',

            fees_status TEXT DEFAULT 'Pending',

            payment_mode TEXT,

            admission_status TEXT DEFAULT 'Document Verification Pending'

        )
    """)

    cursor.execute("PRAGMA table_info(STUDENT)")

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    new_columns = {

        "marksheet_uploaded":
            "INTEGER DEFAULT 0",

        "tc_uploaded":
            "INTEGER DEFAULT 0",

        "aadhaar_uploaded":
            "INTEGER DEFAULT 0",

        "community_uploaded":
            "INTEGER DEFAULT 0",

        "documents_verified":
            "INTEGER DEFAULT 0",

        "token_number":
            "TEXT",

        "queue_position":
            "INTEGER DEFAULT 0",

        "assigned_counter":
            "INTEGER",

        "assigned_mentor":
            "TEXT",

        "queue_status":
            "TEXT DEFAULT 'Waiting'",

        "fees_status":
            "TEXT DEFAULT 'Pending'",

        "payment_mode":
            "TEXT",

        "admission_status":
            "TEXT DEFAULT 'Document Verification Pending'"
    }

    for column, definition in new_columns.items():

        if column not in columns:

            cursor.execute(
                f"""
                ALTER TABLE STUDENT
                ADD COLUMN {column} {definition}
                """
            )

    conn.commit()
    conn.close()


# =========================================================
# ADD STUDENT
# =========================================================

def add_student(
    name,
    dob,
    mobile,
    course,
    marksheet,
    tc,
    aadhaar,
    community
):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO STUDENT
        (
            student_name,
            date_of_birth,
            mobile_number,
            course,
            marksheet_uploaded,
            tc_uploaded,
            aadhaar_uploaded,
            community_uploaded,
            admission_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        name,
        dob,
        mobile,
        course,
        marksheet,
        tc,
        aadhaar,
        community,
        "Document Verification Pending"
    ))

    conn.commit()

    student_id = cursor.lastrowid

    conn.close()

    return student_id


# =========================================================
# GET ALL STUDENTS
# =========================================================

def get_students():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            student_id,
            student_name,
            date_of_birth,
            mobile_number,
            course,

            marksheet_uploaded,
            tc_uploaded,
            aadhaar_uploaded,
            community_uploaded,

            documents_verified,

            token_number,

            queue_position,

            assigned_counter,

            assigned_mentor,

            queue_status,

            fees_status,

            payment_mode,

            admission_status

        FROM STUDENT

        ORDER BY student_id DESC
    """)

    students = cursor.fetchall()

    conn.close()

    return students


# =========================================================
# VERIFY DOCUMENTS
# =========================================================

def verify_documents(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE STUDENT

        SET
            documents_verified = 1,
            admission_status = 'Documents Verified'

        WHERE student_id = ?
    """, (student_id,))

    conn.commit()
    conn.close()


# =========================================================
# NEXT QUEUE POSITION
# =========================================================

def get_next_queue_position():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(queue_position), 0)

        FROM STUDENT

        WHERE token_number IS NOT NULL
    """)

    max_position = cursor.fetchone()[0]

    conn.close()

    return max_position + 1


# =========================================================
# UPDATE TOKEN
# =========================================================

def update_token(
    student_id,
    token_number,
    queue_position,
    assigned_counter,
    assigned_mentor
):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE STUDENT

        SET

            token_number = ?,

            queue_position = ?,

            assigned_counter = ?,

            assigned_mentor = ?,

            queue_status = 'Waiting',

            admission_status = 'Queue Assigned'

        WHERE student_id = ?
    """, (

        token_number,
        queue_position,
        assigned_counter,
        assigned_mentor,
        student_id
    ))

    conn.commit()
    conn.close()


# =========================================================
# UPDATE QUEUE STATUS
# =========================================================

def update_queue_status(student_id, status):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE STUDENT

        SET queue_status = ?

        WHERE student_id = ?
    """, (status, student_id))

    conn.commit()
    conn.close()


# =========================================================
# UPDATE FEES
# =========================================================

def update_fees(student_id, fees_status, payment_mode):

    conn = create_connection()
    cursor = conn.cursor()

    if fees_status == "Paid":

        admission_status = "Fees Paid"

    else:

        admission_status = "Fees Pending"

    cursor.execute("""
        UPDATE STUDENT

        SET

            fees_status = ?,

            payment_mode = ?,

            admission_status = ?

        WHERE student_id = ?
    """, (

        fees_status,
        payment_mode,
        admission_status,
        student_id
    ))

    conn.commit()
    conn.close()


# =========================================================
# COMPLETE ADMISSION
# =========================================================

def complete_admission(student_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE STUDENT

        SET

            admission_status = 'Admission Completed',

            queue_status = 'Completed'

        WHERE student_id = ?
    """, (student_id,))

    conn.commit()
    conn.close()


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_student_table()

print("Database connected successfully!")