"""A one-page Flask app: a simple task list."""
from flask import Flask, redirect, render_template_string, request, url_for

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Task List</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #f4f6f8; margin: 0; }
    main { max-width: 480px; margin: 3rem auto; background: #fff; padding: 2rem;
           border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,.08); }
    h1 { margin-top: 0; }
    form.add { display: flex; gap: .5rem; }
    input[type=text] { flex: 1; padding: .6rem; border: 1px solid #ccc; border-radius: 6px; }
    button { padding: .6rem 1rem; border: 0; border-radius: 6px; cursor: pointer;
             background: #2563eb; color: #fff; }
    button.secondary { background: #6b7280; margin-top: 1rem; }
    ul { padding-left: 1.2rem; }
    li { margin: .4rem 0; }
    .empty { color: #6b7280; font-style: italic; }
  </style>
</head>
<body>git
  <main>
    <h1>Task List</h1>
    <form class="add" method="post" action="{{ url_for('index') }}">
      <input type="text" id="task-input" name="task" placeholder="What needs doing?"
             maxlength="100" required autofocus>
      <button type="submit" id="add-btn" name="action" value="add">Add</button>
    </form>

    {% if tasks %}
      <ul id="task-list">
        {% for task in tasks %}<li class="task">{{ task }}</li>{% endfor %}
      </ul>
      <form method="post" action="{{ url_for('index') }}">
        <button type="submit" id="clear-btn" class="secondary" name="action" value="clear">
          Clear all
        </button>
      </form>
    {% else %}
      <p id="empty-message" class="empty">No tasks yet. Add one above!</p>
    {% endif %}
  </main>
</body>
</html>
"""


def create_app():
    app = Flask(__name__)
    app.config["TASKS"] = []  # in-memory storage, fine for a demo

    @app.route("/", methods=["GET", "POST"])
    def index():
        tasks = app.config["TASKS"]
        if request.method == "POST":
            if request.form.get("action") == "clear":
                tasks.clear()
            else:
                task = request.form.get("task", "").strip()
                if task:
                    tasks.append(task[:100])
            return redirect(url_for("index"))  # Post/Redirect/Get
        return render_template_string(PAGE, tasks=tasks)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=False)
