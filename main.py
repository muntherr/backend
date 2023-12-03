import flask
import configurations
import pymongo
from flask import *

from models.course import Course
from models.instructor import Instructor
from models.student import Students

app = Flask(__name__)

# List all availabel courses info
@app.route("/courses_Info", methods=['GET'])
def courses_information_all():
    try:
        courses_collection = pymongo.collection.Collection(configurations.db, 'courses')
        courses = courses_collection.find()
        return [Course(**course).to_json() for course in courses]

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Add a new courses
@app.route('/add_new_course', methods=['POST'])
def add_new_course():
    try:
        courses_collection = pymongo.collection.Collection(configurations.db, 'courses')
        courses_data = request.json
        course = Course(**courses_data)
        # Insert into MongoDB
        result = courses_collection.insert_one(course.model_dump(by_alias=True))
        # Return success response
        return jsonify({"message": "The Course added successfully", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# List all availabel instructors info
@app.route("/instructors_Info", methods=['GET'])
def instructors_information_all():
    instructors_collection = pymongo.collection.Collection(configurations.db, 'instructors')
    instructors = instructors_collection.find()
    return [Instructor(**instructor).to_json() for instructor in instructors]

########################## :Instructors routes

# Add new instructor
@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    try:
        instructors_collection = pymongo.collection.Collection(configurations.db, 'instructors')
        instructor_data = request.json
        instructor = Instructor(**instructor_data)
        # Insert into MongoDB
        result = instructors_collection.insert_one(instructor.model_dump(by_alias=True))
        # Return success response
        return jsonify({"message": "The Instructor is added successfully", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

########################## :students routes


# List all availabel students info
@app.route("/students_Info", methods=['GET'])
def students_information_all():
    students_collection = pymongo.collection.Collection(configurations.db, 'students')
    students = students_collection.find()
    return [Students(**student).to_json() for student in students]


# Add a new student
@app.route('/add_student', methods=['POST'])
def add_new_student():
    try:
        students_collection = pymongo.collection.Collection(configurations.db, 'students')
        students_data = request.json
        student = Students(**students_data)
        # Insert into MongoDB
        result = students_collection.insert_one(student.model_dump(by_alias=True))
        # Return success response
        return jsonify({"message": "The student is added successfully", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/find_student/<search_param>', methods=['GET'])
def find_student(search_param):
    try:
        students_collection = pymongo.collection.Collection(configurations.db, 'students')
        if search_param.isdigit():  # Check if the param is a valid ObjectId
            query = {"_id": search_param}
        else:
            name_parts = search_param.split(" ")
            query = {"$or": [{"firstName": name_parts[0]}, {"lastName": name_parts[-1]}]}
            print(query)

        students = students_collection.find(query)
        students_list = [student for student in students]
        return jsonify(students_list), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500


# This API will delete a student based on its id
@app.route("/delete_student/<passed_id>", methods=['DELETE'])
def delete_patient(passed_id):
    # delete from user collection
    user_collection = pymongo.collection.Collection(configurations.db, 'students')
    user_collection.delete_one({'_id': passed_id})
    # delete from patient collection
    patient_collection = pymongo.collection.Collection(configurations.db, 'registration')
    patient_collection.delete_one({'studentId': passed_id})
    return "deleted"

# This API will update patient's data based on patient id
@app.route("/update_student/<passed_id>", methods=['PATCH'])
def update_student(passed_id):
    patient_collection = pymongo.collection.Collection(configurations.db, 'students')
    patientId = passed_id
    updated_doc = patient_collection.update_one({"_id": patientId}, {"$set": request.get_json()})
    if updated_doc:
        return "updated"
    else:
        flask.abort(404, "Patient Not Found")


if __name__ == "__main__":
    app.run(host='0.0.0.0')