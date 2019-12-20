from flask import render_template, url_for, flash, redirect, request
from blog_ku import app, db, bcrypt
from blog_ku.forms import Registrasi_F, Login_F
from blog_ku.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts=[
    {
    'penulis':'KASMIL PAPALIA',
    'title':"Blog Post 1",
    'konten':'post pertama KASMIL PAPALIA',
    'tgl_post':'oktober 10, 2019'
    },
    {
    'penulis':'KASMIL',
    'title':"Blog Post 2",
    'konten':'post 2 akan di tampilkan di halaman berikutnya',
    'tgl_post':'oktober 30, 2019'
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title='Home', posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About', posts=posts)

@app.route("/registrasi", methods=['GET','POST'])
def registrasi():
    form = Registrasi_F()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Akun {form.username.data} berhasil ditambahkan!', 'success')
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    return render_template("registrasi.html", title="Registrasi", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login_F()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login gagal..!, periksa Username dan Password', 'danger')
            return redirect(url_for('home'))
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")