from dataclasses import asdict
from flask import Blueprint, jsonify, request
from model.Question import Question
from repository.question_repository import (
    create_question,
    get_all_questions,
    find_question_by_id,
    update_question,
    delete_question
)

question_blueprint = Blueprint("questions", __name__)

@question_blueprint.route("/questions", methods=['GET'])
def get_all_questions_route():
    questions = list(map(asdict, get_all_questions()))
    return jsonify(questions), 200

@question_blueprint.route("/questions/<int:question_id>", methods=['GET'])
def get_question_by_id(question_id):
    question = find_question_by_id(question_id)
    if question:
        return jsonify(asdict(question)), 200
    return jsonify({"error": "Question not found"}), 404

@question_blueprint.route("/questions", methods=['POST'])
def create_question_route():
    question_data = request.json
    new_question = Question(**question_data)
    try:
        question_id = create_question(new_question)
        return jsonify({"id": question_id, "message": "Question created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@question_blueprint.route("/questions/<int:question_id>", methods=['PUT'])
def update_question_route(question_id):
    question_data = request.json
    updated_question = Question(**question_data)
    if update_question(question_id, updated_question):
        return jsonify({"message": "Question updated successfully"}), 200
    return jsonify({"error": "Question not found"}), 404

@question_blueprint.route("/questions/<int:question_id>", methods=['DELETE'])
def delete_question_route(question_id):
    if delete_question(question_id):
        return jsonify({"message": "Question deleted successfully"}), 200
    return jsonify({"error": "Question not found"}), 404
