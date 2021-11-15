import logging
from rest_framework.views import APIView
from rest_framework import status
from utils.write_response import reformat_resp
from utils.check import check_login, check_params
from .business import *
from utils.utils import *


_logger = logging.getLogger('django')

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
