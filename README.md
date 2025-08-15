Conflict-Free Scheduling

A Python-based web application for generating conflict-free college and exam timetables.
The system ensures that no student or resource is double-booked, making scheduling efficient and error-free.

Features

College Timetable Generator – Automatically schedules classes without conflicts.

Exam Timetable Generator – Prevents overlapping exams for the same student.

User-Friendly Interface – Built with Flask for easy interaction.

Customizable Inputs – Easily adapt for different courses, subjects, and constraints.

Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS, Jinja2 Templates

Others: Pandas (data handling), Algorithms for conflict resolution


Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/adi-bansul/Conflict-Free-Scheduling.git
cd Conflict-Free-Scheduling

2️⃣ Create & Activate Virtual Environment

python -m venv venv
venv\Scripts\activate      # For Windows
source venv/bin/activate   # For Mac/Linux

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run the Application

python app.py

The app will start running at: http://127.0.0.1:5000/

## 📂 Project Structure


Conflict-Free-Scheduling/

│── app.py                 # Main Flask application  
│── College_Tt.py          # College timetable generator  
│── Exam_Tt.py             # Exam timetable generator  
│── templates/             # HTML templates  
│── static/css/style.css   # Styling  
│── requirements.txt       # Python dependencies  
└── .gitignore             # Files to be ignored by Git  




Author
Aditya Bansul
