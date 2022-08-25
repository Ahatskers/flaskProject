from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

'''Initializing application and DB (SQLite)'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)


class User(db.Model):
    """creating the User class to registration in DB"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    telephone_number = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.email


@app.route("/index.html", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def index():
    """
    Main page with user registration form,
    also we process the requests from index.html page.
    And if it's necessary add new user in DB
    """
    if request.method == "POST":
        email = request.form['email']
        tel = request.form['telephone_number']
        message = request.form['message']

        user = User(email=email, telephone_number=tel, message=message)
        try:
            db.session.add(user)
            db.session.commit()
            redirect('/')
        except:
            return "User addition error"
    return render_template("index.html")


@app.route("/view")
def view():
    """
    Here we can view users from DB and also search them by email or telephone number.
    """
    search = request.args.get("search")
    if search:
        user = User.query.filter(User.email.contains(search) | User.telephone_number.contains(search)).all()
    else:
        user = User.query.all()
    return render_template("view.html", user=user)  # передаем в шаблон список


if __name__ == "__app__":
    app.run(debug=True)
