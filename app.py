import streamlit as st
st.set_page_config(layout="wide")
import google.generativeai as genai
import re
import json


# Custom CSS for hospital theme, input visibility, and responsive design
st.markdown(
    """
    <style>
    body {
        background-color: #e6f2ff !important;
    }
    .main {
        background-color: #f8fbfd !important;
        border-radius: 16px;
        padding: 2rem 2rem 1rem 2rem;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
        margin-top: 2rem;
    }
    .stButton>button {
        background-color: #0077b6;
        color: white;
        border-radius: 8px;
        font-size: 1.1rem;
        padding: 0.5rem 2rem;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background-color: #023e8a;
        color: #fff;
    }
    /* Fix input/select box visibility */
    .stSelectbox>div>div, .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #e6f2ff !important;
        color: #023e8a !important;
        border: 1px solid #0077b6 !important;
    }
    .stSelectbox>div>div>div {
        color: #023e8a !important;
    }
    .stTextInput>div>div>input::placeholder {
        color: #7baedc !important;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Make the main container use the full width */
    .main .block-container {
        max-width: 100vw !important;
        padding-left: 2vw;
        padding-right: 2vw;
    }
    /* Remove Streamlit's default centering */
    .main {
        align-items: stretch !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the provided Gemini API key directly
GEMINI_API_KEY = "AIzaSyBTE2AS4DKJGuJE9O5CYWsbrYFkk3xwDWE"

genai.configure(api_key=GEMINI_API_KEY)

# Title, tagline, and form immediately below the top, all center-aligned
st.markdown("<h1 style='color:#023e8a; margin: 0.5rem 0 0.2rem 0; text-align: center;'>Cardiovascular Health Assessment</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#0077b6; font-size:1.2rem; margin: 0 0 1.5rem 0; text-align: center;'>A telehealth tool for cardiovascular risk screening</p>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<h3 style='color:#0077b6; text-align: center;'>📝 Your Information Please!</h3>", unsafe_allow_html=True)

with st.form('health_form'):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input('👤 Age', min_value=0, max_value=120, step=1, help="Enter your age in years.")
        gender = st.selectbox('⚧️ Gender', ['male', 'female', 'other'])
        blood_pressure = st.text_input('🩺 Blood Pressure (systolic/diastolic)', placeholder='e.g., 120/80', help="Format: systolic/diastolic")
    with col2:
        cholesterol = st.number_input('🧪 Cholesterol (mg/dL)', min_value=0, max_value=1000, step=1, help="Enter your cholesterol level.")
        smoking_status = st.selectbox('🚬 Smoking Status', ['non-smoker', 'former-smoker', 'current-smoker'])
        diabetes_status = st.selectbox('🍬 Diabetes Status', ['no-diabetes', 'pre-diabetes', 'type1', 'type2'])
    submitted = st.form_submit_button('Submit', use_container_width=True)

if submitted:
    st.info('Submitting your data to the AI model...')
    prompt = f"""
    A user has provided the following health information:
    - Age: {age}
    - Gender: {gender}
    - Blood Pressure: {blood_pressure}
    - Cholesterol: {cholesterol} mg/dL
    - Smoking Status: {smoking_status}
    - Diabetes Status: {diabetes_status}

    Based on this information, assess whether the user is at risk for cardiovascular disease. Respond ONLY with a valid JSON object with two fields: 'healthy' (true/false) and 'consult' (true/false, whether the user should consult a doctor). Do not include any explanation or extra text.
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            result = json.loads(match.group(0))
            st.markdown("---")
            st.markdown("<h3 style='color:#0077b6;'>💡 Assessment Result</h3>", unsafe_allow_html=True)
            if result.get('healthy'):
                st.success('✅ You are Healthy! ❤️')
            else:
                st.error('⚠️ You are At Risk! 💔')
            if result.get('consult'):
                st.warning('👨‍⚕️ We recommend that you consult with a doctor for a more comprehensive evaluation.')
            else:
                st.info("👍 While your results look good, it's always beneficial to maintain a healthy lifestyle and have regular check-ups.")
        else:
            st.error("Could not find a JSON object in the model's response.")
            st.stop()
    except Exception as e:
        st.error(f'Error processing your request: {e}') 
