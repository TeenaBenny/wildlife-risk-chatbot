import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Wildlife Risk Chatbot",
    page_icon="🦉",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("🦉 Light Pollution Wildlife Risk Chatbot")

st.write(
    "Ask questions about light pollution, wildlife and ecological risks."
)


# ============================================================
# LOAD EMBEDDINGS
# Cached so it loads only once
# ============================================================

@st.cache_resource
def load_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embeddings = load_embeddings()


# ============================================================
# LOAD CHROMA VECTOR DATABASE
# Cached so it loads only once
# ============================================================

@st.cache_resource
def load_vectorstore():

    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )


vectorstore = load_vectorstore()


# ============================================================
# CREATE RETRIEVER
# We use 3 relevant chunks instead of 4
# ============================================================

@st.cache_resource
def load_retriever():

    return vectorstore.as_retriever(
        search_kwargs={
            "k": 3
        }
    )


retriever = load_retriever()


# ============================================================
# LOAD GEMINI
# Cached so the model is not recreated every time
# ============================================================

@st.cache_resource
def load_gemini():

    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0
    )


llm = load_gemini()


# ============================================================
# PROMPT
# Kept short to reduce unnecessary tokens
# ============================================================

prompt = ChatPromptTemplate.from_template(
"""
You are a chatbot for a college project about light pollution and wildlife.

Answer using ONLY the context below.

Context:
{context}

Question:
{question}

Instructions:
- Give a clear and concise answer.
- Use only information from the context.
- Do not invent information.
- If the answer is not in the context, say:
"I could not find this information in the provided document."
"""
)


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CLEAR CHAT BUTTON
# ============================================================

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

st.markdown("### 💡 Suggested Questions")

col1, col2 = st.columns(2)

with col1:

    if st.button("What is light pollution?"):

        question = "What is light pollution?"

    elif st.button("How does it affect birds?"):

        question = "How does light pollution affect birds?"

    else:

        question = None


with col2:

    if st.button("How does it affect insects?"):

        question = "How does light pollution affect insects?"

    elif st.button("How can it be reduced?"):

        question = "How can light pollution be reduced?"


# ============================================================
# CHAT INPUT
# ============================================================

chat_question = st.chat_input(
    "Ask about light pollution and wildlife..."
)


# If user types a question, use that instead

if chat_question:

    question = chat_question


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # Display user question
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # Save user question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    try:

        # ====================================================
        # RETRIEVE RELEVANT DOCUMENTS
        # ====================================================

        docs = retriever.invoke(question)


        # ====================================================
        # CHECK DOCUMENTS
        # ====================================================

        if not docs:

            answer = (
                "I could not find relevant information "
                "in the provided document."
            )

        else:

            # =================================================
            # CREATE CONTEXT
            # =================================================

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )


            # =================================================
            # CREATE FINAL PROMPT
            # =================================================

            final_prompt = prompt.format(
                context=context,
                question=question
            )


            # =================================================
            # CALL GEMINI
            # =================================================

            with st.chat_message("assistant"):

                with st.spinner(
                    "🦉 Analyzing wildlife information..."
                ):

                    response = llm.invoke(
                        final_prompt
                    )


                # =================================================
                # CLEAN GEMINI RESPONSE
                # =================================================

                if isinstance(
                    response.content,
                    str
                ):

                    answer = response.content


                elif isinstance(
                    response.content,
                    list
                ):

                    text_parts = []


                    for item in response.content:

                        if isinstance(
                            item,
                            dict
                        ):

                            text = item.get(
                                "text",
                                ""
                            )

                            if text:

                                text_parts.append(
                                    text
                                )


                        elif isinstance(
                            item,
                            str
                        ):

                            text_parts.append(
                                item
                            )


                    answer = "\n".join(
                        text_parts
                    ).strip()


                else:

                    answer = str(
                        response.content
                    )


                # =================================================
                # EMPTY RESPONSE CHECK
                # =================================================

                if not answer:

                    answer = (
                        "I could not generate an answer. "
                        "Please try again."
                    )


                # =================================================
                # DISPLAY ANSWER
                # =================================================

                st.markdown(answer)


                # =================================================
                # SHOW SOURCE PAGES
                # =================================================

                pages = []

                for doc in docs:

                    page = doc.metadata.get(
                        "page"
                    )

                    if page is not None:

                        pages.append(
                            int(page) + 1
                        )


                pages = sorted(
                    set(pages)
                )


                if pages:

                    st.caption(
                        "📚 Information retrieved from "
                        "PDF page(s): "
                        + ", ".join(
                            str(page)
                            for page in pages
                        )
                    )


        # ====================================================
        # SAVE ASSISTANT RESPONSE
        # ====================================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        error_message = (
            "⚠️ Sorry, I couldn't process your question."
        )


        with st.chat_message("assistant"):

            st.error(error_message)


            with st.expander(
                "Technical details"
            ):

                st.code(
                    str(e)
                )