from flask import Flask, render_template, request, url_for, redirect
from client import Client


client = Client()
app = Flask(__name__)
message = {'intent': 'get_all_tags'}
tags = client.send_message(message)['all_tags']
tags = [tag['tag_name'] for tag in tags]
tags = tags[:40]
result_games = []


@app.route('/', methods=['GET'])
def get_index():
    return render_template("index.html", values=tags)


@app.route('/', methods=['POST'])
def post_index():
    chosen_tags = request.form.getlist('checkbox[]')
    message = {'intent': 'get_by_tags',
               'tags': chosen_tags}
    result_games = client.send_message(message)["current_games"]
    result_games = [game for game in result_games]

    return render_template("games_page.html", games=result_games)


if __name__ == '__main__':
    app.run()
