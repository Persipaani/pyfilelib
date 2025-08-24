# Book Dictionary App
A simple python application that uses a text file as a database and allows users viewing books stored in the file and adding new books to it.

# Requirements
1. Python (3.12 or later)
2. Install by running `pip install -r requirements` in the project root.

# Running
Run by using the provided launcher and passing the database file path. If the file does not exist, it will be created. There is an example `data.txt` file in the project root that you can try out.

F.ex. `python launcher.py my_database.txt`

After running the command you should see Reflex initialization and then a url pointing to the application GUI front-end (http://localhost:3000/).

If the port is in use by another application in your system, please change the port to the `rxconfig.py` file in the root (f.ex. frontend_port=3001).

To exit the app, close the browser window and CTRL + C to the server terminal.