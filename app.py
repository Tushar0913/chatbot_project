import streamlit as st
from config import model # Assuming 'model' is your Gemini model instance
import time
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="Gujarat Government Schemes & Citizen Services Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Header Section (Main Content Area) ---
st.title("🤝 Your Guide: Gujarat Government Services")
st.write(
    """
    Hello! I'm here to help you navigate **Gujarat's government schemes,
    certificates, and public services across various districts and cities**. Just ask me a question!
    """
)

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = {}

# --- Sidebar Content ---
with st.sidebar:
    # --- Project Details Section (New) ---
    st.title("👨‍👩‍👧‍👦 CitizenConnect Gujarat") # A catchy name for your chatbot
    st.markdown(
        """
        AI-powered assistant providing **clear, actionable information on Gujarat government schemes and citizen services**.
        """
    )

    st.markdown("---") # Separator

    st.subheader("🌍 UN SDG Alignment")
    st.markdown(
        """
        This project primarily aligns with:
        - **Goal 16: Peace, Justice and Strong Institutions**
          _"Ensure public access to information and protect fundamental freedoms."_
        - **Goal 10: Reduced Inequalities**
          _"Reduce inequality within and among countries."_
        """
    )
    st.info(
        """
        By simplifying access to government information, CitizenConnect Gujarat empowers citizens,
        fosters transparency, and ensures that essential services reach everyone,
        contributing to a more equitable and informed society.
        """
    )

    st.markdown("---") # Separator to separate project info from chat options

    st.header("Chat Options")

    if st.button("➕ Start New Chat", use_container_width=True):
        new_chat_id = str(uuid.uuid4())
        st.session_state.chat_history[new_chat_id] = []
        st.session_state.current_chat_id = new_chat_id
        st.session_state.last_question = ""
        st.session_state.chat_titles[new_chat_id] = f"New Chat {len(st.session_state.chat_titles) + 1}"
        st.rerun()

    st.markdown("---")
    st.subheader("Previous Chats")

    if st.session_state.chat_history:
        sorted_chat_ids = sorted(st.session_state.chat_history.keys(),
                                 key=lambda x: st.session_state.chat_history[x][0].get('timestamp', 0)
                                 if st.session_state.chat_history[x] else 0,
                                 reverse=True)

        for chat_id in sorted_chat_ids:
            title = st.session_state.chat_titles.get(chat_id, f"Chat {chat_id[:8]}...")
            if st.button(title, key=f"load_chat_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.last_question = ""
                st.rerun()
    else:
        st.info("No previous chats. Start a new one!")

    st.markdown("---")
    st.subheader("Settings")
    # The 'Creativity (Temperature)' slider has been removed as requested.
    # A default temperature value is set for the model.
    temperature = 0.7 # Default temperature value after removing the slider

    if st.button("🚫 Clear All Chats", help="This will permanently delete all chat history.", use_container_width=True):
        if st.session_state.get("confirm_clear_all", False):
            st.session_state.chat_history = {}
            st.session_state.current_chat_id = None
            st.session_state.last_question = ""
            st.session_state.chat_titles = {}
            st.session_state.confirm_clear_all = False
            st.success("All chats cleared!")
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.confirm_clear_all = True
            st.warning("Are you sure? This action cannot be undone.")
            if st.button("Yes, Clear All Chats", type="secondary"):
                st.session_state.confirm_clear_all = True
                st.rerun()
            if st.button("No, Cancel"):
                st.session_state.confirm_clear_all = False
                st.rerun()

# Ensure a chat session is active, or create a new one on initial load
if st.session_state.current_chat_id is None and not st.session_state.chat_history:
    new_chat_id = str(uuid.uuid4())
    st.session_state.chat_history[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id
    st.session_state.chat_titles[new_chat_id] = "First Chat"
    st.rerun()

# --- Chat Function ---
def generate_chatbot_response(user_query, temp):
    """Generates a response from the Gemini model with a tailored prompt."""
    prompt = (
        f"You are a helpful and clear chatbot specializing in providing step-by-step guidance "
        f"about government schemes and citizen services across **Gujarat, India**. "
        f"Your responses should be easy to understand for the average citizen, actionable, and concise. "
        f"If the question is outside the scope of Gujarat government services, "
        f"kindly state that you can only assist with Gujarat-related government queries.\n\n"
        f"User Question: {user_query}\n\n"
        f"Chatbot Answer:"
    )
    try:
        # Pass the temperature to the model's generate_content method if it supports it.
        # Assuming 'model' is a Gemini model instance that accepts 'temperature' in generate_content.
        # If your model's generate_content method doesn't take 'temperature' directly,
        # you might need to configure it when initializing the model instance (e.g., model = genai.GenerativeModel(..., generation_config={"temperature": temp}))
        response = model.generate_content(prompt, generation_config={"temperature": temp})
        with st.spinner("Thinking..."):
            time.sleep(0.5)
        return response.text
    except Exception as e:
        st.error(f"Apologies, an error occurred: {e}. Please try again.")
        return "I'm sorry, I couldn't process your request right now. Please try again later."

# --- Display Chat History for the Current Chat ---
chat_container = st.container()

with chat_container:
    if st.session_state.current_chat_id in st.session_state.chat_history:
        current_messages = st.session_state.chat_history[st.session_state.current_chat_id]
        for message in current_messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])
    else:
        st.info("Start a new chat or select a previous one from the sidebar.")

# --- Predefined Suggestions ---
st.markdown("---")
st.subheader("Quick Suggestions:")

suggestion_questions = [
    "How can I apply for a new ration card in Gujarat?",
    "What are the benefits of the Mukhyamantri Amrutam Yojana?",
    "Tell me about the process for obtaining a domicile certificate in Gujarat.",
    "Where can I find information on agricultural schemes in Gujarat?"
]

cols = st.columns(len(suggestion_questions))
for i, question in enumerate(suggestion_questions):
    if cols[i].button(question, key=f"suggestion_{i}"):
        if st.session_state.current_chat_id is None:
             new_chat_id = str(uuid.uuid4())
             st.session_state.chat_history[new_chat_id] = []
             st.session_state.current_chat_id = new_chat_id
             st.session_state.chat_titles[new_chat_id] = question[:30] + "..." if len(question) > 30 else question

        # Ensure temperature is defined before calling generate_chatbot_response
        # It's now a fixed value of 0.7 as the slider is removed.
        temperature = 0.7

        st.session_state.chat_history[st.session_state.current_chat_id].append({"role": "user", "content": question, "timestamp": time.time()})

        bot_response = generate_chatbot_response(question, temperature)
        st.session_state.chat_history[st.session_state.current_chat_id].append({"role": "assistant", "content": bot_response, "timestamp": time.time()})

        if st.session_state.chat_titles[st.session_state.current_chat_id].startswith("New Chat"):
            st.session_state.chat_titles[st.session_state.current_chat_id] = question[:30] + "..." if len(question) > 30 else question

        st.rerun()

# --- User Input Form ---
user_query = st.chat_input("Ask about schemes, certificates, or services across Gujarat...")

if user_query and user_query != st.session_state.last_question:
    if st.session_state.current_chat_id is None:
        new_chat_id = str(uuid.uuid4())
        st.session_state.chat_history[new_chat_id] = []
        st.session_state.current_chat_id = new_chat_id
        st.session_state.chat_titles[new_chat_id] = user_query[:30] + "..." if len(user_query) > 30 else user_query

    st.session_state.last_question = user_query

    # Ensure temperature is defined before calling generate_chatbot_response
    # It's now a fixed value of 0.7 as the slider is removed.
    temperature = 0.7

    st.session_state.chat_history[st.session_state.current_chat_id].append({"role": "user", "content": user_query, "timestamp": time.time()})

    bot_response = generate_chatbot_response(user_query, temperature)
    st.session_state.chat_history[st.session_state.current_chat_id].append({"role": "assistant", "content": bot_response, "timestamp": time.time()})

    if st.session_state.chat_titles[st.session_state.current_chat_id].startswith("New Chat"):
        st.session_state.chat_titles[st.session_state.current_chat_id] = user_query[:30] + "..." if len(user_query) > 30 else user_query

    st.rerun()

# --- Footer or Additional Info (Optional) ---
st.markdown("---")
st.markdown(
    """
    <small>_This chatbot is for informational purposes only. For official information,
    please refer to government websites or departments._</small>
    """,
    unsafe_allow_html=True
)
