import streamlit as st
from chatbot import FAQChatbot


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Nexora AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD CHATBOT
# ============================================================

@st.cache_resource
def load_chatbot():
    return FAQChatbot(threshold=0.25)


bot = load_chatbot()


# ============================================================
# SESSION STATE
# ============================================================

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "current_response" not in st.session_state:
    st.session_state.current_response = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background-color: #080b12;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #0d111a;
        border-right: 1px solid #1e2633;
    }

    section[data-testid="stSidebar"] * {
        color: #d8dee9;
    }


    /* =========================
       HEADINGS
       ========================= */

    h1 {
        color: #ffffff !important;
        font-weight: 750 !important;
        letter-spacing: -1px;
    }

    h2,
    h3 {
        color: #f3f4f6 !important;
    }

    p {
        color: #9ca3af;
    }


    /* =========================
       HERO
       ========================= */

    .hero-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: 750;
        line-height: 1.15;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 15px;
        max-width: 700px;
        line-height: 1.6;
    }


    /* =========================
       METRICS
       ========================= */

    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #222c3b;
        border-radius: 14px;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f9fafb !important;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        background-color: #111827;
        color: #d1d5db;
        border: 1px solid #293445;
        border-radius: 10px;
        min-height: 42px;
        transition: 0.2s;
        text-align: left;
    }

    .stButton > button:hover {
        background-color: #1a2230;
        color: #ffffff;
        border-color: #7c3aed;
    }


    /* =========================
       CHAT INPUT
       ========================= */

    div[data-testid="stChatInput"] {
        background-color: #111827;
        border: 1px solid #303b4d;
        border-radius: 16px;
    }


    /* =========================
       CHAT
       ========================= */

    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        margin-bottom: 10px;
    }


    /* =========================
       INFO CARD
       ========================= */

    .info-card {
        background-color: #111827;
        border: 1px solid #222c3b;
        border-radius: 14px;
        padding: 18px;
        margin-top: 18px;
    }

    .info-title {
        color: #f9fafb;
        font-weight: 650;
        font-size: 14px;
        margin-bottom: 7px;
    }

    .info-text {
        color: #8f9aaa;
        font-size: 12px;
        line-height: 1.6;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #4b5563;
        font-size: 11px;
        margin-top: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# ✦ Nexora AI")

    st.caption("Intelligent Customer Support")

    st.divider()

    st.markdown("###  System")

    st.success("AI Assistant Online")

    st.divider()

    st.markdown("###  Knowledge Base")

    st.write(
        f"**{len(bot.faqs)}** professional FAQs"
    )

    st.write(
        f"**{len(bot.get_categories())}** support categories"
    )

    st.divider()

    st.markdown("###  AI Pipeline")

    st.caption("Text preprocessing")
    st.caption("↓")
    st.caption("TF-IDF vectorization")
    st.caption("↓")
    st.caption("Cosine similarity")
    st.caption("↓")
    st.caption("Intent matching")
    st.caption("↓")
    st.caption("Smart response")

    st.divider()

    if st.button(
        " Clear conversation",
        use_container_width=True
    ):

        st.session_state.current_question = None
        st.session_state.current_response = None

        st.rerun()


# ============================================================
# HERO
# ============================================================

left, right = st.columns([5, 1])

with left:

    st.markdown(
        '<div class="hero-title">✦ Nexora AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "### Intelligent Customer Support"
    )

    st.markdown(
        """
        <div class="hero-subtitle">
        Get instant answers about products, pricing,
        accounts, security, billing and technical support.
        Ask your question naturally and Nexora AI will
        find the most relevant answer.
        </div>
        """,
        unsafe_allow_html=True
    )

with right:

    st.write("")

    st.success(" ONLINE")


# ============================================================
# METRICS
# ============================================================

faq_count = len(bot.faqs)
category_count = len(bot.get_categories())

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        " Knowledge Base",
        f"{faq_count} FAQs"
    )

with m2:

    st.metric(
        " Categories",
        category_count
    )

with m3:

    st.metric(
        " AI Matching",
        "TF-IDF"
    )


st.write("")


# ============================================================
# MAIN CONTENT
# ============================================================

chat_col, suggestion_col = st.columns(
    [2.2, 1],
    gap="large"
)


# ============================================================
# CHAT SECTION
# ============================================================

with chat_col:

    st.markdown("###  Conversation")

    st.caption(
        "Ask Nexora AI anything about our products and services."
    )

    # ----------------------------------------
    # CURRENT QUESTION
    # ----------------------------------------

    if st.session_state.current_question:

        st.chat_message("user").write(
            st.session_state.current_question
        )


    # ----------------------------------------
    # CURRENT ANSWER
    # ----------------------------------------

    if st.session_state.current_response:

        response = st.session_state.current_response

        with st.chat_message("assistant"):

            st.write(
                response["answer"]
            )

            if response.get("matched_question"):

                st.caption(
                    f"Matched FAQ: "
                    f"{response['matched_question']}"
                )

            if response.get("score", 0) > 0:

                st.caption(
                    f"Confidence: "
                    f"{response['score']:.0%}"
                )

    else:

        st.info(
            " Welcome to Nexora AI. "
            "Ask a question or try one of the suggested questions."
        )


    # ----------------------------------------
    # CHAT INPUT
    # ----------------------------------------

    user_question = st.chat_input(
        "Ask Nexora AI anything..."
    )


    if user_question:

        response = bot.get_response(
            user_question
        )

        # Replace old question and answer
        st.session_state.current_question = (
            user_question
        )

        st.session_state.current_response = (
            response
        )

        st.rerun()


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

with suggestion_col:

    st.markdown("###  Suggested Questions")

    st.caption(
        "Try one of these common questions"
    )


    suggested_questions = [
        "How much does Nexora cost?",
        "Is my data secure?",
        "How do I create an account?",
        "How can I contact support?",
        "What products does Nexora offer?"
    ]


    for index, question in enumerate(
        suggested_questions
    ):

        if st.button(
            question,
            key=f"suggestion_{index}",
            use_container_width=True
        ):

            result = bot.get_response(
                question
            )

            # Replace previous conversation
            st.session_state.current_question = (
                question
            )

            st.session_state.current_response = (
                result
            )

            st.rerun()


    # ----------------------------------------
    # ABOUT
    # ----------------------------------------

    st.markdown(
        """
        <div class="info-card">

        <div class="info-title">
         About Nexora AI
        </div>

        <div class="info-text">
        Nexora AI uses NLP preprocessing,
        TF-IDF vectorization and cosine similarity
        to identify the most relevant FAQ answer.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Nexora AI · Intelligent Customer Support ·
        NLP Powered
    </div>
    """,
    unsafe_allow_html=True
)