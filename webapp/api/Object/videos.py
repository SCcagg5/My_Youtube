import json, datetime, time
import jwt
import hashlib
import time
import os
import re
import uuid
import phonenumbers
from .sql import sql

class video:
    def __init__(self, id = -1):
        self.id = str(id)
        self.user = self.__user_infos()

    def post(self, name_or, file, usr_id):
        id = str(uuid.uuid4())
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.mkv', '.mp4', '.avi'):
            return [False, "File extension not allowed.", 401]
        save_path = "/home/video/{user_id}/".format(user_id=usr_id)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = "{path}/{file}{ext}".format(path=save_path, file=id, ext=ext)
        file.save(file_path)
        date = str(int(round(time.time() * 1000)))

        succes = sql.input("INSERT INTO `video` (`id`, `user_id`, `name`, `ext`, `date`) VALUES (%s, %s, %s, %s, %s)", \
        (id, usr_id, name_or, ext, date))
        if not succes:
            return [False, "data input error", 500]
        return [True, {"id": id, "path": "{user_id}/{file}{ext}".format(user_id=usr_id, file=id, ext=ext)}, None]
   
    def infos(self):
        res = sql.get("SELECT id, user_id, name, ext, date FROM `video` WHERE id = %s", (self.id))
        if len(res) == 0:
            return [False, "invalid video id", 404]
        ret = {"id": res[0][0], "path": "{user_id}/{file}{ext}".format(user_id=res[0][1], file=res[0][0], ext=res[0][3]), "name": res[0][2], "date": res[0][4]}
        return [True, {"video": ret}, None]

    def delete(self, id, usr_id):
        if self.user["id"] is None:
            return [False, "Video doesn't exist", 404]
        if self.user["id"] != usr_id:
            return [False, "You cannot delete video of another user", 403]
        sql.input("DELETE FROM `video` WHERE `id` = %s", (self.id))
        return [True, {}, None]

    def all_video(self, nm = "", usr = "",  page = 0, perPage = None, strict = False):
        total = sql.get("SELECT COUNT(id) FROM `video`", ())[0][0]
        name = "%" + str("" if nm is None else nm) + "%"
        user = "" if usr is None else usr
        page = 0 if page is None or int(page) - 1 < 0 else int(page) - 1
        perPage = 25 if perPage is None or perPage < 1 else int(perPage)
        res = sql.get("SELECT id, user_id, name, ext, date FROM `video` WHERE user_id = %s " + ("AND" if strict else "OR") + " name LIKE %s LIMIT %s OFFSET %s", (user, name, perPage, perPage * page))

        i = 0
        ret = {}
        while i < len(res):
            ret[res[i][0]] = {"id": res[i][0], "path": "{user_id}/{file}{ext}".format(user_id=res[i][1], file=res[i][0], ext=res[i][3]), "name": res[i][2], "date": res[i][4]}
            i += 1
        return [True, {"videos": ret, "pager": {"total": total, "current": {"from": int(perPage * page + 1), "to": int(perPage * (page + 1))}, "options": {"name": nm, "user": usr,  "perPage": perPage, "page": page + 1}}}, None]

    def modify(self, name, usr_id):
        if self.user["id"] is None:
            return [False, "Video doesn't exist", 404]
        if self.user["id"] != usr_id:
            return [False, "You cannot edit video of another user", 403]
        succes = sql.input("UPDATE `video` SET `name` = %s WHERE id = %s", (name, self.id))
        if not succes:
            return [False, "data input error", 500]
        return [True, {}, None]

    def __user_infos(self):
        res = sql.get("SELECT `user`.id, `user`.pseudo, `user`.username, `user`.date FROM video INNER JOIN user ON `user`.id = `video`.`user_id` WHERE `video`.id = %s ", (self.id))
        ret = {"id": None, "username": None , "pseudo": None, "since": None}
        if len(res) > 0:
            ret["id"]= res[0][0]
            ret["pseudo"] = res[0][1]
            ret["username"] = res[0][2]
            ret["since"] = res[0][3]
        return ret
