import flask
import configurations
import pymongo
from flask import *

from models.course import Course
from models.instructor import Instructor
from models.student import Students

app = Flask(__name__)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Courses routes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

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
@app.route('/add_course', methods=['POST'])
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

# This API will delete a course based on its id
@app.route("/delete_course/<passed_id>", methods=['DELETE'])
def delete_course(passed_id):
    # delete from course collection
    course_collection = pymongo.collection.Collection(configurations.db, 'courses')
    course_collection.delete_one({'_id': passed_id})
    # delete from registration collection
    registration_collection = pymongo.collection.Collection(configurations.db, 'registration')
    registration_collection.delete_one({'instructorId': passed_id})
    return "deleted"

# Get course information based on it's id
@app.route('/find_course/<search_param>', methods=['GET'])
def find_course(search_param):
    try:
        course_collection = pymongo.collection.Collection(configurations.db, 'courses')
        query = {"_id": search_param}
        courses = course_collection.find(query)
        courses_list = [course for course in courses]
        return jsonify(courses_list), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

# This API will update course's data 
@app.route("/update_course/<passed_id>", methods=['PATCH'])
def update_course(passed_id):
    course_collection = pymongo.collection.Collection(configurations.db, 'courses')
    courseId = passed_id
    updated_doc = course_collection.update_one({"_id": courseId}, {"$set": request.get_json()})
    if updated_doc:
        return "updated"
    else:
        flask.abort(404, "course Not Found")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Instructors routes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# List all availabel instructors info
@app.route("/instructors_Info", methods=['GET'])
def instructors_information_all():
    instructors_collection = pymongo.collection.Collection(configurations.db, 'instructors')
    instructors = instructors_collection.find()
    return [Instructor(**instructor).to_json() for instructor in instructors]

# Add new instructor
@app.route('/add_instructor', methods=['POST'])
def add_instructor():
    try:
        instructors_collection = pymongo.collection.Collection(configurations.db, 'instructors')
        instructor_data = request.json
        instructor = Instructor(**instructor_data)
        # Insert into MongoDB
        result = instructors_collection.insert_one(instructor.model_dump(by_alias=True))
        print(result)
        # Return success response
        return jsonify({"message": "The Instructor is added successfully", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get instructor's information based on it's id
@app.route('/find_instructor/<search_param>', methods=['GET'])
def find_instructor(search_param):
    try:
        instructor_collection = pymongo.collection.Collection(configurations.db, 'instructors')
        if search_param.isdigit():  # Check if the param is a valid ObjectId
            query = {"_id": search_param}
        else:
            name_parts = search_param.split(" ")
            query = {"$or": [{"firstName": name_parts[0]}, {"lastName": name_parts[-1]}]}
            print(query)

        Instructors = instructor_collection.find(query)
        Instructors_list = [Instructor for Instructor in Instructors]
        return jsonify(Instructors_list), 200

    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

# This API will delete a instructor based on its id
@app.route("/delete_instructor/<passed_id>", methods=['DELETE'])
def delete_instructor(passed_id):
    # delete from instructor collection
    instructor_collection = pymongo.collection.Collection(configurations.db, 'instructors')
    instructor_collection.delete_one({'_id': passed_id})
    # delete from instructors collection
    registration_collection = pymongo.collection.Collection(configurations.db, 'registration')
    registration_collection.delete_one({'instructorId': passed_id})
    return "deleted"

# This API will update instructor's data 
@app.route("/update_instructor/<passed_id>", methods=['PATCH'])
def update_instructor(passed_id):
    instructor_collection = pymongo.collection.Collection(configurations.db, 'instructors')
    instructorId = passed_id
    updated_doc = instructor_collection.update_one({"_id": instructorId}, {"$set": request.get_json()})
    if updated_doc:
        return "updated"
    else:
        flask.abort(404, "instructor Not Found")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% students routes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

# Get student's information based on it's id
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
def delete_student(passed_id):
    # delete from user collection
    student_collection = pymongo.collection.Collection(configurations.db, 'students')
    student_collection.delete_one({'_id': passed_id})
    # delete from student collection
    registration_collection = pymongo.collection.Collection(configurations.db, 'registration')
    registration_collection.delete_one({'studentId': passed_id})
    return "deleted"

# This API will update student's data
@app.route("/update_student/<passed_id>", methods=['PATCH'])
def update_student(passed_id):
    student_collection = pymongo.collection.Collection(configurations.db, 'students')
    studentId = passed_id
    updated_doc = student_collection.update_one({"_id": studentId}, {"$set": request.get_json()})
    if updated_doc:
        return "updated"
    else:
        flask.abort(404, "Student Not Found")


if __name__ == "__main__":
    app.run(host='0.0.0.0')