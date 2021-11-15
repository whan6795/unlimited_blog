from utils.hash import str_md5_encrypt
from utils.db_connection import db_util
import logging
from utils.response_code import RET
from utils.utils import gettime

_logger = logging.getLogger('django')


def login(request, username, password):
    password = str_md5_encrypt(password)
    verify = db_util(
        'SELECT id,username FROM user WHERE username=%s AND password=%s;',
        [username, password])
    if verify:
        # print(verify)
        request.session['user_id'] = verify[0]['id']
        request.session['username'] = username
        request.session.set_expiry(0)
        # return reformat_resp(RET.OK, {'session_id': request.session.session_key}, '登陆成功')
        return RET.OK, {'name': verify[0]['username']}, '登陆成功'
    return RET.LOGINERR, {}, '用户名或密码错误'


def reset_password(request, password):
    password = str_md5_encrypt(password)
    now_time = gettime()
    _sql = "UPDATE user SET password=%s,edit_date=%s WHERE username=%s;"
    db_util(_sql, [password, now_time, request.session.get('username')])
    request.session.flush()
    return RET.OK, {}, '修改成功'


def user_info(user_id):
    _sql = 'SELECT id,avator,nickname,introduce FROM ywg_genesis_employee_info where id=%s;'
    re = db_util(_sql, [user_id])
    if re:
        return RET.OK, re[0], 'succeed'
    return RET.OK, {}, 'succeed'
