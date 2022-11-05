import uuid

from flask_session import Session
from flask import Flask, render_template, request


from helpers import read_csv, read_txt, check_all_courses, YT_lookup

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.static_folder = 'static'

# load up dictionaries
cdb = read_txt("cdb")
cdb100 = read_csv("cdb100")

# variables containing the options for the questionnaire
options_q = ["less", "more", "very"]

options_q3 = ["Machine Learning", "Data Analytics/ Science", "Blockchain",
              "Computer Science", "Programming with Python", "Internet of Things", "Web Development"]

options_q4 = ["Start a career in tech", "Boost my CV", "Learn about new technologies"]

keywords_q3 = [["Machine Learning"], ["Data Analytics", "Data Science"], ["Blockchain"],
               ["Computer Science"], ["Python", "Programming with Python"],
               ["Internet of Things"], ["Web Development", "Front-end development", "Fullstack Developer"]]

max_courses = 5


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/qs", methods=["GET", "POST"])
def qs():
    # get user input
    if request.method == "POST":
        # returns the answers as an index number of list options_q
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")

        # returns indeces of select elements in options_q3 that will be used as correspondants to the list of keywords
        List_q3 = request.form.getlist("q3")

        # get actual options chosen based on returned indeces, needed for titles in results.html
        List_q3_options = []
        for i in List_q3:
            List_q3_options.append(options_q3[int(i)])

        # returns list of indeces of options chosen in question 4 as strings
        List_q4 = request.form.getlist("q4")

        # get introductory videos based on first two questions
        intro_videos = {}
        if q1 == "less":
            intro_videos["Technology basics"] = (YT_lookup("Understanding Technology", 3))
        if q2 == "less":
            intro_videos["Programming basics"] = (YT_lookup("Programming basics", 3))
        else:
            intro_videos["Programming advanced"] = (YT_lookup("Programming advanced concepts", 3))

        # the list will contain for each choice(answer to questions three) a list of dictionaries with relevant courses
        choices = []
        # this list will be assigned a keys to the course vendor (currently coursera only)
        course_vendors = {}

        # ! COURSERA !
        for index in List_q3:
            # list of dictionaries with relevant course data
            courses = []
            # check if there is a course in coursera's top 100 with a name smilair to the user's choice
            check_all_courses(courses, index, keywords_q3, max_courses, List_q4=List_q4, cdb100=cdb100, cdb=cdb)
            # look for more courses until the desired number is reached
            if len(courses) < max_courses:
                courses = check_all_courses(courses, index, keywords_q3, max_courses, cdb=cdb)
            # assign every dict a 'unique' identifier later used for html ids
            ids = []
            for dict in courses:
                new_id = uuid.uuid1().int
                # check if they are unique
                if new_id not in ids:
                    ids.append(ids)
                    dict["ID"] = new_id
            # append the list of dictionaries to the outter list
            choices.append(courses)

        course_vendors["coursera"] = choices

        # youtube videos choice specific
        course_videos = []
        for index in List_q3:
            # look for videos using the keywords that correspond the input to q3
            course_videos.append(YT_lookup(" ".join(keywords_q3[int(index)]), 3))

        return render_template("results.html", course_vendors=course_vendors, List_q3_options=List_q3_options, intro_videos=intro_videos, course_videos=course_videos)
    else:
        return render_template("questionnaire.html", options_q=options_q, options_q3=options_q3, options_q4=options_q4)

