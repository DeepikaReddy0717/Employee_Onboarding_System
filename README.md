# 🧠 Employee Training and Onboarding System

A Django-based web application created during the **23CS05EF - Python Full Stack Development with Django**.

This system is designed to streamline employee training, assessments, and progress tracking for HR managers and corporate teams.

> 🚧 This project is currently in the development phase. Basic modules for core user roles have been implemented.

---

## 🚀 Tech Stack

- 💻 **Backend**: Python (Django Framework)
- 🎨 **Frontend**: HTML, CSS (basic templating with Django)
- 🧰 **IDE Used**: PyCharm
- 🛠️ **Database**: SQLite (default Django DB)

---

## 👥 User Roles

### 🔐 1. Admin
- 👑 Full control of the platform
- ➕ Add trainers and courses
- 🧠 Assign courses to specific users
- 🚫 **Terminate access** to any user or trainer
- 📜 **View system logs** to monitor activity

### 🎓 2. Trainer
- 📝 Create and manage training content
- 📊 Track progress of assigned employees
- 🧪 Schedule and manage assessments

### 👤 3. User (Employee)
- 📚 Access and complete assigned training modules
- 📈 Track personal training progress and results
- 🤖 Get help from the chatbot (upcoming feature)

---

## 📦 Modules Implemented

| Module        | Status     | Description |
|---------------|------------|-------------|
| Authentication | ✅ Done | Login/Logout system for all roles |
| Admin Panel   | ✅ Done | Add/terminate users, assign courses, view logs |
| Trainer Panel | ✅ Done | Upload training content, monitor progress |
| User Panel    | ✅ Done | View assigned courses, track status |

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/f69ab1d1-de27-4b95-a37c-968dfed46567)

### Signin Page
![image](https://github.com/user-attachments/assets/186ec1b8-d067-4584-b38c-00451af68a90)

### 🔐 Login Page
![image](https://github.com/user-attachments/assets/2160bc1a-cbe6-4bd3-8add-ba95137525b1)

### 🛡️ Admin Controls
![image](https://github.com/user-attachments/assets/8ce0a49a-ba21-422b-87aa-2b6fcc98dbba)

### 🧑‍🏫 Trainer Dashboard
![image](https://github.com/user-attachments/assets/cab3210d-55e0-40d4-9e02-647260af8b6d)
![image](https://github.com/user-attachments/assets/7abd3d26-2b77-4931-9aaa-3af60ed177d2)

### User Dashboard
![image](https://github.com/user-attachments/assets/0aaed481-4eb6-420b-96ba-50ca40819faa)
![image](https://github.com/user-attachments/assets/e02b1bb9-d55e-4328-99d3-2b6bf25c8542)


---

## 🙏 Acknowledgements

This project was developed collaboratively as part of the **23CS05EF - Python Full Stack Development with Django **.

We would like to thank:

- 💻 Our amazing **team members** for their dedication, teamwork, and contributions across all modules  
- 📚 Various **online communities, tutorials, and documentation** like w3 schools,tutorial point that provided guidance throughout the development  
- 👨‍🏫 The course instructors and mentor Dr.Deepak sir  for their constant support and encouragement  
- 🌐 Open-source tools and frameworks that made this project possible 

## 📌 How to Run the Project Locally

```bash
# Clone the repository
git clone https://github.com/DeepikaReddy0717/Hackthon.git
cd Hackthon

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver

# Open in browser
# Visit: http://127.0.0.1:8000/

