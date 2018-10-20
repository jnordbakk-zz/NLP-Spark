# import necessary libraries
from flask import (
    Flask,
    render_template,
    jsonify,
    request)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Create a list to hold our data
my_data = []


@app.route("/api/data")
def data():
    print(my_data)
    return jsonify(my_data)


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        nickname = request.form["nickname"]
        age = request.form["age"]

        form_data = {
            "nickname": nickname,
            "age": int(age)
        }

        my_data.append(form_data)

        return "Thanks for the form data!"

    return render_template("form.html")


@app.route("/")
def home():
    return "Welcome!"


if __name__ == "__main__":
    app.run(debug=True)
