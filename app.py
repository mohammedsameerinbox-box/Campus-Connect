print ("CAMPUS CONNECT APP LOADED")

from flask import Flask,  render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,
    static_folder="static",
    template_folder="templates"
)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    college = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    student_name = db.Column(db.String(100))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))


# Home Page
@app.route("/")
def home():
    return render_template("index.html")
# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        student = Student.query.filter_by(
            email=email,
            password=password
        ).first()

        if student:
            return render_template(
                "dashboard.html",
                name=student.fullname
            )
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# Companies Page
@app.route("/companies")
def companies():
    return render_template("companies.html")


# Jobs Page
@app.route("/jobs")
def jobs():
    return render_template("companies.html")
# Profile Page
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/dashboard")
def dashboard():

    total_applications = Application.query.count()

    total_students = Student.query.count()

    total_companies = Company.query.count()

    return render_template(
        "dashboard.html",
        total_applications=total_applications,
        total_students=total_students,
        total_companies=total_companies
    )
@app.route("/apply")
def apply():

    new_application = Application(
        company="Infosys",
        student_name="Mohammed Sameer"
    )

    db.session.add(new_application)
    db.session.commit()

    return render_template("apply.html")


@app.route("/applications")
def applications():
    applications = Application.query.all()
    return render_template(
        "applications.html",
        applications=applications
    )

@app.route("/uploadresume", methods=["GET", "POST"])
def uploadresume():

    if request.method == "POST":

        file = request.files["resume"]

        filepath = "uploads/" + file.filename

        file.save(filepath)

        return "Resume Uploaded Successfully!"

    return render_template("uploadresume.html")

@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect("/admindashboard")

        return "Invalid Admin Login"

    return render_template("adminlogin.html")

@app.route("/admindashboard")
def admindashboard():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_applications = Application.query.count()

    return render_template(
        "admindashboard.html",
        total_students=total_students,
        total_companies=total_companies,
        total_applications=total_applications
    )

@app.route("/test")
def test():
    return "TEST WORKING"

@app.route("/hello")
def hello():
    return "HELLO SAMEER"

@app.route("/viewstudents")
def viewstudents():

    search = request.args.get("search")

    if search:
        students = Student.query.filter(
            Student.fullname.contains(search)
        ).all()
    else:
        students = Student.query.all()

    return render_template(
        "viewstudents.html",
        students=students
    )

@app.route("/deletestudent/<int:id>")
def deletestudent(id):

    student = Student.query.get(id)

    db.session.delete(student)

    db.session.commit()

    return redirect("/viewstudents")

@app.route("/deletecompany/<int:id>")
def deletecompany(id):
    company = Company.query.get(id)

    db.session.delete(company)

    db.session.commit()

    return redirect("/viewcompanies")

@app.route("/viewapplications")
def viewapplications():

    applications = Application.query.all()

    return str(applications)

@app.route("/addcompany", methods=["GET", "POST"])
def addcompany():

    if request.method == "POST":

        company = Company(
            company_name=request.form["company"],
            location=request.form["location"]
        )

        db.session.add(company)
        db.session.commit()

        return "Company Added Successfully"

    return render_template("addcompany.html")


@app.route("/viewcompanies")
def viewcompanies():

    companies = Company.query.all()

    return render_template(
        "viewcompanies.html",
        companies=companies
    )


@app.route("/searchcompany", methods=["GET", "POST"])
def searchcompany():

    companies = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        companies = Company.query.filter(
            Company.company_name.contains(keyword)
        ).all()

    return render_template(
        "searchcompany.html",
        companies=companies
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student = Student(
            fullname=request.form["fullname"],
            email=request.form["email"],
            college=request.form["college"],
            password=request.form["password"]
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)