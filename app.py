from flask import Flask, render_template, request, session, redirect
from gemini_response import get_gemini_response  # Ensure this script contains the response logic

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong key in production

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if "history" not in session:
#         session["history"] = []

#     response = ""
#     query = ""

#     if request.method == "POST":
#         query = request.form["query"]
#         response = get_gemini_response(query)
#         session["history"].append({"user": query, "bot": response})
#         session.modified = True

#     return render_template("index.html", query=query, response=response)

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    response = ""
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        print("Received query from user:", query)  # Debug print
        response = get_gemini_response(query)
        print("Bot response:", response)  # Debug print
        session["history"].append({"user": query, "bot": response})
        session.modified = True

    return render_template("index.html", query=query, response=response)

@app.route("/clear", methods=["POST"])
def clear():
    session.pop("history", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
