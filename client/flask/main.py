from flask import Flask, render_template, request

app = Flask(__name__)
item = [i for i in range(1,40)]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form.getlist('checkbox[]'))

    return render_template("index.html", values=item)


if __name__ == '__main__':
    app.run()