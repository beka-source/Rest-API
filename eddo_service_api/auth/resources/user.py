from flask import request, jsonify
from flask_restful import Resource
from eddo_service_api.auth.schemas import UserSchema, RoleSchema, TaskSchema, PositioinSchema
from eddo_service_api.models import TblUsers, TblRole, TblTasks, TblPosition
from eddo_service_api.extensions import db
from eddo_service_api.commons.pagination import paginate
from eddo_service_api.auth.resources.userres import roles_required
from flask_jwt_extended import get_jwt_identity, jwt_required


class UserResource(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        schema1 = UserSchema()
        user = TblUsers.query.get_or_404(user_id)
        if user_id:
            schema = UserSchema(many=True)
            user = TblUsers.query.get_or_404(user_id)
            user_json = schema1.dump(user)
            query = TblUsers.query.filter(TblUsers.id != user_id)
            return {'Me': user_json, 'users': paginate(query, schema)}

        user_json = schema1.dump(user)
        return {'User': user_json}

        # user_id = get_jwt_identity()
        # schema1 = UserSchema()
        # user = TblUsers.query.get_or_404(user_id)
        # if user.role_id:
        #     role = TblRole.query.get(user.role_id)
        #     if role.title == 'admin':
        #         schema = UserSchema(many=True)
        #         user_json = schema1.dump(user)
        #         query = TblUsers.query.filter(TblUsers.id != user_id)
        #         return {'me': user_json, "users": paginate(query, schema)}
        # user_json = schema1.dump(user)
        # return {'User': user_json}


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
        task_id = request.args.get('task_id')

        if task_id:
            schema = TaskSchema()
            task = TblTasks.query.get_or_404(task_id)
            task_json = schema.dump(task)

            return task_json

        schema = TaskSchema(many=True)
        query = TblTasks.query

        return paginate(query, schema)

    # @jwt_required
    # @roles_required('admin')
    # @app.route('/todo/api/v1.0/tasks', methods=['POST'])
    # def create_task():
    #     if not request.json or not 'title' in request.json:
    #         abort(400)
    #     task = {
    #         'id': tasks[-1]['id'] + 1,
    #         'title': request.json['title'],
    #         'description': request.json.get('description', ""),
    #         'done': False
    #     }
    #     tasks.append(task)
    #     return jsonify({'task': task}), 201
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


class PositionResource(Resource):

    def get(self):
        query = TblPosition.query
        resul = []
        tasks = TblTasks.query
        for i in tasks:
            query_ = query.filter(TblPosition.task_id == i.id)
            print(query)
            users = []
            for j in query_:
                users.append({
                    'user_id': str(j.user.id),
                    'username': j.user.username,
                    'full_name': j.user.full_name,
                    'role_id': str(j.role_id),
                    'role_title': j.role_title.title
                })
            resul.append({'task_status': i.task_status, 'task_text': i.task_text, 'users': users})
        print(resul)

        return {'result': resul}

    def post(self):
        schema = PositioinSchema()
        position = schema.load(request.json)
        db.session.add(position)
        db.session.commit()
        return {"msg": "Position created", "Position": schema.dump(position)}, 201
