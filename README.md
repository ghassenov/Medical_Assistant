# 🏥 Medical Assistant Chatbot

A conversational AI-powered **Medical Assistant** designed to help users interact with medical documents and ask health-related questions.
The project is divided into two main parts:

* **Server** (FastAPI + NLP backend)
* **Client** (Streamlit frontend UI)

---

## 🚀 Features

* Upload and process medical documents (PDFs).
* Ask medical-related questions based on uploaded documents.
* Vector database for efficient retrieval.
* Exception handling and structured logging.
* Interactive chat UI built with Streamlit.

---

## 📂 Project Structure

```
MEDICAL_ASSISTANT/
│── client/                     # Frontend (Streamlit)
│   ├── components/             # UI components
│   │   ├── chatUI.py
│   │   ├── history_download.py
│   │   └── upload.py
│   ├── utils/                  # Client utilities
│   │   ├── api.py
│   |── app.py
│   |── config.py
│   └── requirements.txt
│
│── server/                     # Backend (FastAPI)
│   ├── middlewares/            # Exception handlers
│   │   └── exception_handlers.py
│   ├── modules/                # Core functionalities
│   │   ├── llm.py
│   │   ├── load_vectorstore.py
│   │   ├── pdf_handlers.py
│   │   └── query_handlers.py
│   ├── routes/                 # API routes
│   │   ├── ask_question.py
│   │   └── upload_pdfs.py
│   ├── uploaded_docs/          # Uploaded files storage
│   ├── logger.py               # Logging setup
│   ├── main.py                 # FastAPI entrypoint
│   ├── requirements.txt
│   └── test.py
|   └── .env                    # Environment variables
│                        
├── .gitignore
├── .python-version
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git https://github.com/ghassenov/Medical_Assistant.git
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
```

### 3️⃣ Install dependencies

For **server**:

```bash
cd server
pip install -r requirements.txt
```

For **client**:

```bash
cd ../client
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start the FastAPI backend

```bash
cd server
uvicorn main:app --reload
```

* Runs on: `http://127.0.0.1:8000`

### Start the Streamlit frontend

Open a new terminal:

```bash
cd client
streamlit run app.py
```

* Runs on: `http://localhost:8501`

---

## 🔧 Configuration

* Environment variables are stored in `.env`.
* Inside the .env file, you must configure the following:

```bash
# API Keys
JINA_API_KEY=your_jina_api_key
PINECONE_API_KEY=your_pinecone_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Pinecone Index
PINECONE_INDEX_NAME=your_index_name
```
Without these keys, the system will not be able to embed documents, query the vectorstore, or call the LLMs.

---

## 📌 Future Improvements

* Add authentication for users.
* Enhance UI for better user experience.
* Expand support for more medical datasets.
* Add multilingual medical support.

---
