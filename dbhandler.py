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
        self.c.execute('select 1 from user where username = binary %s', (username, ))
        return self.c.rowcount > 0

    def userCreate(self, username, password):
        if self.userExist(username):
            raise DBException('Username exist')

        self.c.execute('insert into user (username, password) value (%s, %s)', (username, generate_password_hash(password)))

    def userLogin(self, username, password):
        if not(self.userExist(username)):
            raise DBException('Username/password is wrong.')

        self.c.execute('select password from user where username = binary %s', (username, ))
        realPassword = self.c.fetchone()[0]

        if not(check_password_hash(realPassword, password)):
            raise DBException('Username/password is wrong.')

    def userLogout(self, token):
        self.c.execute('delete from session where token = binary %s', (token, ))

    def userChangePassword(self, username, oldPassword, newPassword):
        try:
            self.userLogin(username, oldPassword)
        except DBException as err:
            raise err

        self.c.execute('update user set password=%s where username = binary %s', (generate_password_hash(newPassword), username))

    def userOwn(self, username):
        self.c.execute('select map.id, map.url, map.visit from map, own where own.username = binary %s and binary own.id = binary map.id', (username, ))

        return self.c.fetchall()

    def tokenLookup(self, token):
        self.c.execute('select username from session where token = binary %s', (token,))

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

    def urlLookup(self, short):
        self.c.execute('select url from map where id = binary %s', (short, ))

        if self.c.rowcount > 0:
            return self.c.fetchone()[0]
        else:
            raise DBException('URL Not Found')

    def urlNew(self, url, short = None, username = None, length = 3):
        if short is None:
            while(True):
                try:
                    short = randomString(length)
                    _ = self.urlLookup(short)
                except:
                    break
        else:
            try:
                _ = self.urlLookup(short)
            except:
                pass
            else:
                raise DBException('Short URL exists')

        self.c.execute('insert into map (id, url) value (%s, %s)', (short, url))

        if not(username is None):
            self.c.execute('insert into own (username, id) value (%s, %s)', (username, short))

        return short

    def urlDelete(self, username, short):
        self.c.execute('select username from own where id = binary %s', (short, ))

        if self.c.rowcount == 0:
            raise DBException('Not permitted')

        usernameReal = self.c.fetchone()[0]

        if username != usernameReal:
            raise DBException('Not permitted')

        self.c.execute('delete from own where id = binary %s', (short, ))
        self.c.execute('delete from map where id = binary %s', (short, ))

    def urlVisit(self, short):
        self.c.execute('update map set visit = visit + 1 where id = binary %s', (short, ))
