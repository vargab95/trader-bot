#!/usr/bin/python3

import datetime

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash

import storage.user


class LoginApi(Resource):
    user_storage: storage.user.UserStorage = None

    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def post(self):
        request = self.parser.parse_args()

        user = self.user_storage.get(request["email"])

        if not user:
            return {"message": "User does not exists"}, 401

        if not user["active"]:
            return {"message": "User is not active"}, 403

        if not check_password_hash(user["password"], request["password"]):
            return {"message": "Invalid credential"}, 403

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user['_id']),
                                           expires_delta=expires)

        return {'token': access_token}, 200
