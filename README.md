# 🎯 Quizzo — NPTEL Quiz Practice Platform

**Quizzo** is a web-based quiz application designed to help students practice multiple-choice questions (MCQs) for NPTEL courses. It provides a simple, interactive interface for testing knowledge, reviewing answers, and preparing for quizzes.

🌐 **Live Application:** [Play Quizzo](https://quizzo-3skuttgaybrvazqgp72bly.streamlit.app/)

## ✨ Features

- 📚 **Course Selection:** Choose the NPTEL course you want to practice.
- 📅 **Week-wise Quizzes:** Practice questions organized by course weeks.
- 🎲 **Randomized Questions:** Get a varied practice experience.
- 📝 **Interactive MCQs:** Select answers through an easy-to-use interface.
- 📊 **Instant Scoring:** Evaluate your performance after completing a quiz.
- ✅ **Answer Review:** Check correct answers and read explanations.
- 🚀 **Cloud Deployment:** Access the application online without installing Python locally.

## 🛠️ Tech Stack

- **Python** — Application logic
- **Streamlit** — Web application framework
- **JSON** — Question bank storage
- **GitHub** — Source code management
- **Streamlit Community Cloud** — Application hosting

## 📂 Project Structure

```text
Quizzo/
├── app.py             # Main Streamlit application
├── questions.json     # Question bank
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/nandoz28/Quizzo.git
cd Quizzo
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows:**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch Quizzo

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## ➕ Adding Questions

Quizzo stores its questions in `questions.json`. Each question follows this structure:

```json
{
  "id": 1201,
  "course": "Architectural Approaches to Decarbonization of Buildings",
  "week": 12,
  "question": "Enter your question here",
  "options": {
    "A": "Option A",
    "B": "Option B",
    "C": "Option C",
    "D": "Option D"
  },
  "answer": "B",
  "explanation": "Explanation of the correct answer."
}
```

**Guidelines:**
- Use a unique ID for each question.
- Ensure the course name matches the existing questions exactly.
- Set `week` to the appropriate week number.
- Set `answer` to one of `A`, `B`, `C`, or `D`.
- Separate question objects with commas and keep the entire file inside a single JSON array.

After updating the question bank, commit and push the changes to GitHub to update the deployed application.

## 🌍 Deployment

Quizzo is hosted on **Streamlit Community Cloud** and connected to this GitHub repository. Updates committed to the repository can trigger automatic redeployment.

## 🎯 Objective

The primary objective of Quizzo is to make NPTEL quiz preparation more accessible, organized, and convenient through a lightweight web application.

## 🔮 Future Enhancements

- User accounts and personalized progress tracking
- Leaderboards and score history
- Performance analytics and weak-topic identification
- Timed quizzes and mock examinations
- Expanded question banks for additional courses
- Responsive UI improvements

## 👨‍💻 Author

**GitHub:** [@nandoz28](https://github.com/nandoz28)

---

*Quizzo — Practice smarter. Learn better. Score higher.*

