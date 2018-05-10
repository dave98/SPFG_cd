from django.db import connection

"""
    Class that accesses the Database through ORM queries, 
    We create queries by calling the functions of the database 
    that were performed.
"""

class DB:
    def __init__(self):
        self.db = 'mycash'

    # The sum of the income per day in the last days
    @staticmethod
    def income_amount(idu, day):
        with connection.cursor() as cursor:
            cursor.execute("select * from income_day(%s,%s)", [idu, day])
            return cursor.fetchall()

    # The sum of the expense per day in the last days
    @staticmethod
    def expense_amount(idu, day):
        with connection.cursor() as cursor:
            cursor.execute("select * from expense_day(%s,%s)", [idu, day])
            return cursor.fetchall()

    # Verify the login, checking the existence of the user
    # returns 0 if it does not exist, and if it exists returns
    # the user's id.
    @staticmethod
    def validate_user(email, password):
        with connection.cursor() as cursor:
            cursor.execute("select * from validate(%s,%s)", [email, password])
            return int(cursor.fetchone()[0])