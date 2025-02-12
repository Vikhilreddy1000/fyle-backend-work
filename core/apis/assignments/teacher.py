from flask import Blueprint
from core.apis import decorators
from core import db
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from marshmallow.exceptions import ValidationError
from flask import jsonify

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(teacher_id=p.user_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment_teacher(p, incoming_payload):
    try:
        grade_payload = AssignmentGradeSchema().load(incoming_payload)
    except ValidationError as e:
        return jsonify({"error": "ValidationError", "message": str(e)}), 400

    assignment_id = grade_payload.id
    grade = grade_payload.grade

    assignment = Assignment.get_by_id(assignment_id)
    if not assignment:
        return jsonify({"error": "FyleError", "message": "Assignment not found"}), 404

    if assignment.teacher_id != p.teacher_id:
        return jsonify({"error": "FyleError", "message": "This assignment belongs to another teacher"}), 400

    if assignment.state != AssignmentStateEnum.SUBMITTED.value:
        return jsonify({"error": "FyleError", "message": "Only submitted assignments can be graded"}), 400

    if grade not in {g.value for g in GradeEnum}:
        return jsonify({"error": "ValidationError", "message": "Invalid grade"}), 400

    assignment.grade = grade
    assignment.state = AssignmentStateEnum.GRADED.value
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)