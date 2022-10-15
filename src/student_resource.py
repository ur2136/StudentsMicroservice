import pymysql


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
        offset = no_of_results * (page_no - 1)
        searchParams = ""
        if search == '':
            sql = "SELECT * FROM students_db.students ORDER BY {orderBy} LIMIT {noOfResults} OFFSET {offset};".format(
                orderBy=field_order_by,
                noOfResults=no_of_results,
                offset=offset)
        else:
            count = 1
            for val in StudentResource.field_list:
                searchParams += f"{val} LIKE '%{search}%'"
                if count < len(StudentResource.field_list):
                    searchParams += " OR "
                count = count + 1

            sql = "SELECT * FROM students_db.students WHERE " + searchParams + " ORDER BY {orderBy} LIMIT {noOfResults} OFFSET {offset};".format(
                orderBy=field_order_by,
                noOfResults=no_of_results,
                offset=offset)

        conn = StudentResource._get_connection()
        cur = conn.cursor()

        try:
            result = cur.execute(sql)
            result = cur.fetchall()
            return result
        except:
            return None

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




