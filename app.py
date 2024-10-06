from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management

# In-memory storage for demonstration purposes
users = {}

# Chatbot responses dictionary
responses = { 
    "hello": "Hi there! How can I assist you today?",
    "how are you": "I'm fine, thank you! How about you?",
    "bye": "Goodbye! Take care.",
    "your name": "I'm a chatbot created to assist you!",
    "weather": "I'm not sure about the weather right now. You can check a weather app!",
    "time": "Sorry, I don't know the current time. Check your device's clock!",
    "location": "I'm virtual, so I don't have a physical location.",
    "help": "I can assist you with basic questions. Try asking me about the weather, time, or greetings.",
    
    # National Consumer Helpline Queries
    "national consumer helpline": "The National Consumer Helpline (NCH) assists consumers in resolving their complaints and provides guidance. How can I help you with NCH?",
    "nch helpline number": "The National Consumer Helpline toll-free number is 1800-11-4000 or 14404.",
    "file a complaint": ("To file a complaint with NCH, you can visit their website "
                        "<a href='https://consumerhelpline.gov.in/' target='_blank'>here</a> "
                        "or call their toll-free number 1800-11-4000. You can also use the NCH mobile app."),
    "nch services": "The NCH offers services like resolving consumer complaints, providing information about consumer rights, and addressing issues related to defective products, misleading advertisements, and more.",
    "consumer rights": "As a consumer, you have the right to safety, information, choice, redressal, and consumer education. NCH helps enforce these rights.",
    "e-commerce complaints": "For issues related to e-commerce purchases, NCH can assist with grievances such as delayed delivery, defective products, or non-compliance with refund policies.",
    "complaint status": "You can check the status of your complaint by visiting the NCH website or contacting their helpline directly.",
    "refund issue": "If you're facing refund issues with a product or service, you can file a complaint with the National Consumer Helpline for assistance.",
    "misleading advertisement": "If you come across a misleading advertisement, you can report it to NCH for further action."
}

# Function to get chatbot response
def chatbot_response(user_input):
    user_input = user_input.lower()  
    for query, response in responses.items():
        if query in user_input: 
            return response
    if "complain" in user_input or "complaint" in user_input:
        return responses.get("file a complaint", "How can I assist you with a complaint?")
    return "Sorry, I don't understand that. Can you please ask something else?"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")

        if action == "signup":
            if username in users:
                return "User already exists! Try logging in."
            users[username] = password
            session["user"] = username  # Log the user in after signup
            return redirect(url_for("chat"))

        elif action == "login":
            if username in users and users[username] == password:
                session["user"] = username  # Log the user in
                return redirect(url_for("chat"))
            else:
                return "Invalid username or password. Try again."
    return render_template("auth.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/chat")
def chat():
    if "user" in session:
        return render_template("chat.html", username=session["user"])
    return redirect(url_for("auth"))

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    response = chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
