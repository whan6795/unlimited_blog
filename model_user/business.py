from utils.hash import str_md5_encrypt
from utils.db_connection import db_util
import logging
from utils.response_code import RET
from utils.utils import gettime

_logger = logging.getLogger('django')


def login(request, username, password):
    password = str_md5_encrypt(password)
    verify = db_util(
        'SELECT id,username,password,avatar,nickname,introduce FROM user WHERE username=%s;', [username])
    if verify:
        if password == verify[0]['password']:
            request.session['user_id'] = verify[0]['id']
            request.session['username'] = username
            request.session['avatar'] = verify[0]['avatar']
            request.session['nickname'] = verify[0]['nickname']
            request.session['introduce'] = verify[0]['introduce']
            request.session.set_expiry(0)
            detail = {
                "username": username,
                "nickname": verify[0]['nickname'],
                "introduce": verify[0]['introduce'],
                "avatar": verify[0]['avatar']
            }
            # return reformat_resp(RET.OK, {'session_id': request.session.session_key}, '登陆成功')
            return RET.OK, detail, '登陆成功'
        return RET.LOGINERR, {}, '密码错误!'
    return RET.LOGINERR, {}, '用户名不存在'


def reset_password(request, password):
    password = str_md5_encrypt(password)
    now_time = gettime()
    _sql = "UPDATE user SET password=%s,edit_date=%s WHERE username=%s;"
    db_util(_sql, [password, now_time, request.session.get('username')])
    request.session.flush()
    return RET.OK, {}, '修改成功'


def user_info(user_id):
    _sql = 'SELECT id,avatar,nickname,introduce FROM user where id=%s;'
    re = db_util(_sql, [user_id])
    if re:
        return RET.OK, re[0], 'succeed'
    return RET.DATAEMPTY, {}, '无此用户'
