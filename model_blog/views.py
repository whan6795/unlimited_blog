import logging
from rest_framework.views import APIView
from rest_framework import status
from utils.write_response import reformat_resp
from utils.check import check_login, check_params
from .business import *
from utils.utils import *


_logger = logging.getLogger('django')


# 博客门户
class BlogPortalHandler(APIView):

    # 获取文章列表和详情
    def get(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 8))
        if page < 1 or page_size < 1:
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        title = request.GET.get('title', '')
        # label = request.GET.get('label', '')
        blog_id = request.GET.get('blog_id', '')
        author = request.GET.get('author', '')
        cur_page = (page - 1) * page_size
        user_id = request.session.get('user_id', '')
        code, body, message = get_blog_portal(title, blog_id, cur_page, page_size, user_id)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)


# 个人主页
class BlogManageHandler(APIView):

    # 获取文章列表和详情
    def get(self, request, user_id):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 8))
        if page < 1 or page_size < 1:
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        title = request.GET.get('title', '')
        label = request.GET.get('label', '')
        blog_id = request.GET.get('blog_id', '')
        author = request.GET.get('author', '')
        cur_page = (page - 1) * page_size
        user_id = request.session.get('user_id', '')
        code, body, message = get_blog(title, label, blog_id, cur_page, page_size, user_id)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)

    # 添加文章
    @check_login
    def post(self, request, user_id):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.POST)), get_ip(request)))
        needed_params = ['title', 'content', 'status']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        title = request.POST.get('title')
        content = request.POST.get('content')
        _status = request.POST.get('status')
        label = request.POST.get('label', '')
        user = request.session.get('user_id')
        code, body, message = add_blog(title, label, content, user, _status)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)

    # 删除文章
    @check_login
    def delete(self, request, user_id):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        needed_params = ['blog_id']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        blog_id = request.GET.get('blog_id')
        code, body, message = delete_blog(blog_id)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)

    # 编辑文章
    @check_login
    def put(self, request, user_id):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.POST)), get_ip(request)))
        needed_params = ['blog_id', 'title', 'content', 'status']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        blog_id = request.POST.get('blog_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        _status = request.POST.get('status')
        label = request.POST.get('label', '')
        user = request.session.get('user_id')
        code, body, message = edit_blog(blog_id, title, label, content, user, _status)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)
