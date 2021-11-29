import logging
from rest_framework.views import APIView
from rest_framework import status
from utils.write_response import reformat_resp
from utils.check import check_login, check_params
from .business import *
from utils.utils import *


_logger = logging.getLogger('django')


class BlogManageHandler(APIView):

    # 获取文章列表和详情
    def get(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        # print(1111111111111111)
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 8))
        if page < 1 or page_size < 1:
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        title = request.GET.get('title', '')
        label = request.GET.get('label', '')
        blog_id = request.GET.get('blog_id', '')
        cur_page = (page - 1) * page_size
        if_login = request.session.get('user_id', '')
        code, body, message = get_blog_info(title, label, blog_id, cur_page, page_size, if_login)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)

    # 添加文章
    @check_login
    def post(self, request):
        _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
        needed_params = ['title', 'content', 'status']
        if not check_params(request, needed_params):
            _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
            return reformat_resp(RET.PARAMERR, {}, '参数错误')
        title = request.POST.get('title')
        content = request.POST.get('content')
        _status = request.POST.get('status')
        label = request.POST.get('label', '')
        user = request.session.get('user_id', 1)
        code, body, message = add_blog(title, label, content, user, _status)
        _logger.info('response:[%s,%s,%s]' % (code, body, message))
        return reformat_resp(code, body, message)

    # 删除文章
    @check_login
    def delete(self, request):
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
    def put(self, request):
        pass

#
# class Test(APIView):
#
#     def post(self, request):
#         _logger.info('input params:%s, from ip:%s' % (str(dict(request.POST)), get_ip(request)))
#         needed_params = ['image_base64']
#         if not check_params(request, needed_params):
#             _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
#             return reformat_resp(RET.PARAMERR, {}, '参数错误')
#         base64img = request.POST.get('image_base64')
#         _url = upload_img_to_ali_oss(base64img)
#         # _logger.info('response:[%s,%s,%s]' % (code, body, message))
#         return reformat_resp(RET.OK, {}, _url)
#
#     def delete(self, request):
#         _logger.info('input params:%s, from ip:%s' % (str(dict(request.GET)), get_ip(request)))
#         needed_params = ['file_list']
#         if not check_params(request, needed_params):
#             _logger.info('response:[%s,%s,%s]' % (RET.PARAMERR, {}, '参数错误'))
#             return reformat_resp(RET.PARAMERR, {}, '参数错误')
#         img_id = eval(request.GET.get('file_list'))
#         delete_picture_from_cos(img_id)
#         # _logger.info('response:[%s,%s,%s]' % (code, body, message))
#         return reformat_resp(RET.OK, {}, '')
