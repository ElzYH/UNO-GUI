import sqlite3
def create():
    conn = sqlite3.connect("uno_database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE Leaderboard (
        UserName VARCHAR(10),
        Games INT,
        Wins INT,
        Loss INT,
        Draws INT,
        Win_ratio FLOAT(128,2),
        PRIMARY KEY('UserName'))""")
    conn.commit()
    conn.close()


class User:
    def __init__(self,u=""):
        self.__username = u
        self.error = ""
    
    
    def set_username(self,u):
        conn = sqlite3.connect("uno_database.db")
        c = conn.cursor()
        self.__username = u.replace(" ", "_") 

        try:
            copy_check = c.execute(f'SELECT UserName FROM Leaderboard WHERE UserName IS "{self.__username}"')
            copy_check = str("".join(c.fetchone()))
        except TypeError: None

        if copy_check == self.__username: 
            self.error = "Please Create A UserName That Not In The Database"
        elif self.__username == "": 
            self.error = "Please Do Not Leave The Username Blank"
        else: 
            c.execute(f"INSERT INTO Leaderboard(UserName,Games,Wins,Loss,Draws,Win_ratio) VALUES ('{self.__username.lower()}',0,0,0,0,0)")
        
        self.__username = ""
        conn.commit()
        conn.close()
 

    def sign_in(self,u):
        conn = sqlite3.connect("uno_database.db")
        c = conn.cursor()

        self.__username = str("".join([i for i in u])).lower()
        check = c.execute(f'SELECT UserName FROM Leaderboard WHERE UserName IS "{self.__username}"')

        try:
            check = str("".join(c.fetchone())).lower()
        except TypeError:
            self.__username = ""
            self.error = "Please Enter A Valid Username"
            conn.close()
        
        if check == self.__username: 
            return self.__username

    def get_user(self): 
        return self.__username

    def error_code(self):
        display = self.error 
        self.error = ""
        return display


def login_or_sign(login_options,name):
    account_name = User()
    if login_options == "sign up":
            account_name.set_username(name)

    elif login_options == "sign in":
        account_name.sign_in(name)

    list2 = [account_name.get_user(), account_name.error_code()]
    return list2

    
    
