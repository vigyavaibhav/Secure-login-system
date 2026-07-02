 from flask import Flask, render_template, redirect, request, flash

from flask_bcrypt import Bcrypt

from flask_login import LoginManager, login_user, login_required, logout_user

from models import db, User

app = Flask(__name__)

app.config.from_pyfile("config.py")

db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]

        password=request.form["password"]

        user=User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password,password):

            login_user(user)

            return redirect("/dashboard")

        flash("Invalid Credentials")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")

if __name__=="__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
