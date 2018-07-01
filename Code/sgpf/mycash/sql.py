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
    def income_month(idu, month):
        with connection.cursor() as cursor:
            cursor.execute("select * from income_month(%s,%s)", [idu, month])
            return cursor.fetchall()

    # The sum of the expense per day in the last days
    @staticmethod
    def expense_day(idu, day):
        with connection.cursor() as cursor:
            cursor.execute("select * from expense_day(%s,%s)", [idu, day])
            return cursor.fetchall()

    @staticmethod
    def delete_account(id_us):
        with connection.cursor() as cursor:
            cursor.execute("select * from delete_account(%s)", [id_us])

    @staticmethod
    def savings_per_user(id_us):
        with connection.cursor() as cursor:
            cursor.execute("select * from savings_per_user(%s)", [id_us])
            return cursor.fetchall()[0][0]