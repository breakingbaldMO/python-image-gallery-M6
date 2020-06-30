import db
import psycopg2

def menu():
  try:
    choice = input("1) List users\n2) Add user\n3) Edit user\n4) Delete user\n5) Quit\nEnter Command> ")
    choice = int(choice)
    if choice == 1:
        print("\nList Users\n")
        res = db.select_all("users")
        print("username                  password                  full name\n---------------------------------------------------------------------")
        for row in res:
           print("{: <25} {: <25} {: <25}".format(*row))
        print("\n")
        menu()

    elif choice == 2:
        print("\nAdd User\n")
        username = input("Username>")
        password = input("Password>")
        full_name = input("Full name>")
        print("\n")
        if not username:
            print("Failed to add user: username must be specified\n")
            menu()
        else:
            db.add_user(username, password, full_name)
            menu()

    elif choice == 3:
        print("\nEdit User\n")
        user_to_edit = input("\nUsername to edit>")
        cursor = db.connection.cursor()
        cursor.execute("select * from users where username='" + user_to_edit + "';")
        res = cursor.fetchall()
        if not res:
            print("\nNo such user exists\n")
            print("\n")
            menu()
        else:
            password = input("New password (press enter to keep current)>")
            full_name = input("New full name (press enter to keep current)>")
            print("\n")
            db.edit_user(user_to_edit, password, full_name)
            menu()

    elif choice == 4:
        print("\nDelete User\n")
        user_to_delete = input("\nEnter username to delete>")
        cursor = db.connection.cursor()
        cursor.execute("select * from users where username='" + user_to_delete + "';")
        res = cursor.fetchall()
        if not res:
            print("\nNo such user exists\n")
            menu()
        else:
            answer = input("\nAre you sure that you want to delete " + user_to_delete + "? ")
            if answer is "Yes" or "Y":
                db.delete_user(user_to_delete)
                menu()

    elif choice == 5:
        print("\nGoodbye!\n")

    else:
        print("\n")
        menu()

  except Exception as error:
      print("\n")
      menu()

def main():
    db.connect()
    menu()

    # res = execute('select * from users')
    # for row in res:
    #    print(row)
    # res = execute("update users set password=%s where username='fred'", ('banana',))
    # res = execute('select * from users')
    # for row in res:
    #    print(row)


if __name__ == '__main__':
    main()
