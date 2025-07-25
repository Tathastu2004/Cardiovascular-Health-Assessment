# Cardiovascular Health Assessment (Streamlit + Gemini API)

This app allows users to input their health data and receive an AI-powered cardiovascular risk assessment using Google's Gemini API.

## Features
- Collects user health data via a Streamlit web form
- Sends data to Gemini API for risk assessment (no local calculation)
- Displays results and recommendations

## Setup

1. **Clone the repository**
2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up your Gemini API key**

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

4. **Run the app**

```bash
streamlit run app.py
```

5. **Open your browser**

Go to [http://localhost:8501](http://localhost:8501) to use the app.

## Notes
- You must have a valid Gemini API key from Google.
- All risk assessment is performed by the Gemini model, not locally. 