from flask import request
from flask_restful import Resource
from eddo_service_api.auth.schemas import UserSchema, RoleSchema, TaskSchema
from eddo_service_api.models import TblUsers, TblRole, TblTasks
from eddo_service_api.extensions import db
from eddo_service_api.commons.pagination import paginate
from eddo_service_api.auth.resources.userres import roles_required
from flask_jwt_extended import get_jwt_identity, jwt_required


class UserResource(Resource):
    # @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        schema1 = UserSchema()
        user = TblUsers.query.get_or_404(user_id)
        if user.role_id:
            role = TblRole.query.get(user.role_id)
            if role.title == 'admin':
                schema = UserSchema(many=True)
                user_json = schema1.dump(user)
                query = TblUsers.query.filter(TblUsers.id != user_id)
                return {'me': user_json, "users": paginate(query, schema)}
        user_json = schema1.dump(user)
        return {'User': user_json}

    @jwt_required
    @roles_required('admin')
    def put(self):
        schema = UserSchema(partial=True)
        user = TblUsers.query.get_or_404(request.args.get('user_id'))
        user = schema.load(request.json, instance=user)
        db.session.commit()

        return {"msg": "User updated", "User": schema.dump(user)}

    @jwt_required
    @roles_required('admin')
    def delete(self):
        user = TblUsers.query.get_or_404(request.args.get('user_id'))
        db.session.delete(user)
        db.session.commit()

        return {"msg": "User deleted"}


class RoleResource(Resource):
    def get(self):
        role_id = request.args.get('role_id')

        if role_id:
            schema = RoleSchema()
            role = TblRole.query.get_or_404(role_id)
            role_json = schema.dump(role)

            return {'Role': role_json}

        schema = RoleSchema(many=True)
        query = TblRole.query

        return paginate(query, schema)

    def post(self):
        schema = RoleSchema()
        role = schema.load(request.json)
        db.session.add(role)
        db.session.commit()

        return {"msg": "Role created", "Role": schema.dump(role)}, 201

    def put(self):
        schema = RoleSchema(partial=True)
        role = TblRole.query.get_or_404(request.args.get('role_id'))
        role = schema.load(request.json, instance=role)
        db.session.commit()

        return {"msg": "Role updated", "Role": schema.dump(role)}

    @jwt_required
    @roles_required('admin')
    def delete(self):
        role = TblRole.query.get_or_404(request.args.get('role_id'))
        db.session.delete(role)
        db.session.commit()

        return {"msg": "Role deleted"}


class TaskResource(Resource):
    # @jwt_required
    # @roles_required('admin')
    def get(self):
        print(3)
        schema1 = TaskSchema()
        print(1)
        task_id = request.args.get('task_id')
        print(2)
        task = TblTasks.query.get_or_404(task_id)
        print(4)
        if task_id:
            print(5)
            task = TblTasks.query.get(task.task_id)
            print(6)
            if task.task_status == 'New status':
                print(7)
                schema = TaskSchema()
                print(8)
                task_json = schema1.dump(task)
                query = TblTasks.query.filter(TblTasks.task_id != task_id)
                return {'New Task': task_json, 'tasks': paginate(query, schema)}
        task_json = schema1.dump(task)
        return {'Task': task_json}

    # @jwt_required
    # @roles_required('admin')
    def post(self):
        schema = TaskSchema()
        task = schema.load(request.json)
        db.session.add(task)
        db.session.commit()

        return {"msg": "Task created", "Task": schema.dump(task)}, 201

    # @jwt_required
    # @roles_required('admin')
    def put(self):
        schema = TaskSchema(partial=True)
        task = TblTasks.query.get_or_404(request.args.get('task_id'))
        task = schema.load(request.json, instance=task)
        db.session.commit()

        return {"msg": "Task updated", "Task": schema.dump(task)}

    # @jwt_required
    # @roles_required('admin')
    def delete(self):
        task = TblTasks.query.get_or_404(request.args.get('task_id'))
        db.session.delete(task)
        db.session.commit()

        return {"msg": "Task deleted"}
