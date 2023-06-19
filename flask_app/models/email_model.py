from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Email:
    DB = 'email_validation'
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO email_validation (email)
        VALUES (%(email)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):           #get all does not need data as parameter
        query = """
        SELECT * FROM email_validation;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        emails = []
        for row in results:
            emails.append(cls(row))
        return emails
    
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM email_validation
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash("Email is not valid!")
            is_valid = False
        return is_valid
    
    @staticmethod
    def is_valid(email):
        is_valid = True
        query = """
        SELECT * FROM email_validation
        WHERE email = %(email)s;
        """
        results = connectToMySQL(Email.DB).query_db(query, email)   #cannot use cls becuase this is a static method, but you can just target the class itself
        if len(results) >= 1:
            flash("Email is already taken.")
            is_valid = False
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email!")
            is_valid = False
        return is_valid