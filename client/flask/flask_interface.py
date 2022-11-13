from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/html")
def main_interface():
    return render_template("index.html", user_image="main_pic.jpg")
    
if __name__ == "__main__":
    app.run()
