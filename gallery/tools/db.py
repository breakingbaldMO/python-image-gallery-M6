import psycopg2
import json
from secrets import get_secret_image_gallery


connection = None


def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)


def get_password(secret):
    return secret['password']


def get_host(secret):
    return secret['host']


def get_username(secret):
    return secret['username']


def get_dbname(secret):
    return secret['database_name']


def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    connection.set_session(autocommit=True)


def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor


def add_user(username, password, full_name):
    cursor = connection.cursor()
    try:
        execute("""
        INSERT into users (username, password, full_name) VALUES (%s, %s, %s);
        """, (username, password, full_name))


    except Exception as error:
        print("Error: a user with username '" + username + "' already exists\n")


def edit_user(user_to_edit, password, full_name):
    try:
        if password:
                execute("UPDATE users SET password='" + password + "' WHERE username='" + user_to_edit + "';")


    except Exception as error:
                print("Error updating password\n")
    try:
        if full_name:
                execute("UPDATE users SET full_name='" + full_name + "' WHERE username='" + user_to_edit + "';")


    except Exception as error:
                print("Error updating full name\n")


def delete_user(user_to_delete):
    try:
        execute("DELETE FROM users WHERE username='" + user_to_delete + "';")

    except Exception as error:
            print("Error deleting username\n")


def select_all(table):
    res = execute('select * from ' + table).fetchall()
    return res


def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)

if __name__ == '__main__':
    main()