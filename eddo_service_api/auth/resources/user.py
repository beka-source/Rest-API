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

# class TaskResource(Resource):
#     @jwt_required
#     def put(self):
#         user_id =  get_jwt_identity()
#         schema = PositioinSchema(partial=True)
#         position = TblPosition.query.get(request.args.get('task_id',None))
#         user = TblUsers.query.get_or_404(user_id)
#         for i in position.role_id:
#             if i
#         role = schema.load(request.json, instance=role)
#         db.session.commit()


class TaskResource(Resource):
    @jwt_required
    # @roles_required('admin')
    def get(self):
        query = TblPosition.query
        resul = []
        # user_id = '21af59a0-5159-4b84-80e7-fb5ceb0cea6b'
        user_id = get_jwt_identity()
        user = TblUsers.query.get_or_404(user_id)
        tasks = TblTasks.query
        for i in tasks:
            query_ = query.filter(TblPosition.task_id == i.id)
            if query_.count() != 0:
                print(query)
                users = []
                for j in query_:
                    users.append({
                        'user_id': str(j.user_id),
                        'username': j.user.username,
                        'full_name': j.user.full_name,
                        'role_id': str(j.role_id),
                        'role_title': j.role_title.title,
                    })
                resul.append({'task_id': str(i.id), 'task_status': i.task_status, 'task_text': i.task_text, 'create_time': str(i.create_time), 'update_time': str(i.update_time), 'deadline': str(i.deadline), 'users': users})
        print(resul)

        return {'result': resul}

        # return paginate(query, schema)

    def post(self):
        schema = TaskSchema()
        query_all = dict(request.json)
        a = query_all.pop('users')

        task = schema.load(query_all)
        db.session.add(task)
        db.session.commit()
        task = schema.dump(task)

        task_id = task['id']
        for i in a:
            i['task_id'] = task_id
        ty = PositioinSchema()
        for i in a:
            db.session.add(ty.load(i))
            db.session.commit()
        task['users'] = a
        return {"msg": "Task created", "Task": task}, 201

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


class ChangeTXResource(Resource):
    @jwt_required
    def put(self):
        user_id = get_jwt_identity()
        schema = TaskSchema(partial=True)
        id = request.json.get('task_id')
        task_text = request.json.get('task_text')

        task = TblTasks.query.get_or_404(id)
        task.task_text = task_text
        db.session.add(task)
        db.session.commit()

        return {"msg": "Text updated", "Text": schema.dump(task)}


class ChangeSTResource(Resource):
    @jwt_required
    def put(self):
        user_id = get_jwt_identity()
        schema = TaskSchema(partial=True)
        id = request.json.get('task_id')
        task_status = request.json.get('task_status')

        task = TblTasks.query.get_or_404(id)
        task.task_status = task_status
        db.session.add(task)
        db.session.commit()

        return {"msg": "Status updated", "Status": schema.dump(task)}


class PositionResource(Resource):
    @jwt_required
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
