#!/usr/bin/python3

from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash

import storage.user


class SignupApi(Resource):
    user_storage: storage.user.UserStorage

    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def post(self):
        request = self.parser.parse_args()
        try:
            self.user_storage.add(request["email"],
                                  generate_password_hash(request["password"]))
            return {}, 200
        except storage.user.InvalidUserRequest:
            return {"message": "E-mail already exists"}, 409
