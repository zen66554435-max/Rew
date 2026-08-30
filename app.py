from flask import Flask, request, render_template_string, redirect, url_for, session, send_from_directory, jsonify
import sqlite3, os, hashlib, uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sup3r_s3cr3t_k3y_chang3_m3")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_PATH = "site.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DB_PATH):
        try:
            test_conn = sqlite3.connect(DB_PATH)
            test_conn.execute("SELECT 1")
            test_conn.close()
        except:
            os.remove(DB_PATH)
    
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        role TEXT DEFAULT 'user'
    );
    CREATE TABLE IF NOT EXISTS galleries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_path TEXT,
        caption TEXT
    );
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gallery_id INTEGER,
        user_id INTEGER,
        comment TEXT
    );
    """)
    
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing == 0:
        conn.execute("INSERT INTO users (username, password, email, role) VALUES ('admin', ?, 'admin@site.local', 'admin')",
                    (hashlib.md5('Admin@123'.encode()).hexdigest(),))
        conn.execute("INSERT INTO users (username, password, email, role) VALUES ('ahmed', ?, 'ahmed@site.local', 'user')",
                    (hashlib.md5('password123'.encode()).hexdigest(),))
        conn.execute("INSERT INTO users (username, password, email, role) VALUES ('sara', ?, 'sara@site.local', 'user')",
                    (hashlib.md5('sara2024'.encode()).hexdigest(),))
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db()
    galleries = conn.execute("SELECT g.*, u.username FROM galleries g JOIN users u ON g.user_id = u.id ORDER BY g.id DESC LIMIT 10").fetchall()
    conn.close()
    return render_template_string('''
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>معرض الصور</title>
        <style>
            body { font-family: Tahoma, sans-serif; background: #f5f5f5; padding: 20px; margin: 0; }
            nav { background: #2c3e50; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
            nav a { color: white; margin: 0 10px; text-decoration: none; }
            h1 { color: #2c3e50; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
            .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .card img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; }
            .card a { color: #3498db; }
        </style>
    </head>
    <body>
        <nav>
            <a href="/">الرئيسية</a>
            <a href="/upload">رفع صورة</a>
            <a href="/login">تسجيل دخول</a>
            <a href="/debug">Debug</a>
            <a href="/api/users">API Users</a>
            <a href="/backup">Backup</a>
        </nav>
        <h1>معرض الصور</h1>
        <div class="grid">
            {% for g in galleries %}
            <div class="card">
                <img src="/{{ g.image_path }}" alt="{{ g.caption }}">
                <h3>{{ g.caption }}</h3>
                <p>بواسطة: {{ g.username }}</p>
                <a href="/gallery/{{ g.id }}">عرض التفاصيل</a>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    ''', galleries=galleries)

@app.route('/gallery/<int:id>', methods=['GET', 'POST'])
def gallery(id):
    conn = get_db()
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        user_id = session.get('user_id', 1)
        conn.execute("INSERT INTO comments (gallery_id, user_id, comment) VALUES (?, ?, ?)", (id, user_id, comment))
        conn.commit()
    gallery = conn.execute("SELECT g.*, u.username FROM galleries g JOIN users u ON g.user_id = u.id WHERE g.id = ?", (id,)).fetchone()
    comments = conn.execute("SELECT c.*, u.username FROM comments c JOIN users u ON c.user_id = u.id WHERE c.gallery_id = ? ORDER BY c.id DESC", (id,)).fetchall()
    conn.close()
    if not gallery:
        return "غير موجود", 404
    return render_template_string('''
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>{{ gallery.caption }}</title>
        <style>
            body { font-family: Tahoma, sans-serif; background: #f5f5f5; padding: 20px; }
            img { max-width: 600px; border-radius: 8px; }
            .comment { background: white; padding: 10px; margin: 10px 0; border-radius: 5px; }
            textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>{{ gallery.caption }}</h1>
        <img src="/{{ gallery.image_path }}" alt="{{ gallery.caption }}">
        <p>رفع بواسطة: {{ gallery.username }}</p>
        <h2>التعليقات</h2>
        {% for c in comments %}
        <div class="comment">
            <strong>{{ c.username }}</strong>: {{ c.comment }}
        </div>
        {% endfor %}
        <h3>أضف تعليقاً</h3>
        <form method="POST">
            <textarea name="comment" placeholder="اكتب تعليقك هنا..."></textarea><br>
            <button type="submit">إرسال</button>
        </form>
    </body>
    </html>
    ''', gallery=gallery, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        md5_pass = hashlib.md5(password.encode()).hexdigest()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{md5_pass}'"
        try:
            conn = get_db()
            user = conn.execute(query).fetchone()
            conn.close()
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect('/')
            error = "بيانات الدخول خاطئة"
        except Exception as e:
            error = f"خطأ: {str(e)}"
    return render_template_string('''
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل الدخول</title>
        <style>
            body { font-family: Tahoma, sans-serif; background: #ecf0f1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 40px; border-radius: 10px; width: 350px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            button { width: 100%; padding: 10px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .error { color: red; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>تسجيل الدخول</h2>
            {% if error %}<p class="error">{{ error }}</p>{% endif %}
            <form method="POST">
                <input type="text" name="username" placeholder="اسم المستخدم">
                <input type="password" name="password" placeholder="كلمة المرور">
                <button type="submit">دخول</button>
            </form>
        </div>
    </body>
    </html>
    ''', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('image')
        caption = request.form.get('caption', '')
        if file:
            filename = secure_filename(file.filename)
            if not filename:
                filename = "file.txt"
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(filepath)
            conn = get_db()
            cursor = conn.execute("INSERT INTO galleries (user_id, image_path, caption) VALUES (?, ?, ?)", (1, filepath, caption))
            conn.commit()
            gallery_id = cursor.lastrowid
            conn.close()
            return redirect(f'/gallery/{gallery_id}')
    return render_template_string('''
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>رفع صورة</title>
        <style>
            body { font-family: Tahoma, sans-serif; background: #ecf0f1; padding: 20px; }
            .upload-box { background: white; padding: 30px; border-radius: 10px; max-width: 500px; }
            input[type="file"] { margin: 15px 0; }
            input[type="text"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="upload-box">
            <h1>رفع صورة جديدة</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="image">
                <input type="text" name="caption" placeholder="وصف الصورة">
                <button type="submit">رفع</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    return jsonify({"query": q, "results": "لا توجد نتائج", "raw": q})

@app.route('/api/user/<int:id>')
def api_user(id):
    conn = get_db()
    user = conn.execute("SELECT id, username, email, role FROM users WHERE id=?", (id,)).fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(user))

@app.route('/api/users')
def api_users():
    conn = get_db()
    users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@app.route('/debug')
def debug():
    return jsonify({
        "secret_key": app.secret_key,
        "upload_folder": UPLOAD_FOLDER,
        "python_version": "3.11",
        "flag": "FLAG{S3CR3T_K3Y_F0UND}"
    })

@app.route('/backup')
def backup():
    if os.path.exists(DB_PATH):
        return send_from_directory('.', 'site.db', as_attachment=True)
    return "No backup", 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
