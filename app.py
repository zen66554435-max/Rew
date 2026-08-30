from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory, jsonify, make_response
import sqlite3, os, hashlib, uuid, base64
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sup3r_s3cr3t_k3y_chang3_m3")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect("site.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        role TEXT DEFAULT 'user',
        is_active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS galleries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_path TEXT,
        caption TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gallery_id INTEGER,
        user_id INTEGER,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS api_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        token TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)
    
    # بيانات افتراضية
    try:
        conn.execute("INSERT INTO users (username, password, email, role) VALUES ('admin', '?', 'admin@site.local', 'admin')",
                    (hashlib.md5('Admin@123'.encode()).hexdigest(),))
        conn.execute("INSERT INTO users (username, password, email, role) VALUES ('ahmed', '?', 'ahmed@site.local', 'user')",
                    (hashlib.md5('password123'.encode()).hexdigest(),))
        conn.execute("INSERT INTO users (username, password, email, role) VALUES ('sara', '?', 'sara@site.local', 'user')",
                    (hashlib.md5('sara2024'.encode()).hexdigest(),))
        conn.execute("INSERT INTO settings (key, value) VALUES ('site_name', 'معرض الصور')")
        conn.execute("INSERT INTO settings (key, value) VALUES ('admin_email', 'hidden_admin@site.local')")
        conn.execute("INSERT INTO settings (key, value) VALUES ('backup_path', '/backup/site_backup.zip')")
        conn.execute("INSERT INTO settings (key, value) VALUES ('secret_key', '')".replace('', 'REPLACE_ME'))
        conn.commit()
    except:
        pass
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return "403 Forbidden", 403
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    conn = get_db()
    galleries = conn.execute("""
        SELECT galleries.*, users.username FROM galleries 
        JOIN users ON galleries.user_id = users.id 
        ORDER BY galleries.created_at DESC LIMIT 12
    """).fetchall()
    conn.close()
    return render_template('index.html', galleries=galleries)

@app.route('/gallery/<int:id>')
def gallery(id):
    conn = get_db()
    gallery = conn.execute("""
        SELECT galleries.*, users.username FROM galleries 
        JOIN users ON galleries.user_id = users.id 
        WHERE galleries.id = ?
    """, (id,)).fetchone()
    comments = conn.execute("""
        SELECT comments.*, users.username FROM comments 
        JOIN users ON comments.user_id = users.id 
        WHERE comments.gallery_id = ?
    """, (id,)).fetchall()
    conn.close()
    if not gallery:
        return "غير موجود", 404
    return render_template('gallery.html', gallery=gallery, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        # SQL Injection هنا عمداً
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashlib.md5(password.encode()).hexdigest()}'"
        conn = get_db()
        user = conn.execute(query).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(request.args.get('next') or url_for('home'))
        error = "بيانات الدخول خاطئة"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('image')
        caption = request.form.get('caption', '')
        if file:
            # ثغرة: لا يوجد تحقق من نوع الملف الحقيقي
            filename = secure_filename(file.filename)
            # ثغرة: امتداد مزدوج
            filepath = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
            file.save(filepath)
            conn = get_db()
            conn.execute("INSERT INTO galleries (user_id, image_path, caption) VALUES (?, ?, ?)",
                        (session['user_id'], filepath, caption))
            conn.commit()
            conn.close()
            return redirect(url_for('gallery', id=conn.execute("SELECT last_insert_rowid()").fetchone()[0]))
    return render_template('upload.html')

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    # ثغرة: XSS انعكاسي في JSON بدون تهريب
    return jsonify({"query": q, "results": "لا توجد نتائج", "raw": q})

@app.route('/api/user/<int:id>')
def api_user(id):
    conn = get_db()
    user = conn.execute("SELECT id, username, email, role FROM users WHERE id=?", (id,)).fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))

@app.route('/api/gallery/<int:id>')
def api_gallery(id):
    conn = get_db()
    gallery = conn.execute("SELECT * FROM galleries WHERE id=?", (id,)).fetchone()
    conn.close()
    if not gallery:
        return jsonify({"error": "Gallery not found"}), 404
    return jsonify(dict(gallery))

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    conn = get_db()
    users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
    galleries_count = conn.execute("SELECT COUNT(*) as cnt FROM galleries").fetchone()['cnt']
    conn.close()
    return render_template('admin.html', users=users, galleries_count=galleries_count)

@app.route('/admin/export')
@login_required
@admin_required
def admin_export():
    conn = get_db()
    users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
    conn.close()
    # ثغرة: تصدير بيانات بدون تعقيم
    data = "ID,Username,Email,Role\n"
    for u in users:
        data += f"{u['id']},{u['username']},{u['email']},{u['role']}\n"
    response = make_response(data)
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = "attachment; filename=users.csv"
    return response

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email', '')
        # ثغرة: SSTI محتمل في رسالة الترحيب
        conn = get_db()
        conn.execute("UPDATE users SET email=? WHERE id=?", (email, session['user_id']))
        conn.commit()
        conn.close()
        return render_template('profile.html', message=f"تم تحديث البريد إلى: {email}")
    conn = get_db()
    user = conn.execute("SELECT id, username, email, role FROM users WHERE id=?", (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '')
        # ثغرة: كشف وجود المستخدم
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user:
            return "تم إرسال رابط إعادة التعيين إلى بريدك الإلكتروني"
        return "هذا البريد غير مسجل"
    return render_template('forgot.html')

@app.route('/debug')
def debug():
    # ثغرة: كشف معلومات حساسة
    import sys
    return jsonify({
        "python_version": sys.version,
        "app_config": dict(app.config),
        "secret_key": app.secret_key,
        "upload_folder": UPLOAD_FOLDER
    })

@app.route('/backup')
def backup():
    # ثغرة: الوصول لنسخة احتياطية بدون تحقق
    return send_from_directory('.', 'site.db', as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
