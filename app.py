import os
import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #666;
            margin-bottom: 25px;
        }

        .result-box {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            background-color: #fafafa;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✉️ AI Email Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate, improve, rewrite, and grammatically correct professional emails using AI.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# GET GROQ API KEY
# ============================================================

def get_api_key():
    """
    Get the Groq API key.

    Priority:
    1. Streamlit Secrets
    2. Environment variable
    """

    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


API_KEY = get_api_key()


# ============================================================
# CHECK API KEY
# ============================================================

if not API_KEY:

    st.warning(
        "Groq API key is not configured. "
        "Add GROQ_API_KEY to Streamlit Secrets or your environment variables."
    )

    st.info(
        "For local testing, you can set the GROQ_API_KEY environment variable."
    )

    st.stop()


# ============================================================
# CREATE GROQ CLIENT
# ============================================================

try:
    client = Groq(api_key=API_KEY)

except Exception as error:
    st.error(f"Could not initialize Groq client: {error}")
    st.stop()


# ============================================================
# MODEL
# ============================================================

# Keep the model name in one place so it is easy to change later.
MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# AI FUNCTION
# ============================================================

def generate_ai_response(prompt):
    """
    Send a prompt to Groq and return the AI response.
    """

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional AI email writing assistant. "
                        "Help users write clear, natural, professional emails. "
                        "Follow the user's instructions carefully. "
                        "Do not invent information that the user did not provide."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as error:

        st.error(
            "Something went wrong while communicating with the AI."
        )

        st.exception(error)

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Email Settings")

    tone = st.selectbox(
        "Select Email Tone",
        [
            "Professional",
            "Friendly",
            "Formal",
            "Casual",
            "Apologetic",
            "Persuasive"
        ]
    )

    language = st.selectbox(
        "Email Language",
        [
            "English",
            "Urdu",
            "Roman Urdu"
        ]
    )

    st.divider()

    st.markdown("### 💡 Prompting Tip")

    st.write(
        "Give the AI enough context. "
        "A better prompt usually produces a better email."
    )

    st.markdown(
        """
        **Prompt Formula**

        Role + Task + Context + Tone + Format
        """
    )


# ============================================================
# MAIN INPUT SECTION
# ============================================================

st.header("📝 Create Your Email")

col1, col2 = st.columns(2)

with col1:

    recipient = st.text_input(
        "Recipient",
        placeholder="e.g. Manager, Client, Teacher"
    )

with col2:

    purpose = st.text_input(
        "Email Purpose",
        placeholder="e.g. Request two days leave"
    )


context = st.text_area(
    "Important Details",
    placeholder=(
        "Enter any important information you want "
        "to include in the email..."
    ),
    height=150
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.button(
    "✨ Generate Email",
    type="primary",
    use_container_width=True
)


# ============================================================
# GENERATE EMAIL
# ============================================================

if generate_button:

    if not purpose.strip():

        st.warning("Please enter the purpose of the email.")

    else:

        prompt = f"""
Create an email with the following requirements.

Recipient:
{recipient if recipient.strip() else "Not specified"}

Purpose:
{purpose}

Important details:
{context if context.strip() else "No additional details provided"}

Tone:
{tone}

Language:
{language}

Requirements:
- Create a suitable subject line.
- Write a clear and natural email.
- Keep it concise.
- Make it appropriate for the selected tone.
- Do not invent information.
- Preserve all important details supplied by the user.
- Return the result in this format:

Subject: [subject]

Email:
[email body]
"""

        with st.spinner("🤖 AI is writing your email..."):

            result = generate_ai_response(prompt)

        if result:

            st.session_state["email_result"] = result


# ============================================================
# DISPLAY GENERATED EMAIL
# ============================================================

if "email_result" in st.session_state:

    st.divider()

    st.header("📨 Generated Email")

    st.text_area(
        "Your Email",
        value=st.session_state["email_result"],
        height=350,
        key="generated_email"
    )


# ============================================================
# EMAIL ACTIONS
# ============================================================

if "email_result" in st.session_state:

    st.divider()

    st.header("🛠️ Modify Your Email")

    action = st.selectbox(
        "Choose an action",
        [
            "Improve Email",
            "Correct Grammar",
            "Make Shorter",
            "Make More Formal",
            "Make More Friendly",
            "Rewrite Email"
        ]
    )

    custom_instruction = st.text_area(
        "Optional Additional Instruction",
        placeholder="Tell AI exactly how you want to modify the email...",
        height=100
    )

    modify_button = st.button(
        "🔄 Modify Email",
        use_container_width=True
    )

    if modify_button:

        current_email = st.session_state["email_result"]

        action_instructions = {

            "Improve Email":
                "Improve the clarity, structure, professionalism, and readability.",

            "Correct Grammar":
                "Correct grammar, spelling, punctuation, and sentence structure. Preserve the original meaning.",

            "Make Shorter":
                "Make the email shorter and more concise while keeping all important information.",

            "Make More Formal":
                "Rewrite the email using a highly professional and formal tone.",

            "Make More Friendly":
                "Rewrite the email using a warm, friendly, and natural tone while remaining professional.",

            "Rewrite Email":
                "Rewrite the email to make it clearer, more natural, and more effective."
        }

        selected_instruction = action_instructions[action]

        prompt = f"""
You are an expert email editor.

Modify the following email.

Action:
{selected_instruction}

Additional user instruction:
{custom_instruction if custom_instruction.strip() else "No additional instruction."}

Important rules:
- Preserve the original meaning.
- Do not invent facts.
- Do not remove important information.
- Keep the email professional and natural.
- Return the complete revised email.
- Keep the subject line if one exists.

Original email:

{current_email}
"""

        with st.spinner("🤖 AI is modifying your email..."):

            result = generate_ai_response(prompt)

        if result:

            st.session_state["email_result"] = result

            st.rerun()


# ============================================================
# CLEAR BUTTON
# ============================================================

st.divider()

if st.button(
    "🗑️ Clear Everything",
    use_container_width=True
):

    st.session_state.clear()

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Built with Python + Streamlit + Groq API"
)
