# Flask Attendance System with Face Recognition Using CNN Model
🎉🎉🎉 This project is a Flask-based application for managing an attendance system using face recognition technology. It incorporates real-time communication with Socket.IO and supports machine learning for facial recognition. 🎉🎉🎉


## Features
- 🎯 **Face Recognition**: Automated attendance marking based on face detection and recognition.
- 🎯 **Real-time Communication**: Uses Socket.IO for real-time updates.
- 🎯 **Database Integration**: Supports MySQL for storing user and attendance data.
- 🎯 **User Roles**: Separate pages for lecturers and students to manage and view attendance. 
- 🎯 **Scheduling**: Background task scheduling using APScheduler.

## Prerequisites
📋 Make sure you have the following installed: 📋
1. Python 3.8 or higher
2. MySQL database server
3. Virtual environment tool (optional but recommended)

## Installation
1. **Clone the Repository:**
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```
2. **Create a Virtual Environment (Optional):**
   ```
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```
3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Set Up the Environment Variables:**
   Create a `.env` file in the root directory with the following content:
   ```
   DB_USERNAME=root
   DB_PASSWORD=your_password
   DB_NAME=attendance_system
   DB_HOST=localhost
   ```
5. **Set Up the Database:**
   - Create a MySQL database named `attendance_system`.
   - Run any provided SQL scripts to initialize the tables.
6. **Run the Application:**
   ```
   python app.py
   ```
   🚀 The application will be accessible at http://127.0.0.1:5000/. 🚀


## Project Structure
🎨
```
project-root/
├── app.py               # Main Flask application file
├── requirements.txt     # List of dependencies
├── templates/           # HTML templates for pages
├── static/              # Static files (CSS, JS, images)
├── facerecognition.py   # Face recognition processing logic
├── .env                 # Environment variables
└── README.md            # Project documentation
```


## Usage
- 🎓 Lecturer: Access the "Create Attendance" page to create attendance sessions.
- 🎓 Student: Use the "Scan Attendance" page to scan your face for attendance.


## Key Libraries
📚 The following libraries are used in this project: 📚
- Flask: For building the web application.
- Socket.IO: For real-time data communication.
- OpenCV: For face detection and processing.
- Keras/TensorFlow: For implementing face recognition models.
- MySQL: For database management.
- APScheduler: For task scheduling.


## Acknowledgments
🙏 Special thanks to the open-source community for providing the tools and libraries that made this project possible. 🙏
