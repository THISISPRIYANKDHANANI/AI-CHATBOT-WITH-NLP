import google.generativeai as genai
import spacy

# --- Load spaCy model ---
nlp = spacy.load("en_core_web_sm")

# --- Define preprocessing function ---
def preprocess_input(user_input):
    doc = nlp(user_input)
    return " ".join([token.lemma_ for token in doc if token.is_alpha and not token.is_stop])

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyC7Tppb23CtEpmqOPaRdmoN3r5Fu4BXBF8")  # Replace with your key

# --- Initialize Gemini model ---
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction = """
You are a highly intelligent, emotionally aware, and friendly AI assistant named CodTech Buddy.
Your role is to chat naturally with users like a helpful friend or companion. Respond in a warm, caring, and supportive tone.
Be empathetic, curious, and helpful — whether the user asks questions about learning, coding, emotions, or everyday problems.
If appropriate, you may use emojis to express emotions and make the conversation more human-like and engaging.

Your goals:
- Be helpful, honest, and emotionally supportive
- Make users feel understood, not just informed
- Use friendly and conversational language
- Use markdown formatting for better readability
- Add warmth and clarity to your answers without being overly formal
"""
)

def get_gemini_response(user_input):
    try:
        # Skip preprocessing for short/simple inputs
        if len(user_input.strip().split()) <= 3:
            processed_query = user_input.strip()
        else:
            processed_query = preprocess_input(user_input)

        if not processed_query.strip():
            return "⚠️ Please enter a valid question."

        response = model.generate_content(processed_query)

        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'candidates') and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "⚠️ No content found in the response."

    except Exception as e:
        return f"❌ Error: {str(e)}"

