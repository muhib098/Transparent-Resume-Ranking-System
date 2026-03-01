# Transparent-Resume-Ranking-System
A web-based application that automatically ranks uploaded resumes using a structured, explainable scoring model. The system evaluates candidates based on skill matching (70%) and experience (30%), highlights skill gaps, and provides a transparent score breakdown — eliminating black-box AI decisions.

## 🚀 Live Demo

🔗 Streamlit App: http://localhost:8501/#transparent-resume-ranking-system


---

## 📌 Project Overview

This application allows users to upload multiple resumes (PDF format) and automatically ranks candidates based on:

- **Skill Match (70%)**
- **Experience Score (30%)**
- Transparent score breakdown
- Skill gap detection
- Deterministic ranking logic (No black-box AI)

The system ensures fairness, transparency, and structured evaluation.

---

## 🎯 Target Users

- HR Departments  
- Startups  
- University Placement Cells  
- Hackathon Evaluation Systems  
- Recruitment Teams  

---


## ⚙️ How It Works

### 1️⃣ Upload Resumes
Upload one or multiple PDF resumes.

### 2️⃣ Skill Detection
System extracts required skills using:
- Regex pattern matching
- Text extraction from PDFs

### 3️⃣ Experience Extraction
Years of experience are detected from resume text.

### 4️⃣ Score Calculation
Final Score = (0.7 × Skill Match %) + (0.3 × Experience Score)

Candidates are sorted by:
1. Final Score  
2. Skill Score  
3. Experience  

### 5️⃣ Output
- Ranked candidate table
- Skill gap highlighting (in red)
- Skill match bar chart
- CSV download option

---

## 🧠 Technical Implementation

- Python
- Streamlit (UI)
- pdfplumber (PDF text extraction)
- Pandas (Data processing)
- Regex (Skill detection)
- Sorting algorithms for ranking
- Deterministic tie-breaking logic

---

---

## 💻 Installation (Run Locally)

### 1️⃣ Clone the repository
git clone [link]
### 2️⃣ Install dependencies

### 3️⃣ Run the app
streamlit run app.py
