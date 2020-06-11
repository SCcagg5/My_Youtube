import json, datetime, time
import jwt
import hashlib
import time
import os
import re
import uuid
import phonenumbers
from .sql import sql
from .videos import video

class comment:
    def post(text, user_id, video_id):
        id = str(uuid.uuid4())
        date = str(int(round(time.time() * 1000)))

        if video(video_id).user["id"] is None:
            return [False, "Invalid video id", 404]

        succes = sql.input("INSERT INTO `comment` (`id`, `video_id`, `user_id`, `text`, `date`) VALUES (%s, %s, %s, %s, %s)", \
        (id, video_id, user_id, text, date))
        if not succes:
            return [False, "data input error", 500]
        return [True, {"id": id, "video_id": video_id, "user_id": user_id, "text": text, "date": date}, None]

    def all_comment(vid_id, page = 0, perPage = None):
        total = sql.get("SELECT COUNT(id) FROM `comment` WHERE video_id = %s", (vid_id))[0][0]
        page = 0 if page is None or int(page) - 1 < 0 else int(page) - 1
        perPage = 50 if perPage is None or perPage < 1 else int(perPage)

        res = sql.get("SELECT `id`, `user_id`, `text`, `date` FROM `comment` WHERE video_id = %s LIMIT %s OFFSET %s", (vid_id, perPage, perPage * page))

        i = 0
        ret = {}
        while i < len(res):
            ret[res[i][0]] = {"id": res[i][0], "user_id": res[i][1], "text": res[i][2], "date": res[i][3]}
            i += 1
        return [True, {"comments": ret, "pager": {"total": total, "current": {"from": int(perPage * page + 1), "to": int(perPage * (page + 1))}, "options": {"video": vid_id,  "perPage": perPage, "page": page + 1}}}, None]
