from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)



GEMINI_API_KEY = "AIzaSyB_LSNLrNxWVvFDHpERtkAFOztn1YT4TQM"

if not GEMINI_API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY environment variable")

genai.configure(api_key=GEMINI_API_KEY)

# Use a fast model – change if needed
model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------
# 2. Helper: build AI prompt
# ---------------------------
def build_prompt(symptoms: str, last_meal: str, duration: str) -> str:
    """
    Create a clear medical-style prompt for Gemini.
    """
    return f"""
You are an experienced medical information assistant (NOT a doctor). 
Your job is to give **simple, clear, patient-friendly guidance** based on the user's description.

User details:
- Symptoms: {symptoms}
- Last meal: {last_meal or "Not provided"}
- Duration: {duration or "Not provided"} days

Rules:
1. Explain in **very simple language** (like talking to a non-medical person).
2. Do **NOT** give a confirmed diagnosis. Talk about **possible causes / possibilities** only.
3. ALWAYS include these sections in order, using Markdown formatting:

**Possible causes**
- (2–5 bullet points)

**Home care advice**
- (practical steps they can do at home)

**When to see a doctor**
- (clear signs when they should consult a doctor soon)

**Emergency warning signs**
- (red-flag symptoms where they should go to the emergency room or call local emergency services immediately)

**Lifestyle & prevention tips**
- (simple tips related to diet, sleep, water intake, etc.)

**Important safety note**
- Short, strong disclaimer that this is NOT a medical diagnosis,
  may be incomplete, and they must consult a doctor or local emergency services for serious or worsening symptoms.

4. Do NOT ask questions back. Just use the details already given.
5. Respond only in Markdown text.
    """


# ---------------------------
# 3. Routes
# ---------------------------

@app.route("/")
def index():
    # This will render templates/index.html
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    This endpoint is called from the frontend JS:
    fetch('/predict', { method: 'POST', body: JSON.stringify({...}) })
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON body."}), 400

    symptoms = (data.get("symptoms") or "").strip()
    last_meal = (data.get("last_meal") or "").strip()
    duration = (data.get("duration") or "").strip()

    if not symptoms:
        return jsonify({"error": "Symptoms are required."}), 400

    try:
        prompt = build_prompt(symptoms, last_meal, duration)

        # Call Gemini
        response = model.generate_content(prompt)
        advice_text = (response.text or "").strip()

        if not advice_text:
            raise ValueError("Empty response from Gemini")

        return jsonify({"advice": advice_text})

    except Exception as e:
        # Log error in backend console
        print("Error during /predict:", e)
        return jsonify({
            "error": "Failed to generate health advice. Please try again later."
        }), 500


if __name__ == "__main__":
    # For development
    app.run(host="0.0.0.0", port=5000, debug=True)
