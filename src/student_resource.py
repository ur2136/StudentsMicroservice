import pymysql

def pagination_wrapper(result, num_results, page_no):
    # Hack to get the total number of records as well - required by UI
    if not result:
        return [], 0
    if num_results is None:
        return result, len(result)
    offset = num_results * (page_no - 1)
    limit = offset + num_results + 1
    return result[offset:limit], len(result)

class StudentResource:
    last_name = ""
    first_name = ""
    middle_name = ""
    email = ""
    school_code = ""

    field_list = ["UNI","last_name", "first_name", "middle_name", "email", "school_code"]

    def __int__(self, first_name, middle_name, last_name, email, school_code):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.school_code = school_code

    @staticmethod
    def _get_connection():
        conn = pymysql.connect(
            user="root",
            password="dbuserdbuser",
            host="sprint1db.cujzitb9jpux.us-east-1.rds.amazonaws.com",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def insert_student(student_dict):
        sql = "INSERT INTO students_db.students ({columns}) VALUES ({values});".format(
            columns=",".join(student_dict.keys()),
            values=", ".join(["%s"] * len(student_dict)));
        conn = StudentResource._get_connection()
        cur = conn.cursor()

        try:
            cur.execute(sql, list(student_dict.values()))
            return 1
        except:
            return 0

    @staticmethod
    def get_students(field_order_by, no_of_results, page_no, search):
        searchParams = ""
        if search == '':
            sql = "SELECT * FROM students_db.students ORDER BY {orderBy};".format(
                orderBy=field_order_by)
        else:
            count = 1
            for val in StudentResource.field_list:
                searchParams += f"{val} LIKE '%{search}%'"
                if count < len(StudentResource.field_list):
                    searchParams += " OR "
                count = count + 1

            sql = "SELECT * FROM students_db.students WHERE " + searchParams + " ORDER BY {orderBy};".format(
                orderBy=field_order_by)

        conn = StudentResource._get_connection()
        cur = conn.cursor()

        try:
            result = cur.execute(sql)
            result = cur.fetchall()
            return pagination_wrapper(result, no_of_results, page_no)
        except:
            return None, 0

    @staticmethod
    def get_student_by_uni(uni):
        sql = "SELECT * FROM students_db.students WHERE UNI = %s;"
        conn = StudentResource._get_connection()
        cur = conn.cursor()

        result = cur.execute(sql,uni)
        result = cur.fetchone()
        return result

    @staticmethod
    def delete_student_by_uni(uni):
        sql = "DELETE FROM students_db.students WHERE UNI = %s;"
        conn = StudentResource._get_connection()
        cur = conn.cursor()

        try:
            result = cur.execute(sql, uni)
            return 1
        except:
            return 0

    @staticmethod
    def update_student_by_uni(student_dict, uni):
        sql = "UPDATE students_db.students SET "

        updateParams = ""
        count = 1
        args = []
        for key, value in student_dict.items():
            updateParams += f"{key}=%s"
            args.append(value)
            if count < len(student_dict):
                updateParams += ", "
            count = count + 1

        whereParam = " WHERE UNI=%s"
        sql = sql + updateParams + whereParam
        args.append(uni)

        conn = StudentResource._get_connection()
        cur = conn.cursor()

        try:
            result = cur.execute(sql, args)
            if result <= 1:
                return 1
            else:
                return 0
        except:
            return 0




