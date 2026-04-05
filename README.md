 🚀 AI Resume Screener

An intelligent **AI-powered Resume Screening Web App** that matches resumes with job descriptions using **NLP, TF-IDF, BERT, and Skill Extraction**.

Built with **Streamlit**, this project helps recruiters quickly identify the best candidates based on skill relevance and semantic similarity.

---

## 🌟 Features

* 📄 Upload multiple resumes (PDF format)
* 🧠 NLP-based text preprocessing
* 📊 TF-IDF similarity scoring
* 🤖 BERT-based semantic similarity
* 🧩 Skill extraction from resumes & job description
* ✅ Matched & ❌ Missing skills analysis
* 🏆 Automatic ranking of candidates
* 📈 Model comparison (TF-IDF vs BERT vs Final Score)
* 📥 Download results as CSV


---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Libraries:**

  * pandas
  * scikit-learn
  * nltk / spacy (for NLP)
  * sentence-transformers (BERT)
  * PyPDF2 / pdfplumber (for PDF parsing)

---

## 📂 Project Structure

```
Smart_Resume_Screener/
│
├── app.py               # Main Streamlit app
├── utils.py             # Text processing & scoring functions
├── skills.py            # Skill extraction logic
├── data/                # (Optional) saved outputs
├── requirements.txt     # Dependencies
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/sakshi-0101/SMART_RESUME_SCREENER
cd ai-resume-screener
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App


streamlit run app.py

Then open in browser:
http://localhost:8501


## 📊 How It Works

1. **Input Job Description**
2. **Upload Resumes (PDF)**
3. App performs:

   * Text cleaning
   * Skill extraction
   * TF-IDF similarity
   * BERT similarity
4. Combines scores → generates **final ranking**
5. Displays:

   * Match %
   * Skills found
   * Missing skills
6. Download results as CSV

---

## 🧠 Scoring Logic

* **TF-IDF Score** → Keyword-based similarity
* **BERT Score** → Semantic similarity
* **Final Score** → Weighted combination of both

---

## 🚀 Future Improvements

* 📊 Add interactive charts & analytics
* 🧾 Support DOCX resumes
* 🌐 Deploy on Streamlit Cloud / AWS
* 🧠 Improve skill extraction using ML models
* 📌 Add recruiter dashboard

---

## 🎯 Use Cases

* HR Resume Screening
* Internship Shortlisting
* College Placement Filtering
* Automated Candidate Ranking

---




## 👩‍💻 Author

Sakshi Grawal





