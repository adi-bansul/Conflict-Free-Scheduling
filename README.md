# 📅 Conflict-Free Scheduling

A Flask-based web application for generating conflict-free timetables for colleges and exams.  
It ensures that no student or resource has overlapping schedules, making timetable creation efficient and error-free.

---

## 🚀 Features
- Generate **college timetables** without clashes.
- Create **exam timetables** ensuring no student has overlapping exams.
- Simple **web interface** for data input and viewing results.
- **Dynamic scheduling** logic to handle multiple constraints.
- Clean, responsive UI with HTML + CSS.

---

## 🛠️ Tech Stack
- **Python** — Core programming language  
- **Flask** — Backend framework  
- **HTML, CSS** — Frontend UI  
- **Pandas** — Data handling  
- **Jinja2** — Template rendering

---

## 📂 Project Structure


Conflict-Free-Scheduling/

│── app.py                 # Main Flask application  
│── College_Tt.py          # College timetable generator  
│── Exam_Tt.py             # Exam timetable generator  
│── templates/             # HTML templates  
│── static/css/style.css   # Styling  
│── requirements.txt       # Python dependencies  
└── .gitignore             # Files to be ignored by Git  

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/Conflict-Free-Scheduling.git
cd Conflict-Free-Scheduling

2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
python app.py
```

Open your browser and go to:

http://127.0.0.1:5000

📜 License

This project is licensed under the MIT License — feel free to use and modify it.

Author
Aditya Bansul
