from flask import Blueprint, current_app, request, redirect, url_for

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/habit/<habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    user_id = request.cookies.get('user_id')
    current_app.habit_service.delete_habit(habit_id, user_id)

    return redirect(url_for('router.enroll_page'))


@api_bp.route('/habit', methods=['POST'])
def post_habit():
    content = request.json.get('content')
    user_id = request.cookies.get('user_id')

    current_app.habit_service.add(content, user_id)

    return redirect(url_for('router.enroll_page'))


@api_bp.route('/habit/toggle', methods=['POST'])
def toggle():
    log_id = request.json.get('_id')
    user_id = request.cookies.get('user_id')

    current_app.habit_log_service.set_check(log_id, user_id)

    return redirect(url_for('router.enroll_page'))
