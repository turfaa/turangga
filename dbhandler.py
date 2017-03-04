import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from myconfig import host, user, password, database
from util import randomString

class DBException(BaseException):
    def __init__(self, message):
        self.message = message

class DBHandler:
    def __init__(self, host = host, user = user, password = password, database = database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def __del__(self):
        try:
            self.disconnect()
        except:
            pass

    def connect(self):
        self.conn = MySQLdb.connect(self.host, self.user, self.password, self.database)
        self.c = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.c.close()
        self.conn.close()

    def userExist(self, username):
        self.c.execute('select 1 from user where username = %s', (username, ))
        return self.c.rowcount > 0

    def userCreate(self, username, password):
        if self.userExist(username):
            raise DBException('Username exist')

        self.c.execute('insert into user (username, password) value (%s, %s)', (username, generate_password_hash(password)))

    def userLogin(self, username, password):
        if not(self.userExist(username)):
            raise DBException('Username/password is wrong.')

        self.c.execute('select password from user where username = %s', (username, ))
        realPassword = self.c.fetchone()[0]

        if not(check_password_hash(realPassword, password)):
            raise DBException('Username/password is wrong.')

    def userLogout(self, token):
        self.c.execute('delete from session where token = %s', (token, ))

    def userChangePassword(self, username, oldPassword, newPassword):
        try:
            self.userLogin(username, oldPassword)
        except DBException as err:
            raise err

        self.c.execute('update user set password=%s where username = %s', (generate_password_hash(newPassword), username))

    def tokenLookup(self, token):
        self.c.execute('select username from session where token = %s', (token,))

        if self.c.rowcount > 0:
            return self.c.fetchone()[0]
        else:
            raise DBException('Session not found')

    def tokenNew(self, username, length = 64):
        while(True):
            try:
                token = randomString(length)
                us = self.tokenLookup(token)
            except DBException:
                break


        self.c.execute('insert into session (username, token) value (%s, %s)', (username, token))
        return token
