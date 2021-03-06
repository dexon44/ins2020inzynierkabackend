from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from ..decorators import *
from ..models import *
from ..schema import UserSchema

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static')


@admin_bp.route('/dashboard/admin', methods=['GET'])
@required_login
@required_admin
def admin(user=None):
    users = User.query.filter(User.superuser.isnot(True)).all()
    user_schema = UserSchema(many=True)
    return jsonify({'user': user_schema.dump(users)}), 200


@admin_bp.route('/dashboard/admin/user/<username>/give_privileges', methods=['GET'])
@required_login
@required_admin
@required_superadmin
def admin_user_give_privileges(user=None, username=None):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(message="No account with provided username - {}".format(username)), 409
    user.role = True
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(message="user with provided credentials already exist", error_message=str(e.orig)), 400
    return jsonify(message='privileges granted'), 200


@admin_bp.route('/dashboard/admin/user/<username>/change_email', methods=['POST'])
@required_login
@required_admin
def admin_user_change_email(user=None, username=None):
    data = request.get_json()
    new_email = data['new_email']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(message="No account with provided username - {}".format(username)), 409
    user.email = new_email
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(message="db error", error_message=str(e.orig)), 400
    return jsonify(message='email for user - {} has been changed'.format(user.username)), 200


@admin_bp.route('/dashboard/admin/user/<username>/delete_account', methods=['GET'])
@required_login
@required_admin
def admin_user_delete_account(user=None, username=None):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(message="No account with provided username - {}".format(username)), 409
    db.session.delete(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(message="db error", error_message=str(e.orig)), 400
    return jsonify(message='user - {} has been deleted'.format(user.username)), 200


@admin_bp.route('/dashboard/admin/user/<username>/ban_user', methods=['GET'])
@required_login
@required_admin
def admin_user_ban_user(user=None, username=None):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(message="No account with provided username - {}".format(username)), 409
    user.is_banned = True
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(message="db error", error_message=str(e.orig)), 400
    return jsonify(message='user - {} is banned now'.format(user.username)), 200


@admin_bp.route('/dashboard/admin/user/<username>/unban_user', methods=['GET'])
@required_login
@required_admin
def admin_user_unban_user(user=None, username=None):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(message="No account with provided username - {}".format(username)), 409
    user.is_banned = False
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(message="db error", error_message=str(e.orig)), 400
    return jsonify(message='user - {} is unbanned now'.format(user.username)), 200
