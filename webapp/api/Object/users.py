import json, datetime, time
import jwt
import hashlib
import time
import os
import re
import uuid
import phonenumbers
from .sql import sql

class user:
    def __init__(self, id = -1):
        self.id = str(id)

    def gettoken(self, id = None):
        id = self.__getid(id, self.id)
        secret =  self.__getsecret()
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=48)
        ret = jwt.encode({'exp': exp, 'id': id, 'password': hash(str(id) + str(secret))}, secret).decode('utf-8')
        return [True, {'exp': str(exp), "usrtoken": str(ret)}, None, {"usrtoken": str(ret)}]

    def verify(self, token, id = None):
        secret = self.__getsecret()
        try:
            decoded = jwt.decode(token, secret, leeway=10, algorithms=['HS256'])
            id = self.__getid(id, decoded["id"])
            if decoded["password"] != hash(str(id) + str(secret)):
                 raise
            self.id = id
        except jwt.ExpiredSignature:
            return [False, "Signature expired", 403]
        except:
            return  [False, "Invalid usrtoken", 400]
        return [True, {}, None]

    def register(self, usr, pseudo, email, passw):
        if self.__exist_email(email):
            return [False, "Email already in use", 400]
        if self.__exist_username(usr):
            return [False, "Username already in use", 400]
        if not self.__email(email):
            return [False, "Invalid email", 400]

        id = str(uuid.uuid4())
        password = self.__hash(email, passw)
        date = str(int(round(time.time() * 1000)))

        succes = sql.input("INSERT INTO `user` (`id`, `username`, `pseudo`, `email`, `password`, `date`) VALUES (%s, %s, %s, %s, %s, %s)", \
        (id, usr, pseudo, email, password, date))
        if not succes:
            return [False, "data input error", 500]
        return [True, {}, None]

    def login(self, email, passw):
        password = self.__hash(email, passw)
        res = sql.get("SELECT `id`  FROM `user` WHERE `email` = %s AND `password` = %s", (email, password))
        if len(res) > 0:
            self.id = str(res[0][0])
            return [True, {"user_id": self.id}, None]
        else:
            res = sql.get("SELECT `email`  FROM `user` WHERE `username` = %s", (email))
            if len(res) > 0:
                email = str(res[0][0])
                password = self.__hash(email, passw)
                res = sql.get("SELECT `id`  FROM `user` WHERE `email` = %s AND `password` = %s", (email, password))
                if len(res) > 0:
                    self.id = str(res[0][0])
                    return [True, {"user_id": self.id}, None]
        return [False, "Invalid email or password", 403]

    def delete(self, id):
        if self.id != str(id):
            return [False, "You cannot delete another user", 403]
        sql.input("DELETE FROM `user` WHERE `id` = %s", (self.id))
        return [True, {}, None]

    def update_data(self, id, username, pseudo, email, passw):
         if self.id != str(id):
             return [False, "You cannot edit another user", 403]
         password = self.__hash(email, passw)
         date = str(int(round(time.time() * 1000)))

         succes = sql.input("INSERT `user` (`id`, `username`, `pseudo`, `email`, `password`, `date`) \
                            VALUES (%s, %s, %s, %s, %s, %s) \
                            ON DUPLICATE KEY \
                            UPDATE `username` = %s, `pseudo` = %s, `email` = %s, `password` = %s",
                 (id, username, pseudo, email, password, date, username, pseudo, email, password))
         if not succes:
             return [False, "data input error", 500]
         return [True, {}, None]

    def infos(self, id = None):
        if id is None:
            id = self.id
        res = sql.get("SELECT username, pseudo, email, date FROM user WHERE id = %s", (id))
        if len(res) > 0:
            ret = {'username': '@' + str(res[0][0]), 'pseudo': str(res[0][1]), 'since': str(res[0][3])}
            if self.id == str(id):
                ret["email"] = res[0][2]
            return [True, {str(id): ret}, None]
        return [False, "Invalid user id", 404]

    def all_user(self, psd = "", page = 0, perPage = None):
        total = sql.get("SELECT COUNT(id) FROM `user`", ())[0][0]
        pseudo = "%" + str("" if psd is None else psd) + "%"
        page = 0 if page is None or int(page) - 1 < 0 else int(page) - 1
        perPage = 25 if perPage is None or perPage < 1 else int(perPage)
        res = sql.get("SELECT id, username, pseudo, date FROM `user` WHERE username LIKE %s OR pseudo LIKE %s LIMIT %s OFFSET %s", (pseudo, pseudo, perPage, perPage * page))

        i = 0
        ret = {}
        while i < len(res):
            ret[res[i][0]] = {'username': '@' + str(res[i][1]), 'pseudo': str(res[i][2]), 'since': str(res[i][3])}
            i += 1
        return [True, {"users": ret, "pager": {"total": total, "current": {"from": int(perPage * page + 1), "to": int(perPage * (page + 1))}, "options": {"perPage": perPage, "page": page + 1, "search": psd}}}, None]

    def __hash(self, email, password):
        if password is None or email is None:
            return None
        s = len(email)
        n = s % (len(password) - 1 if len(password) > 1 else 1)
        secret = self.__getsecret()
        salted = password[:n] + str(s) + password[n:] + secret
        hashed = hashlib.sha512(salted.encode('utf-8')).hexdigest()
        return hashed

    def __exist_email(self, email):
        res = sql.get("SELECT `id` FROM `user` WHERE `email` = %s", (email))
        if len(res) > 0:
            return True
        return False

    def __exist_username(self, usr):
        res = sql.get("SELECT `id` FROM `user` WHERE `username` = %s", (usr))
        if len(res) > 0:
            return True
        return False

    def __getsecret(self):
        return str(os.getenv('API_SCRT', '!@ws4RT4ws212@#%'))

    def __getid(self, id, idbis = None):
        return id if id != "-1" and id is not None else idbis if idbis is not None else self.id

    def __email(self, email):
        return re.match("[^@]+@[^@]+\.[^@]+", email)
