#!/usr/bin/python3

import pymongo.errors


class InvalidUserRequest(Exception):
    pass


class UserStorage:
    def __init__(self, db):
        self.__collection = db.users

    def add(self, email: str, password_hash: str):
        try:
            self.__collection.insert_one({
                "email": email,
                "password": password_hash,
                "active": False
            })
        except pymongo.errors.DuplicateKeyError:
            raise InvalidUserRequest("User already exists")

    def get(self, email=None):
        return self.__collection.find_one({"email": {"$eq": email}})
