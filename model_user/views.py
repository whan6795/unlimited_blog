from rest_framework.views import APIView
from rest_framework import status
from utils.write_response import reformat_resp
from utils.check import check_login, check_params
from utils.utils import *
from .business import *

_logger = logging.getLogger('django')


class LoginView(APIView):

    def post(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.POST)), get_ip(request)))
        needed_params = ['username', 'password']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        code, body, message = login(request, username, password)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)


class CheckLoginView(APIView):

    @check_login
    def get(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        _logger.info('response:[%s,%s,%s]' % (RET.OK, {}, 'succeed'))
        return reformat_resp(RET.OK, {}, 'succeed')


class LogOutView(APIView):

    @check_login
    def get(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        request.session.flush()
        _logger.info('response:[%s,%s,%s]' % (RET.OK, {}, 'succeed'))
        return reformat_resp(RET.OK, {}, 'succeed')


#  查看用户信息
class ShowUserInfoHandler(APIView):

    @check_login
    def get(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        needed_params = ['user_id']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        user_id = request.GET.get('user_id')
        code, body, message = user_info(user_id)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)


#  用户修改自己的密码
class ChangePasswordHandler(APIView):

    @check_login
    def patch(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.POST)), get_ip(request)))
        needed_params = ['password']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        password = request.POST.get('password', '')
        code, body, message = reset_password(request, password)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)

