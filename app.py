from flask import Flask, request, render_template_string, redirect, url_for, session, send_from_directory
import sqlite3, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "CHANGE_ME_SECRET"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT)")
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
        c.execute("INSERT INTO users (username, password, role) VALUES ('user1', 'pass1', 'user')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template_string('''
    <h1>CTF Training Lab</h1>
    <ul>
        <li><a href="/login">تسجيل دخول</a></li>
        <li><a href="/posts">منشورات</a></li>
        <li><a href="/upload">رفع ملف</a></li>
        <li><a href="/profile/1">ملف المستخدم 1</a></li>
        <li><a href="/search">بحث</a></li>
    </ul>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        # SQL Injection هنا
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]
            return f"<h1>مرحبا {user[1]}</h1><p>الدور: {user[3]}</p><a href='/admin'>لوحة الإدارة</a>"
        return "<h1>فشل الدخول</h1>"
    return render_template_string('''
    <form method="POST">
        <input name="username" placeholder="اسم المستخدم"><br>
        <input name="password" placeholder="كلمة المرور" type="password"><br>
        <button>دخول</button>
    </form>
    ''')

@app.route('/admin')
def admin():
    if session.get('role') == 'admin':
        return "<h1>لوحة الإدارة</h1><p>نجحت في الوصول للوحة الإدارة!</p>"
    return "<h1>وصول مرفوض</h1>"

@app.route('/posts')
def posts():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT posts.id, users.username, posts.content FROM posts JOIN users ON posts.user_id = users.id")
    posts_data = c.fetchall()
    conn.close()
    # XSS هنا
    post_html = ""
    for p in posts_data:
        post_html += f"<div><h3>{p[1]}</h3><p>{p[2]}</p></div>"
    return f"<h1>المنشورات</h1>{post_html}<hr><form method='POST' action='/add_post'><input name='content'><button>إضافة</button></form>"

@app.route('/add_post', methods=['POST'])
def add_post():
    if not session.get('user_id'):
        return redirect('/login')
    content = request.form.get('content', '')
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (user_id, content) VALUES (?, ?)", (session['user_id'], content))
    conn.commit()
    conn.close()
    return redirect('/posts')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # File Upload بدون تحقق من الامتداد
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return f"<h1>تم الرفع</h1><p>الملف: {filename}</p><a href='/uploads/{filename}'>عرض الملف</a>"
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <button>رفع</button>
    </form>
    '''

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return f"<h1>ملف المستخدم</h1><p>ID: {user[0]}</p><p>اسم: {user[1]}</p><p>دور: {user[2]}</p>"
    return "<h1>غير موجود</h1>"

@app.route('/search')
def search():
    q = request.args.get('q', '')
    # XSS عاكس
    return f"<h1>نتائج البحث عن: {q}</h1><p>لا توجد نتائج</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))