from flask import Flask, request, render_template
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(nltk.corpus.stopwords.words('english'))

# Training data
training_data = [
    {"question": "What are the symptoms of a fever?", "intent": "symptoms"},
    {"question": "What are the symptoms of the flu?", "intent": "symptoms"},
    {"question": "How can I improve my sleep?", "intent": "general_advice"},
    {"question": "What should I do if I have a fever?", "intent": "symptoms"},
    {"question": "What are the ways to boost immunity?", "intent": "preventive_care"},
    {"question": "How can I prevent a cold?", "intent": "preventive_care"},
    {"question": "What should I do if I have a headache?", "intent": "symptoms"},
    {"question": "How do I sleep better at night?", "intent": "general_advice"},
    {"question": "What should I eat to stay healthy?", "intent": "preventive_care"}
]

# Split into questions and intents
questions = [item["question"] for item in training_data]
intents = [item["intent"] for item in training_data]

# Vectorize the questions using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Train the Naive Bayes classifier
model = MultinomialNB()
model.fit(X, intents)

# Responses dictionary to provide appropriate responses
responses = {
    "symptoms": "Common symptoms include fever, chills, and body aches.",
    "general_advice": "To improve sleep, maintain a consistent schedule, avoid caffeine, and create a restful environment.",
    "preventive_care": "To boost immunity, eat a balanced diet, exercise regularly, and get enough sleep.",
    "gratitude": "You're very welcome! 😊",
    "unknown": [
        "I'm not sure about that. Can you try asking in a different way?",
        "I don't have that information yet. Would you like to ask me about health or symptoms?",
        "Hmm, I can't seem to answer that. Try something else like healthcare tips."
    ]
}

# Flask application setup
app = Flask(__name__)

# Helper functions
def classify_intent(user_input):
    user_input_vector = vectorizer.transform([user_input])
    intent = model.predict(user_input_vector)[0]
    return intent

def get_response(intent):
    if intent == "unknown":
        return random.choice(responses["unknown"])
    return responses.get(intent, "Sorry, I don't understand your question.")

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    intent = classify_intent(user_input)
    response = get_response(intent)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # Use a different port to avoid conflicts
