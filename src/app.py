from flask import Flask, Response, request, send_from_directory
from datetime import datetime
import json
from flask_cors import CORS
from student_resource import StudentResource
from flask_swagger_ui import get_swaggerui_blueprint
from middleware.sns_notifications import Notifications

sns_middleware = Notifications()

app = Flask(__name__)
CORS(app)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Students Microservice"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.before_request
def before_request_func():
    print('before_request executing!')
    print("request = ",json.dumps(request, indent=2, default=str))
@app.route("/api/summary")
def site_map():
    links = []
    ignore_methods = {'HEAD', 'OPTIONS'}
    for rule in app.url_map.iter_rules():
        links.append(f"{rule.rule} {rule.methods - ignore_methods} -> {rule.endpoint}")
    return Response(json.dumps(sorted(links)), status=200, content_type="application/json")

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
    student_results, total_records = StudentResource.get_students(field_order_by, no_of_results, page_no, search)
    if student_results is not None:
        result = Response(json.dumps({
            "result": student_results,
            "_total_records": total_records
        }), status=200, content_type="application/json")
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

@app.after_request
def after_request_func(response):
    print('after_request executing!')
    print("response = ",json.dumps(response, indent=2, default=str))
    sns_middleware.check_publish(request, response)
    return response

if __name__ == '__main__':
    app.run()
