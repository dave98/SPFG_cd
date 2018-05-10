from django.db import connection


class DB:
    def __init__(self):
        self.db = 'mycash'

    @staticmethod
    def income_amount(idu, day):
        with connection.cursor() as cursor:
            cursor.execute("select * from income_day(%s,%s)", [idu, day])
            return cursor.fetchall()

    @staticmethod
    def expense_amount(idu, day):
        with connection.cursor() as cursor:
            cursor.execute("select * from expense_day(%s,%s)", [idu, day])
            return cursor.fetchall()

    @staticmethod
    def validate_user(email, password):
        with connection.cursor() as cursor:
            cursor.execute("select * from validate(%s,%s)", [email, password])
            return int(cursor.fetchone()[0])