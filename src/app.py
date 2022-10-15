from flask import Flask, Response, request
from datetime import datetime
import json
from flask_cors import CORS
from student_resource import StudentResource

app = Flask(__name__)

CORS(app)

@app.get("/api/health")
def hello_world():
    t = str(datetime.now())
    msg = {
        "name": "Students Microservice",
        "health": "Good",
        "at time": t
    }
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    return result

@app.route("/api/insert", methods=['POST'])
def insert_student():
    request_json = request.json
    insert_status = StudentResource.insert_student(request_json)
    if insert_status == 1:
        msg = {
            "message": "Student added successfully!"
        }
        result = Response(json.dumps(msg), status=200, content_type="application/json")
        return result
    else:
        msg = {
            "status": 404,
            "message": "Student cannot be added"
        }
        result = Response(json.dumps(msg), status=404, content_type="application/json")
        return result

@app.route("/api/students", methods=['GET'])
def get_students_with_search():
    field_order_by = request.args.get('field', default='UNI', type=str)
    no_of_results = request.args.get('noOfResults', default=5, type=int)
    page_no = request.args.get('pageNo', default=1, type=int)
    search = request.args.get('search', default='', type=str)
    student_results = StudentResource.get_students(field_order_by, no_of_results, page_no, search)
    if student_results is not None:
        result = Response(json.dumps(student_results), status=200, content_type="application/json")
        return result
    else:
        msg = {
            "status": 400,
            "message": "No data in the table"
        }
        result = Response(json.dumps(msg), status=404, content_type="application/json")
        return result

@app.route("/api/students/<uni>", methods=['GET'])
def get_student_by_uni(uni):
    student_result = StudentResource.get_student_by_uni(uni)
    if student_result is not None:
        result = Response(json.dumps(student_result), status=200, content_type="application/json")
        return result
    else:
        msg = {
            "status": 400,
            "message": f"No student with UNI {uni} present"
        }
        result = Response(json.dumps(msg), status=404, content_type="application/json")
        return result

@app.route("/api/students/<uni>", methods=['DELETE'])
def delete_student_by_uni(uni):
    delete_result = StudentResource.delete_student_by_uni(uni)
    if delete_result == 1:
        msg = {
            "message": f"Student with UNI {uni} deleted successfully!"
        }
        result = Response(json.dumps(msg), status=200, content_type="application/json")
        return result
    else:
        msg = {
            "status": 400,
            "message": f"No student with UNI {uni} present!"
        }
        result = Response(json.dumps(msg), status=404, content_type="application/json")
        return result

@app.route("/api/students/<uni>", methods=['PUT'])
def update_student_by_uni(uni):
    request_json = request.json
    update_status = StudentResource.update_student_by_uni(request_json,uni)
    if update_status == 1:
        msg = {
            "message": "Student record updated successfully!"
        }
        result = Response(json.dumps(msg), status=200, content_type="application/json")
        return result
    else:
        msg = {
            "status": 404,
            "message": "Student record cannot be updated!"
        }
        result = Response(json.dumps(msg), status=404, content_type="application/json")
        return result

if __name__ == '__main__':
    app.run()
