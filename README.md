# ShapeViewer_WebApplication
Shape Viewer is a full-stack web app for visualizing 3D prism shapes using Three.js. If a shape isn't found locally, the backend fetches compute scripts from GitHub, processes them, and returns the model data for rendering. Easily extensible with new shape plugins.

---

## 🌐 Overview

**Shape Viewer (Web Version)** is a **full-stack 3D visualization platform** that lets users explore and interact with prism shapes directly in their browser.  
It uses **Three.js** for rendering 3D models, a **React.js** frontend for an interactive UI, and a **Django REST Framework** backend to dynamically fetch, compute, and deliver shape data.

> 🚀 **Dynamic Plugin Architecture:** No need to hardcode shapes — new shape logic is fetched on demand from GitHub.

---

## ✨ Key Features

✅ **Dynamic Plugin System** — Shape computation logic is fetched and integrated at runtime from GitHub  
✅ **3D Interactive Visualization** — Powered by **Three.js**  
✅ **REST API Architecture** — Clean separation between backend & frontend  
✅ **Scalable & Modular** — Add new shape types easily  
✅ **Automated CI/CD Pipeline** — Built with **GitHub Actions**  

---

## 🛠 Tech Stack

**Frontend:**  
- ⚛️ [React.js](https://reactjs.org/) — Dynamic UI  
- 🎨 [Three.js](https://threejs.org/) — 3D rendering in browser  
- 📦 npm — Dependency management

**Backend:**  
- 🐍 [Python 3.10](https://www.python.org/) — Core logic  
- 🌱 [Django](https://www.djangoproject.com/) + [Django REST Framework](https://www.django-rest-framework.org/) — API layer  
- 🗄 Local database — Shape storage

**DevOps:**  
- 🤖 [GitHub Actions](https://github.com/features/actions) — CI/CD automation  
- 🛠 Node.js v22.18 — Build tools

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/shape-viewer-web.git
cd shape-viewer-web
```

### 2️⃣ Backend Setup (Django)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
python manage.py migrate

# Start Django backend
python manage.py runserver
```

### 3️⃣ Frontend Setup (React)
```bash
cd frontend
npm install
npm start
```

---

## 🔄 How It Works

1. **User selects a prism shape** in the React frontend.  
2. **Frontend sends API request** → Django backend.  
3. **Backend checks local DB** for shape logic.  
4. **If missing**, backend fetches script from GitHub → runs computation.  
5. **Model data is sent** back to frontend.  
6. **Three.js renders** it interactively in the browser.

---

## 🚀 Deployment

The app can be deployed on:  
- ☁ **AWS EC2 / Elastic Beanstalk**  
- ▲ **Vercel** (Frontend)  
- 🌀 **Heroku / Render** (Backend)  

**CI/CD via GitHub Actions** handles:  
- Installing frontend & backend dependencies  
- Running unit tests  
- Building React app  
- Running migrations & collecting static files for Django  

---

## 📂 Project Structure
```
shape-viewer-web/
│
├── backend/                 # Django backend (API & shape logic)
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/                # React frontend (Three.js rendering)
│   ├── package.json
│   └── src/
│
├── .github/workflows/       # GitHub Actions CI/CD pipelines
└── README.md
```

---

## 🧑‍💻 Contributing

Pull requests are welcome! Please follow these steps:
1. Fork the repo
2. Create a new branch (`feature-new-shape`)
3. Commit your changes
4. Open a pull request



---

## 📸 Screenshots (Optional)
*(Add sample GIFs or screenshots here to showcase 3D models in action)*

---
```

---

I’ve kept the **emoji-based section headers**, **badges for instant visual appeal**, and **clear step-by-step install instructions** so someone can set it up quickly.  
If you want, I can also **add live demo GIFs** showing shape rendering for maximum impact.

