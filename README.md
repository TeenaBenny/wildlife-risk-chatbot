# 🦉 Light Pollution Wildlife Risk Chatbot

## 📌 Project Overview

The **Light Pollution Wildlife Risk Chatbot** is a Python-based chatbot designed to answer questions about light pollution, its effects on wildlife, and ways to reduce its environmental impact.

The chatbot uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from a wildlife PDF document and uses Google's Gemini AI to generate answers based on the retrieved content.

This project demonstrates how Artificial Intelligence, Natural Language Processing, vector databases, and Large Language Models can be combined to build a document-based question-answering system.

## 🎯 Objectives

* Understand the effects of artificial light at night on wildlife.
* Develop an interactive chatbot for wildlife-related questions.
* Retrieve relevant information from a PDF document.
* Use vector embeddings for semantic search.
* Use ChromaDB as a vector database.
* Generate context-based answers using the Gemini API.

## ✨ Features

* 💬 Interactive chatbot interface using Streamlit.
* 📄 Answers questions using information retrieved from a wildlife PDF.
* 🔎 Semantic search using vector embeddings.
* 🗄️ ChromaDB vector database for storing and searching document embeddings.
* 🤖 Google Gemini API for generating answers.
* 📚 Displays the PDF page numbers used to retrieve information.
* 🧹 Clear chat functionality.
* 💡 Suggested questions for users.

## 🛠️ Technologies Used

| Technology                        | Purpose                                           |
| --------------------------------- | ------------------------------------------------- |
| Python                            | Main programming language                         |
| Streamlit                         | Chatbot user interface                            |
| LangChain                         | Connects the document retrieval and AI components |
| ChromaDB                          | Vector database                                   |
| HuggingFace Sentence Transformers | Converts text into vector embeddings              |
| Google Gemini API                 | Generates chatbot answers                         |
| PyPDF                             | Reads PDF documents                               |
| python-dotenv                     | Loads the API key from an environment file        |

## 🏗️ System Architecture

```text
          wildlife.pdf
               |
               v
         PyPDFLoader
               |
               v
         Text Splitting
               |
               v
      HuggingFace Embeddings
               |
               v
           ChromaDB
        (Vector Database)
               |
               v
         User Question
               |
               v
       Semantic Retrieval
               |
               v
       Relevant PDF Chunks
               |
               v
          Gemini API
               |
               v
        Chatbot Answer
```

## 🔄 How It Works

1. **PDF Loading:** The system reads the wildlife information PDF using PyPDFLoader.
2. **Text Splitting:** The document is divided into smaller text chunks.
3. **Embedding Generation:** HuggingFace Sentence Transformers convert the text chunks into numerical vectors.
4. **Vector Storage:** ChromaDB stores the vectors and associated document text.
5. **Question Retrieval:** When a user asks a question, the retriever searches for relevant document chunks.
6. **Answer Generation:** The retrieved context and user question are sent to Gemini.
7. **Response Display:** The chatbot displays the generated answer in the Streamlit interface.

## 📂 Project Structure

```text
wildlife_chatbot/
│
├── app.py              # Streamlit chatbot application
├── ingest.py           # PDF processing and vector database creation
├── wildlife.pdf        # Wildlife information document
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration
├── .gitignore          # Files excluded from Git
├── README.md           # Project documentation
└── chroma_db/          # Generated vector database (not committed)
```

## ⚙️ Requirements

* Python 3.10 or a compatible Python version.
* pip package manager.
* A Google Gemini API key.
* Internet access for API requests and initial model downloads.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/TeenaBenny/wildlife-risk-chatbot.git
cd wildlife-risk-chatbot
```

### 2. Create a virtual environment

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own Gemini API key.

**Security:** Never upload `.env` or your actual API key to GitHub.

### 5. Prepare the vector database

Make sure `wildlife.pdf` is present in the project root and that the PDF path in `ingest.py` matches its location.

Run:

```cmd
python ingest.py
```

This processes the PDF and creates the ChromaDB vector database in the `chroma_db` folder.

You only need to run ingestion again when you want to create or update the database from the PDF.

### 6. Run the chatbot

```cmd
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 💬 Example Questions

* What is light pollution?
* How does light pollution affect birds?
* How does artificial light affect insects?
* How can light pollution be reduced?
* Why is darkness important for wildlife?
* What are the effects of artificial light at night on animals?

Answers depend on the information available in the PDF document.

## 🗄️ Vector Database

This project uses **ChromaDB** as its vector database.

The document text is converted into vector embeddings using the `sentence-transformers/all-MiniLM-L6-v2` model. ChromaDB stores these embeddings and supports similarity-based retrieval of relevant text.

This helps the chatbot find information related to a question even when the wording of the question differs from the wording in the PDF.

## 🧠 Retrieval-Augmented Generation (RAG)

RAG combines document retrieval with AI-based answer generation.

In this project:

* **Retrieval:** ChromaDB retrieves relevant information from the wildlife PDF.
* **Augmentation:** The retrieved text is added to the user's question as context.
* **Generation:** Gemini generates an answer using the supplied context.

The application prompt instructs the chatbot to answer from the retrieved context and state when the requested information cannot be found.

## 🔐 Environment Variables and Security

* Store your Gemini API key in `.env`.
* Add `.env`, `venv/`, and `chroma_db/` to `.gitignore`.
* Do not commit API keys, passwords, or other secrets.
* Users must configure their own API key to run the chatbot.

## ⚠️ Limitations

* Answers depend on the quality and coverage of the PDF document.
* The chatbot requires access to the Gemini API for AI-generated responses.
* API quotas and rate limits may restrict usage.
* Initial setup may require downloading Python packages and the embedding model.
* The chatbot is an educational project and should not be treated as a substitute for expert wildlife or environmental assessments.

## 🔮 Future Enhancements

* Support multiple PDF documents.
* Add wildlife risk prediction using a machine learning model.
* Integrate the chatbot with a Power BI wildlife risk dashboard.
* Add multilingual question answering.
* Improve document citations and source references.
* Add a feedback system to evaluate answer quality.

## 🌱 Project Applications

This project can be used as an educational tool to explore light pollution, wildlife conservation, environmental awareness, and document-based AI question answering.

## 👩‍💻 Author

**Teena Benny**

College Project: Light Pollution and Wildlife Risk Prediction

## 📄 License

This project is intended for educational and academic purposes. Add an appropriate open-source license if you decide to distribute the project publicly.
