from flask import Flask, render_template_string, request
import aiosqlite
import asyncio
import os

app = Flask(__name__)
DB_PATH = "database.db"
MEDIA_BASE = "media"

TEMPLATE = """
<!doctype html>
<title>Admin Panel</title>
<h2>Pengguna</h2>
<table border=1 cellpadding=5>
<tr><th>ID</th><th>Gender</th><th>Premium</th><th>Partner</th><th>Note</th><th>Foto</th><th>VN</th></tr>
{% for u in users %}
<tr>
<td>{{ u[0] }}</td>
<td>{{ u[1] }}</td>
<td>{{ '✅' if u[3] else '❌' }}</td>
<td>{{ u[2] or '-' }}</td>
<td>{{ u[5] or '-' }}</td>
<td>
  {% if u[6] %}
    {% for f in u[6] %}<a href="{{ f }}" target="_blank">🖼️</a> {% endfor %}
  {% endif %}
</td>
<td>
  {% if u[7] %}
    {% for v in u[7] %}<a href="{{ v }}" target="_blank">🔊</a> {% endfor %}
  {% endif %}
</td>
</tr>
{% endfor %}
</table>
"""

@app.route("/")
def index():
    users = asyncio.run(fetch_users())
    return render_template_string(TEMPLATE, users=users)

async def fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        rows = await db.execute_fetchall("SELECT * FROM users")
        results = []
        for r in rows:
            uid = r[0]
            photo_dir = os.path.join(MEDIA_BASE, "photo", str(uid))
            voice_dir = os.path.join(MEDIA_BASE, "voice", str(uid))
            photos = [f"/{photo_dir}/{f}" for f in os.listdir(photo_dir)] if os.path.isdir(photo_dir) else []
            voices = [f"/{voice_dir}/{f}" for f in os.listdir(voice_dir)] if os.path.isdir(voice_dir) else []
            results.append(r + (photos, voices))
        return results

if __name__ == "__main__":
    app.run(debug=True, port=8000)
