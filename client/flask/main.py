from flask import Flask, render_template, request
from client import Client


client = Client()
app = Flask(__name__)
message = {'intent': 'get_all_tags'}
tags = client.send_message(message)['all_tags']
tags = [tag['tag_name'] for tag in tags]
tags = tags[:40]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        chosen_tags = request.form.getlist('checkbox[]')
        print(chosen_tags)
        message = {'intent': 'get_by_tags',
                   'tags': chosen_tags}
        print(client.send_message(message))

    return render_template("index.html", values=tags)


if __name__ == '__main__':
    app.run()