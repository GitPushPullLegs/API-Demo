"""A demo API that executes SQL queries dynamically.

Generates different sql queries based on the users requirements.

Checklist:
• Group by student_id and count completed assignments ✓
• Group by course_id and average grade ✓
• Group by teacher_id and count assignments created ✓
• Group by school_id and find percentage of students with more than 1 assignment completed ✓
"""

from flask import Flask, g, request

import sqlite3
from .querybuilder import QueryBuilder
import json
import os

app = Flask(__name__)

DATABASE = os.path.split(__file__)[0] + '/sqlite-5.db'


def get_df():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=()):
    cur = get_df().execute(query, args)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = {'data': []}
    for result in rv:
        json_data['data'].append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


@app.route('/')
def index():
    return "Schoolytics API Demo"


@app.route('/students')
@app.route('/students/<int:student_id>')
def get_students(student_id=None):
    """Returns the base data of each student

    Args:
        student_id: A student's ID number if you want to return just this student.

    URL Params:
        school_id: If you want to filter by just one school.
        grade_level: If you want to filter for just one grade level.
        enrolled_in: The ID number of a specific course you'd like to filter by.
        submitted_assignments: Bool. Returns the count of submitted assignments.
        limit: To limit the amount of results.

    Returns:
        JSON data for each student.

        {'data': [
            {'student_id': 123456,
             'school_id': 11,
             'grade_level: 'KN'}
        ]}
    """
    query = QueryBuilder()
    query.distinct()
    query.select(["S.student_id", "S.grade_level", "S.school_id"])
    query.from_table("student S")
    if request.args.get('school_id'):
        query.where("S.school_id = ?")
        query.args.append(request.args.get('school_id'))
    if request.args.get('grade_level'):
        query.where("S.grade_level = ?")
        query.args.append(request.args.get('grade_level'))
    if request.args.get('limit'):
        query.limit(request.args.get('limit'))
    if request.args.get('enrolled_in'):
        query.inner_join("roster R ON R.student_id = S.student_id")
        query.where("R.course_id = ?")
        query.args.append(request.args.get('enrolled_in'))
    if request.args.get('submitted_assignments') == "True":
        query.select(['IFNULL(SUM(SSUM.status_code), 0) [submitted_assignments]'])
        query.left_join('student_submission SSUM ON SSUM.student_id = S.student_id')
        query.add_group_by(['S.student_id', 'S.grade_level', 'S.school_id'])
    if student_id:
        query.where("S.student_id = ?")
        query.args.append(student_id)

    return query_db(query.query, query.args)


@app.route('/courses')
@app.route('/courses/<int:course_id>')
def get_courses(course_id=None):
    """Returns JSON data for a course.

        Args:
            course_id: The ID number of a course, if you'd like to specify.

        URL Params:
            teacher_id: If you want to filter to courses by just one teacher.
            name: If you want to filter for a specific course name.
            average_grade: Returns the average grade in each course.
            limit: To limit the amount of results.

        Returns:
            JSON data for each course.

            {'data': [
                {'course_id': 123456,
                 'teacher_id': 11,
                 'name: 'Jane Doe'}
            ]}
        """
    query = QueryBuilder()
    query.select(['C.course_id', 'C.teacher_id', 'C.name'])
    query.from_table('course C')

    if request.args.get('teacher_id'):
        query.where("C.teacher_id = ?")
        query.args.append(request.args.get('teacher_id'))
    if request.args.get('name'):
        query.where("C.name = ?")
        query.args.append(request.args.get('name'))
    if request.args.get('average_grade') == "True":
        query.select(['ROUND(((SUM(sSUM.assigned_points) / SUM(sSUM.max_points)) * 100), 2) average_grade'])
        query.inner_join("course_work CW ON CW.course_id = C.course_id")
        query.inner_join("student_submission sSUM ON sSum.course_work_id = CW.course_work_id")
        query.add_group_by(["C.course_id", "C.teacher_id", "C.name"])

    if request.args.get('limit'):
        query.limit(request.args.get('limit'))

    if course_id:
        query.where("C.course_id = ?")
        query.args.append(course_id)

    return query_db(query.query, query.args)


@app.route('/teachers')
@app.route('/teachers/<int:teacher_id>')
def get_teachers(teacher_id=None):
    """Returns JSON data for a teacher.

            Args:
                teacher_id: The ID number of a teacher, if you'd like to specify.

            URL Params:
                assignments_created: Bool. Returns the count of assignments created.
                limit: To limit the amount of results.

            Returns:
                JSON data for each teacher.

                {'data': [
                    {'course_id': 123456,
                     'teacher_id': 11,
                     'name: 'Jane Doe'}
                ]}
            """
    query = QueryBuilder()
    query.select(['T.teacher_id', 'T.current_school_id', 'T.active'])
    query.from_table('teacher T')

    if request.args.get('assignments_created') == "True":
        query.select(['COUNT(DISTINCT CW.course_work_id) [assignments_created]'])
        query.inner_join('course C on C.teacher_id = T.teacher_id')
        query.left_join('course_work CW ON CW.course_id = C.course_id')
        query.add_group_by(['T.teacher_id', 'T.current_school_id', 'T.active'])
    if request.args.get('limit'):
        query.limit(request.args.get('limit'))

    if teacher_id:
        query.where('T.teacher_id = ?')
        query.args.append(teacher_id)

    return query_db(query.query, query.args)


@app.route('/schools')
@app.route('/schools/<int:school_id>')
def get_schools(school_id=None):
    """Returns JSON data for a school.

            Args:
                school_id: The ID number of a school, if you'd like to specify.

            URL Params:
                student_engagement_percentage: Bool. Returns the percentage of students who have completed at least one assignment.
                limit: To limit the amount of results.

            Returns:
                JSON data for each school.

                {'data': [
                    {'school_id': 123456,
                     'school_name': 'Gregori'}
                ]}
            """
    query = QueryBuilder()
    query.select(['SCH.school_id', 'SCH.school_name'])
    query.from_table('school SCH')

    if school_id:
        query.where('SCH.school_id = ?')
        query.args.append(school_id)

    if request.args.get('student_engagement_percentage') == "True":
        query.select('ROUND(CAST(COUNT(DISTINCT CASE WHEN SSUM.status_code = 1 THEN SSUM.student_id END) AS FLOAT) / COUNT(DISTINCT S.student_id), 2) [percent_student_engagement]')
        query.inner_join("teacher T ON T.current_school_id = SCH.school_id")
        query.inner_join('course C ON T.teacher_id = C.teacher_id')
        query.left_join("student_submission SSUM ON SSUM.course_id = C.course_id")
        query.inner_join("student S ON S.school_id = SCH.school_id")
        query.add_group_by(['SCH.school_id', 'SCH.school_name'])
    if request.args.get('limit'):
        query.limit(request.args.get('limit'))

    return query_db(query.query, query.args)
