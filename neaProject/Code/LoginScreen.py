# import the libraries
from appJar import gui
import sqlite3

# connect to the database
connection = sqlite3.connect("Logins.db")
browser = connection.cursor()

# create a table to store the logins, if it does not already exist on the system.
browser.execute(
    "CREATE TABLE IF NOT EXISTS Login (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name VARCHAR(30), Password VARCHAR(30), "
    "Highscore INTEGER)")


# function to log in when the user presses the button
def buttonPress(option):
    name = window.getEntry("Name")
    password = window.getEntry("Password")
    # input validation: Make sure the name, password are both under 30 characters and contain no special characters
    if len(name) < 30 and len(password) < 30 and name.isalnum() and password.isalnum():
        # If the user has decided to log in
        if option == "Enter":
            query = "SELECT Password FROM Login WHERE Name = \"%s\"" % name
            result = browser.execute(query).fetchall()
            # check if the selected password matches what the user has entered
            try:
                if result[0][0] == password:
                    # The password is correct
                    import MainGame
                else:
                    # Alert the user that the password was incorrect
                    window.retryBox("warning", "Password is not correct")
            except:
                # No users found
                window.retryBox("warning", "User not found, try signing up!")

        # If the user decided to sign up
        elif option == "Sign-up":
            query = "SELECT COUNT(*) FROM Login WHERE Name = \"%s\"" % name
            result = browser.execute(query).fetchall()
            print(result[0][0])
            if result[0][0] == 0:
                # The username has not been taken, so register the player.
                query = "INSERT INTO Login VALUES (%s, \"%s\", \"%s\", 0)" % (result[0][0] + 1, name, password)
                browser.execute(query)
                connection.commit()
            else:
                # The username has been taken
                window.retryBox("warning", "This username has been taken")

    else:
        # Alert the user that their input was rejected
        window.retryBox("warning", "Both inputs must be less than 30 characters in length and have no special "
                                   "characters (and cannot be blank obviously")


# Create windowJar widgets
window = gui("Gojani's Quiz", "576 x 800")
window.addLabel("title", "Gojani's quiz")
window.setBg("gray")
window.setPadding([20, 20])
window.setInPadding([40, 40])
window.addEntry("Name")
window.addEntry("Password")
window.addButtons(["Enter", "Sign-up"], buttonPress)
window.setFont(size=40, family="verdana")
window.setLabelBg("title", "grey")

# start the program
window.go()

# Close database connection once the login phase has been completed.
connection.close()
