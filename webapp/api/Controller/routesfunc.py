from Model.basic import check, auth
from Object.users import user
from Object.videos import video
from Object.comments import comment
from Object.admin import admin
import json

def signup(cn, nextc):
    err = check.contain(cn.pr, ["username", "pseudo", "email", "password"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = user()
    err = use.register(cn.pr["username"], cn.pr["pseudo"], cn.pr["email"], cn.pr["password"])
    cn.private["user"] = use

    return cn.call_next(nextc, err)

def signin(cn, nextc):
    err = check.contain(cn.pr, ["login", "password"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = user()
    err = use.login(cn.pr["login"], cn.pr["password"])
    cn.private["user"] = use

    return cn.call_next(nextc, err)

def authuser(cn, nextc):
    err = check.contain(cn.hd, ["usrtoken"], "HEAD")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.hd = err[1]

    use = user()
    err = use.verify(cn.hd["usrtoken"])
    cn.private["user"] = use

    return cn.call_next(nextc, err)

def get_token(cn, nextc):
    err = check.contain(cn.pr, [])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = cn.private["user"]
    err = use.gettoken()
    return cn.call_next(nextc, err)

def verifykey(cn, nextc):
    err = check.contain(cn.pr, ["key"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = user()
    err = use.verify_key(cn.pr["key"])
    cn.private["user"] = use
    return cn.call_next(nextc, err)

def check_act(cn, nextc):
    use = cn.private["user"]
    err = use.check_activation()
    return cn.call_next(nextc, err)

def delete_user(cn, nextc):
    use = cn.private["user"]
    err = use.delete(cn.rt["user"])
    return cn.call_next(nextc, err)

def modify_user(cn, nextc):
    err = check.contain(cn.pr, ["username", "pseudo", "email"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = cn.private["user"]
    err = use.update_data(cn.rt["user"], cn.pr["username"], cn.pr["pseudo"], cn.pr["email"])
    return cn.call_next(nextc, err)

def get_user(cn, nextc):
    use = cn.private["user"]
    err = use.infos(cn.rt["user"])
    return cn.call_next(nextc, err)

def get_all_users(cn, nextc):
    cn.get = check.setnoneopt(cn.get, ["pseudo", "perpage", "page"])
    err = user().all_user(cn.get["pseudo"], cn.get["page"], cn.get["perpage"])
    return cn.call_next(nextc, err)

def post_video(cn, nextc):
    err = check.contain(cn.req.files, ["file"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = check.contain(cn.req.forms, ["name"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    if str(cn.private["user"].id) != str(cn.rt["user"]):
        return cn.toret.add_error("Invalid rights", 403)

    use = video()
    err = use.post(cn.req.forms["name"], cn.req.files["file"], cn.rt["user"])
    return cn.call_next(nextc, err)

def get_videos(cn, nextc):
    cn.get = check.setnoneopt(cn.get, ["name", "perpage", "page"])
    user = str(cn.rt["user"] if "user" in cn.rt else "")
    err = video().all_video(cn.get["name"], user, cn.get["page"], cn.get["perpage"], True)
    return cn.call_next(nextc, err)

def get_video(cn, nextc):
    err = video(cn.rt["video"] if "video" in cn.rt else None).infos()
    return cn.call_next(nextc, err)

def patch_video(cn, nextc):
    err = [False, "Not implemented", 404]
    return cn.call_next(nextc, err)

def modify_video(cn, nextc):
    err = check.contain(cn.pr, ["name"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    use = video(cn.rt["video"])
    err = use.modify(cn.pr["name"], cn.private["user"].id)
    return cn.call_next(nextc, err)

def delete_video(cn, nextc):
    err = video(cn.rt["video"]).delete(cn.rt["video"], cn.private["user"].id)
    return cn.call_next(nextc, err)

def get_all_videos(cn, nextc):
    cn.get = check.setnoneopt(cn.get, ["name", "user", "perpage", "page"])
    err = video().all_video(cn.get["name"], cn.get["user"], cn.get["page"], cn.get["perpage"])
    return cn.call_next(nextc, err)

def post_comment(cn, nextc):
    err = check.contain(cn.pr, ["text"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.hd = err[1]
    err = comment.post(cn.pr["text"], cn.private["user"].id, cn.rt["video"])
    return cn.call_next(nextc, err)


def get_comment(cn, nextc):
    video = str(cn.rt["video"] if "video" in cn.rt else "")
    cn.get = check.setnoneopt(cn.get, ["perpage", "page"])
    err = comment.all_comment(video, cn.get["page"], cn.get["perpage"])
    return cn.call_next(nextc, err)

def admtoken(cn, nextc):
    err = check.contain(cn.pr, ["password"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    err = admin.gettoken(cn.pr["password"])
    return cn.call_next(nextc, err)


def authadmin(cn, nextc):
    err = check.contain(cn.hd, ["admtoken"], "HEAD")
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.hd = err[1]

    err = admin.verify(cn.hd["admtoken"])
    return cn.call_next(nextc, err)

def all_users(cn, nextc):
    err = admin.all_user()
    return cn.call_next(nextc, err)

def gettokenadm(cn, nextc):
    err = check.contain(cn.pr, ["usr_id"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = user(cn.pr["usr_id"])
    err = use.gettoken()
    return cn.call_next(nextc, err)
