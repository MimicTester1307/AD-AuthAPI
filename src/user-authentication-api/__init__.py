from datetime import datetime
import os
from dotenv import load_dotenv

from pymongo.collection import Collection, ReturnDocument
from pymongo.server_api import ServerApi

import flask
from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError

from .model import Student, Staff

# configure flask
load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
pymongo = PyMongo(app)

# get a reference to the staff collection
staff_: Collection = pymongo.db.Staff
students: Collection = pymongo.db.Students
print(staff_)
print(students)


# Reading a single student
@app.route("/Students/<int:id_>", methods=["GET"])
def get_student(id_: int):
    student = students.find_one_or_404({"student_id": id_})
    return Student(**student).to_json()


# Reading a single staff
@app.route("/Staff/<int:id_>", methods=["GET"])
def get_staff(id_: int):
    staff = staff_.find_one_or_404({"staff_id": id_})
    return Staff(**staff).to_json()


# Listing all the students
@app.route("/")
@app.route("/Students/")
def list_students():
    page = int(request.args.get("page", 1))
    per_page = 10

    cursor = students.find().sort("student_id").skip(per_page * (page - 1)).limit(per_page)
    student_count = students.count_documents({})

    links = {
        "self": {"href": url_for(".list_students", page=page - 1, _external=True)},
        "last": {
            "href": url_for(
                ".list_students", page=(student_count // per_page) + 1, _external=True
            )
        },
    }

    # Add a 'prev' link if it's not on the first page:
    if page > 1:
        links["prev"] = {
            "href": url_for(".list_students", page=page - 1, _external=True)
        }
        # Add a 'next' link if it's not on the last page:
    if page - 1 < student_count // per_page:
        links["next"] = {
            "href": url_for(".list_students", page=page + 1, _external=True)
        }

    return {
        "student": [Student(**doc).to_json() for doc in cursor],
        "_links": links,
    }


# Listing all the staff
# Listing all the students
@app.route("/Staff/")
def list_staff():
    page = int(request.args.get("page", 1))
    per_page = 10

    cursor = staff_.find().sort("staff_id").skip(per_page * (page - 1)).limit(per_page)
    staff_count = staff_.count_documents({})

    links = {
        "self": {"href": url_for(".list_staff", page=page - 1, _external=True)},
        "last": {
            "href": url_for(
                ".list_staff", page=(staff_count // per_page) + 1, _external=True
            )
        },
    }

    # Add a 'prev' link if it's not on the first page:
    if page > 1:
        links["prev"] = {
            "href": url_for(".list_staff", page=page - 1, _external=True)
        }
        # Add a 'next' link if it's not on the last page:
    if page - 1 < staff_count // per_page:
        links["next"] = {
            "href": url_for(".list_staff", page=page + 1, _external=True)
        }

    return {
        "staff": [Staff(**doc).to_json() for doc in cursor],
        "_links": links,
    }


@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404


@app.errorhandler(DuplicateKeyError)
def resource_not_found(e):
    """
    An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
    """
    return jsonify(error=f"Duplicate key error."), 400


if __name__ == '__main__':
    app.run()
