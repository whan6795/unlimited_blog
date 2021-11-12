from utils.db_connection import db_util
from .write_response import reformat_resp
from rest_framework import status
from .response_code import RET
import logging
import os

_logger = logging.getLogger('django')
setting_file = os.environ.get('ENV', 'prod')


def check_user_power(power_list: list):
    def outwrapper(func):
        def wrapper(obj, request, *args, **kwargs):
            role_id = request.session.get('role_id', '')
            # print('role_id:', role_id)
            if role_id:
                _sql = 'SELECT id FROM ywg_genesis_roles_power WHERE role_id=%s AND value=1 AND (id=%s'
                _sql += 'OR id=%s ' * (len(power_list) - 1)
                _sql += ');'
                power = db_util(_sql, [role_id] + power_list)
                # print('model_power:', model_power)
                if power:
                    _logger.info('已授权的用户访问，用户role：%s,权限列表：%s' % (role_id, str(power_list)))
                    return func(obj, request, *args, **kwargs)
            _logger.info('无权限授权的用户访问，用户role：%s,权限列表：%s' % (role_id, str(power_list)))
            return reformat_resp(RET.REQERR, {}, "无权限", http_status=status.HTTP_403_FORBIDDEN)

        return wrapper

    return outwrapper


if setting_file == 'local':
    def check_login(func):
        def wrapper(obj, request, *args, **kwargs):
            _logger.info('本地测试，不进行登录验证')
            return func(obj, request, *args, **kwargs)

        return wrapper
else:
    def check_login(func):
        def wrapper(obj, request, *args, **kwargs):
            user_id = request.session.get('user_id', '')
            if user_id != '':
                _logger.info('已登录，用户id：%s' % user_id)
                return func(obj, request, *args, **kwargs)
            _logger.info('未登录')
            return reformat_resp(RET.ROLEERR, {}, "未登录或登录信息过期", http_status=status.HTTP_401_UNAUTHORIZED)

        return wrapper


def check_params(request, needed_params):
    method = request.method
    method = 'GET' if method == 'DELETE' else method
    method = 'POST' if method == 'PATCH' or method == 'PUT' else method
    request_data = eval('request.%s' % method)
    effective_keys = [i for i in request_data.keys() if request_data.get(i)]
    return set(needed_params) <= set(effective_keys)
