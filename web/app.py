from flask import Flask, request, render_template_string, redirect, url_for
import redis
import os


app = Flask(__name__)

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),  # по умолчанию 'redis'
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Слова</title>
</head>
<body>
    <h1>Слова</h1>
    <ul>
    {% for word in words %}
        <li>{{ word }} 
            <a href="{{ url_for('delete_word', word=word) }}">[удалить]</a>
        </li>
    {% endfor %}
    </ul>
    <form method="POST">
        <input type="text" name="word" placeholder="Введите слово" required>
        <button type="submit">Добавить</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_word = request.form["word"]
        r.rpush("words", new_word)  # добавить слово в список
        return redirect(url_for('index'))
    words = r.lrange("words", 0, -1)  # получить все слова
    return render_template_string(html, words=words)

@app.route("/delete/<word>")
def delete_word(word):
    r.lrem("words", 0, word)  # удалить все вхождения слова
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
