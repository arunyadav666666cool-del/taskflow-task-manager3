Task Management System

A desktop task management application built with **Python & Tkinter**, designed for team workflows where a **Manager** assigns and reviews tasks submitted by **Subordinates**.

---

## Features

### 👔 Manager
- Login with manager credentials
- View **all submitted projects** from subordinates
- **Filter** projects by status: All / Pending / Reviewed / Approved / Rejected
- Add **remarks** to any project
- **Approve**, **Reject**, or **Mark as Reviewed** with confirmation dialogs
- Live **stats dashboard** showing count by status

### 👤 Subordinate
- Login with individual subordinate credentials
- **Upload/submit projects** with title, description, and file attachment
- View **personal project history** with current status
- See **manager remarks** and feedback on each submission

---

## 🛠️ Tech Stack

| Component     | Technology                     |
|---------------|-------------------------------|
| Language      | Python 3.x                    |
| GUI Framework | Tkinter (built-in)            |
| Data Storage  | JSON (`task_data.json`)       |
| File Uploads  | Local directory (`uploaded_projects/`) |

---

## 📁 Project Structure

```
task-management/
│
├── task_app.py              # Main application file
├── task_data.json           # Auto-generated data storage
├── uploaded_projects/       # Auto-created folder for uploaded files
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external libraries required (uses only Python standard library)

### Steps

```bash
# 1. Clone or download the project
git clone https://github.com/yourname/task-management.git
cd task-management

# 2. Run the application
python task_app.py
```

> ✅ Tkinter comes pre-installed with most Python distributions. If missing, install via:
> ```bash
> sudo apt-get install python3-tk   # Linux
> ```

---

## 🔐 Demo Credentials

| Role        | Email                  | Password   |
|-------------|------------------------|------------|
| Manager     | manager@task.com       | mgr123     |
| Subordinate | arjun@task.com         | arjun123   |
| Subordinate | priya@task.com         | priya123   |
| Subordinate | rahul@task.com         | rahul123   |
| Subordinate | neha@task.com          | neha123    |

---

## 🖥️ How to Use

### Manager Flow
1. Open the app → select **Manager** role → sign in
2. Dashboard shows all project submissions with status badges
3. Use **filter bar** to narrow by status
4. On any **Pending** project:
   - Type a remark in the text box
   - Click **Approve**, **Reject**, or **Save Remark**
5. Stats update automatically

### Subordinate Flow
1. Open the app → select **Subordinate** role → sign in
2. **My Projects tab** — see all your submissions and manager feedback
3. **Upload Project tab** — submit a new project:
   - Enter title and description
   - Attach a file (PDF, DOCX, XLSX, PPTX, TXT, etc.)
   - Click **Submit Project**

---

## 📊 Project Status Lifecycle

```
Submitted → PENDING → REVIEWED → APPROVED
                   ↘           ↗
                    REJECTED
```

| Status   | Color  | Meaning                              |
|----------|--------|--------------------------------------|
| Pending  | Yellow | Awaiting manager action              |
| Reviewed | Purple | Manager left a remark, deciding      |
| Approved | Green  | Project accepted                     |
| Rejected | Red    | Project needs rework                 |

---

## 🗂️ Data Storage

All project data is saved in **`task_data.json`** automatically. Each project record contains:

```json
{
  "id": 1,
  "title": "Website Redesign",
  "desc": "Project description...",
  "file": "redesign_v2.pdf",
  "owner": "Arjun Sharma",
  "email": "arjun@task.com",
  "status": "pending",
  "remark": "",
  "date": "2025-06-18"
}
```

Uploaded files are copied to the `uploaded_projects/` folder for local storage.

---

## 🔒 Validations & Error Handling

- Role mismatch check on login (can't log in as wrong role)
- Duplicate project title prevention (per user)
- Required field validation on project submission
- Confirmation dialog before approve/reject actions
- Graceful file copy error handling

---

## 🎨 UI Highlights

- Clean card-based layout with color-coded status badges
- Smooth scrollable project lists
- Responsive window resizing
- Tab navigation for subordinate dashboard
- Role-specific color themes (Blue for Manager, Green for Subordinate)

---

## 🔮 Future Enhancements

- [ ] Add signup functionality for new users
- [ ] Manager-assigned tasks (push tasks to subordinates)
- [ ] Email notifications on status change
- [ ] Deadline / due date tracking
- [ ] Search and sort functionality
- [ ] Export reports to Excel/PDF
- [ ] Password hashing for security
- [ ] Multi-project file attachments

---

## 📄 License

This project is open-source and free to use for educational or personal purposes.

---

## 🙌 Author

Built with Python & Tkinter.  
Feel free to fork, modify, and improve!
