# **Task Manager Web**

Task Manager Web is a web application that allows users to manage tasks by creating, editing, and organizing them into categories and statuses. The application also includes user authentication and role-based access control.

---

## **Features**

### 1. User Authentication and Authorization
- **Registration** and **Login** for users.
- Role-based access:
  - **Admin**: Can manage tasks for all users.
  - **User**: Can manage only their own tasks.

### 2. Task Management (CRUD)
- **Create**: Add tasks with a title, description, deadline, and priority.
- **Edit**: Update task details.
- **Delete**: Remove tasks.
- **View**: Filter tasks by status, category, or priority.

### 3. Categories and Statuses
- Organize tasks into categories like *Work* or *Personal*.
- Tasks have statuses: *New*, *In Progress*, and *Completed*.

### 4. API (Django REST Framework)
- RESTful API for interacting with tasks programmatically.

---

## **Technology Stack**

- **Backend**: Python 3.10+, Django 4.x
- **API**: Django REST Framework
- **Database**: SQLite (for development)
- **Testing**: Ngrok for temporary HTTPS links during development

---

## **Setup Instructions**

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/task-manager-web.git
cd task-manager-web
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`.

---

## **API Documentation**

API endpoints are available at:
```
http://127.0.0.1:8000/api/
```

---

## **Known Issues and Limitations**

- Password reset functionality is not implemented yet.
- Role management is only accessible via the admin panel.
- Deployment on Heroku is pending due to account verification.

---

## **Future Enhancements**
- Implement password reset functionality.
- Add a user-friendly interface for role management.
- Complete deployment setup for production.

---

If you find any issues or want to contribute, feel free to open an issue or submit a pull request.
