import streamlit as st

from datetime import date

from database import (
    add_student,
    get_students,
    verify_documents,
    update_token,
    get_next_queue_position,
    update_queue_status,
    update_fees,
    complete_admission
)

from ocr import (
    extract_text,
    extract_marksheet_details
)




st.set_page_config(
    page_title="AdmissionFlow",
    page_icon="🎓",
    layout="wide"
)




st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)




weekly_schedule = {

    "Monday": "Subashini",

    "Tuesday": "Megala",

    "Wednesday": "Subashini",

    "Thursday": "Anusha",

    "Friday": "Megala",

    "Saturday": "Vijitha"
}



counter_map = {

    "Subashini": 1,

    "Megala": 2,

    "Anusha": 3,

    "Vijitha": 4
}




if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "role" not in st.session_state:

    st.session_state.role = None



if not st.session_state.logged_in:

    st.title("🎓 AdmissionFlow")

    st.subheader(
        "Smart College Admission Queue Management System"
    )

    st.divider()

    username = st.text_input(
        "👤 Username"
    )

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    role = st.selectbox(
        "Select Role",
        [
            "Student",
            "Staff",
            "Admin"
        ]
    )


    if st.button("🔐 Login"):

        valid = False

        if role == "Student":

            if username == "student" and password == "1234":

                valid = True


        elif role == "Staff":

            if username == "staff" and password == "1234":

                valid = True


        elif role == "Admin":

            if username == "admin" and password == "1234":

                valid = True


        if valid:

            st.session_state.logged_in = True

            st.session_state.role = role

            st.rerun()

        else:

            st.error(
                "❌ Invalid username or password"
            )


    st.info(
        "Demo Login → Username: student / staff / admin | Password: 1234"
    )

    st.stop()



today = date.today().strftime("%A")


if today == "Sunday":

    current_mentor = None

else:

    current_mentor = weekly_schedule.get(today)



st.title("🎓 ADMISSION FLOW")

st.write(
    "📋 Smart College Admission Queue Management System"
)




st.sidebar.success(
    f"Logged in as: {st.session_state.role}"
)


if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.session_state.role = None

    st.rerun()




if today == "Sunday":

    st.warning(
        "🏫 Today is Sunday — College is closed."
    )

else:

    st.success(
        f"📅 {today} → "
        f"👩‍🏫 Today's Mentor: {current_mentor}"
    )




if st.session_state.role == "Student":

    st.header("🎓 Student Admission")


  

    st.subheader("👤 Student Details")


    student_name = st.text_input(
        "Student Name"
    )


    date_of_birth = st.date_input(
        "🎂 Date of Birth",

        min_value=date(1990, 1, 1),

        max_value=date.today(),

        format="DD/MM/YYYY"
    )


    mobile_number = st.text_input(
        "📱 Mobile Number"
    )


    course = st.text_input(
        "🎓 Course"
    )


    st.subheader(
        "📄 Admission Documents"
    )


    marksheet = st.file_uploader(
        "📋 12th Marksheet",
        type=["pdf", "jpg", "jpeg", "png"]
    )


    tc = st.file_uploader(
        "📋 Transfer Certificate",
        type=["pdf", "jpg", "jpeg", "png"]
    )


    aadhaar = st.file_uploader(
        "🪪 Aadhaar Card",
        type=["pdf", "jpg", "jpeg", "png"]
    )


    community = st.file_uploader(
        "📋 Community Certificate",
        type=["pdf", "jpg", "jpeg", "png"]
    )




    if st.button(
        "💾 Save Student Details"
    ):

        if (
            student_name
            and mobile_number
            and course
        ):

            student_id = add_student(

                student_name,

                str(date_of_birth),

                mobile_number,

                course,

                1 if marksheet else 0,

                1 if tc else 0,

                1 if aadhaar else 0,

                1 if community else 0
            )


            st.session_state[
                "current_student_id"
            ] = student_id


            st.success(
                "✅ Student details saved successfully!"
            )


            st.info(
                f"🆔 Application ID: {student_id}"
            )

        else:

            st.warning(
                "⚠️ Please fill all required details."
            )


    # -----------------------------------------------------
    # DOCUMENT STATUS
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "📋 Document Status"
    )


    documents = {

        "📄 12th Marksheet":
            marksheet,

        "📄 Transfer Certificate":
            tc,

        "🪪 Aadhaar Card":
            aadhaar,

        "📄 Community Certificate":
            community
    }


    for document, uploaded in documents.items():

        if uploaded:

            st.write(
                f"{document} — ✅ Uploaded"
            )

        else:

            st.write(
                f"{document} — ❌ Missing"
            )



    if marksheet:

        file_name = marksheet.name.lower()


        if file_name.endswith(
            (".jpg", ".jpeg", ".png")
        ):

            st.divider()

            st.subheader(
                "🔍 Marksheet OCR"
            )


            extracted_text = extract_text(
                marksheet
            )


            st.text_area(
                "Extracted Text",
                extracted_text,
                height=250
            )


            details = extract_marksheet_details(
                extracted_text
            )


            if details:

                st.write(
                    "📌 Extracted Details:"
                )

                st.json(details)


    

    all_documents = (

        marksheet
        and tc
        and aadhaar
        and community
    )


    if all_documents:

        st.success(
            "✅ All required documents uploaded."
        )

    else:

        st.warning(
            "⚠️ Some required documents are missing."
        )


    st.divider()

    st.subheader(
        "🎫 My Admission Status"
    )


    if st.button(
        "🔎 Check Admission Status"
    ):

        students = get_students()


        current_id = (
            st.session_state.get(
                "current_student_id"
            )
        )


        student = None


        for record in students:

            if record[0] == current_id:

                student = record

                break


        if student:

            st.write(
                "👤 Student:",
                student[1]
            )

            st.write(
                "🆔 Application ID:",
                student[0]
            )

            st.write(
                "🎓 Course:",
                student[4]
            )


            # Verification

            if student[9]:

                st.success(
                    "✅ Documents Verified"
                )

            else:

                st.warning(
                    "⏳ Documents Waiting for Verification"
                )


            # Token

            if student[10]:

                st.success(
                    f"🎫 Token: {student[10]}"
                )

                st.info(
                    f"📍 Queue Position: {student[11]}"
                )

                waiting_time = student[11] * 10

                st.write(
                    f"⏱️ Estimated Waiting Time: "
                    f"{waiting_time} minutes"
                )


                if student[12]:

                    st.success(
                        f"🏢 Counter {student[12]}"
                    )


                if student[13]:

                    st.write(
                        f"👩‍🏫 Staff: {student[13]}"
                    )


                st.write(
                    f"👥 Queue Status: "
                    f"{student[14]}"
                )


            # Fees

            st.write(
                f"💰 Fees Status: "
                f"{student[15]}"
            )


            if student[16]:

                st.write(
                    f"💳 Payment Mode: "
                    f"{student[16]}"
                )


            # Admission

            if student[17] == "Admission Completed":

                st.success(
                    "🎉 Admission Completed Successfully!"
                )

            else:

                st.info(
                    f"📌 Admission Status: "
                    f"{student[17]}"
                )


        else:

            st.error(
                "❌ Student record not found."
            )


elif st.session_state.role == "Staff":

    st.header(
        "👩‍🏫 Staff Dashboard"
    )


    students = get_students()


    if not students:

        st.info(
            "ℹ️ No student records available."
        )

    else:

        options = [

            f"{student[1]} "
            f"(Application ID: {student[0]})"

            for student in students
        ]


        selected = st.selectbox(
            "👤 Select Student",
            options
        )


        index = options.index(selected)

        student = students[index]


        st.subheader(
            "👤 Student Details"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "🆔 Application ID:",
                student[0]
            )

            st.write(
                "👤 Name:",
                student[1]
            )

            st.write(
                "🎂 DOB:",
                student[2]
            )


        with col2:

            st.write(
                "📱 Mobile:",
                student[3]
            )

            st.write(
                "🎓 Course:",
                student[4]
            )


        st.divider()

        st.subheader(
            "📄 Document Verification"
        )


        document_status = {

            "12th Marksheet":
                student[5],

            "Transfer Certificate":
                student[6],

            "Aadhaar Card":
                student[7],

            "Community Certificate":
                student[8]
        }


        for name, status in document_status.items():

            st.write(

                f"{name} — "
                f"{'✅ Uploaded' if status else '❌ Missing'}"

            )


        if student[9]:

            st.success(
                "✅ Documents already verified."
            )

        else:

            if st.button(
                "✅ Verify Documents"
            ):

                verify_documents(
                    student[0]
                )

                st.success(
                    "✅ Documents verified successfully!"
                )

                st.rerun()



        if student[9]:

            st.divider()

            st.subheader(
                "🎫 Token & Queue"
            )


            if student[10]:

                st.info(
                    f"🎫 Token: {student[10]}"
                )

                st.write(
                    f"📍 Queue Position: "
                    f"{student[11]}"
                )

                st.write(
                    f"🏢 Counter: "
                    f"{student[12]}"
                )

                st.write(
                    f"👩‍🏫 Mentor: "
                    f"{student[13]}"
                )

            else:

                if today == "Sunday":

                    st.warning(
                        "🏫 College is closed today."
                    )

                else:

                    if st.button(
                        "🎫 Generate Token"
                    ):

                        queue_position = (
                            get_next_queue_position()
                        )


                        token_number = (
                            f"A{student[0]:03d}"
                        )


                        assigned_mentor = (
                            current_mentor
                        )


                        assigned_counter = (
                            counter_map[
                                assigned_mentor
                            ]
                        )


                        update_token(

                            student[0],

                            token_number,

                            queue_position,

                            assigned_counter,

                            assigned_mentor
                        )


                        st.success(
                            f"🎫 Token Generated: "
                            f"{token_number}"
                        )

                        st.rerun()


    

        latest_students = get_students()


        updated_student = None


        for record in latest_students:

            if record[0] == student[0]:

                updated_student = record

                break


        if updated_student and updated_student[10]:

            st.divider()

            st.subheader(
                "👥 Queue Management"
            )


            queue_status = st.selectbox(

                "Queue Status",

                [
                    "Waiting",
                    "In Progress",
                    "Completed",
                    "Cancelled"
                ],

                index=[
                    "Waiting",
                    "In Progress",
                    "Completed",
                    "Cancelled"
                ].index(
                    updated_student[14]
                )
                if updated_student[14]
                in [
                    "Waiting",
                    "In Progress",
                    "Completed",
                    "Cancelled"
                ]
                else 0
            )


            if st.button(
                "🔄 Update Queue Status"
            ):

                update_queue_status(
                    updated_student[0],
                    queue_status
                )

                st.success(
                    "✅ Queue status updated."
                )

                st.rerun()



            st.divider()

            st.subheader(
                "💰 Fees & Payment"
            )


            fees_status = st.selectbox(

                "Fees Status",

                [
                    "Pending",
                    "Paid"
                ]
            )


            payment_mode = st.selectbox(

                "Payment Mode",

                [
                    "UPI",
                    "Card",
                    "Cash",
                    "Online Transfer"
                ]
            )


            if st.button(
                "💳 Update Payment"
            ):

                update_fees(

                    updated_student[0],

                    fees_status,

                    payment_mode
                )

                st.success(
                    "✅ Payment status updated."
                )

                st.rerun()



            st.divider()

            st.subheader(
                "🎓 Admission Completion"
            )


            if updated_student[15] == "Paid":

                st.success(
                    "💰 Fees Paid"
                )


                if updated_student[17] == "Admission Completed":

                    st.success(
                        "🎉 Admission already completed!"
                    )

                else:

                    if st.button(
                        "🎓 Complete Admission"
                    ):

                        complete_admission(
                            updated_student[0]
                        )

                        st.success(
                            "🎉 Admission completed successfully!"
                        )

                        st.rerun()

            else:

                st.warning(
                    "⚠️ Please complete fee payment before admission completion."
                )

elif st.session_state.role == "Admin":

    st.header(
        "🧑‍💼 Admin Dashboard"
    )


    students = get_students()



    total_students = len(students)


    verified_students = sum(
        1
        for student in students
        if student[9]
    )


    waiting_students = sum(
        1
        for student in students
        if student[14] == "Waiting"
    )


    completed_students = sum(
        1
        for student in students
        if student[17] == "Admission Completed"
    )


    paid_students = sum(
        1
        for student in students
        if student[15] == "Paid"
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "👥 Total Students",
        total_students
    )


    col2.metric(
        "✅ Verified",
        verified_students
    )


    col3.metric(
        "👥 Waiting",
        waiting_students
    )


    col4.metric(
        "💰 Fees Paid",
        paid_students
    )


    col5.metric(
        "🎓 Completed",
        completed_students
    )



    st.divider()

    st.subheader(
        "🏢 Counter Management"
    )


    counter_data = {

        1: "Subashini",

        2: "Megala",

        3: "Anusha",

        4: "Vijitha"
    }


    for counter, mentor in counter_data.items():

        st.write(
            f"🏢 Counter {counter} → "
            f"👩‍🏫 {mentor}"
        )



    st.subheader(
        "📅 Weekly Mentor Schedule"
    )


    for day, mentor in weekly_schedule.items():

        st.write(
            f"📅 {day} → 👩‍🏫 {mentor}"
        )


    st.write(
        "📅 Sunday → 🏫 College Holiday"
    )


    st.divider()

    st.subheader(
        "📋 Admission Records"
    )


    if students:

        for student in students:

            with st.expander(
                f"👤 {student[1]} — "
                f"Application ID {student[0]}"
            ):

                st.write(
                    f"🎓 Course: {student[4]}"
                )

                st.write(
                    f"🎫 Token: "
                    f"{student[10] or 'Not Generated'}"
                )

                st.write(
                    f"🏢 Counter: "
                    f"{student[12] or 'Not Assigned'}"
                )

                st.write(
                    f"👩‍🏫 Mentor: "
                    f"{student[13] or 'Not Assigned'}"
                )

                st.write(
                    f"👥 Queue: {student[14]}"
                )

                st.write(
                    f"💰 Fees: {student[15]}"
                )

                st.write(
                    f"💳 Payment: "
                    f"{student[16] or 'Not Paid'}"
                )

                st.write(
                    f"🎓 Admission: {student[17]}"
                )

    else:

        st.info(
            "No admission records available."
        )