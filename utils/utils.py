import time


def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_ip(request):
    """获取请求者的IP信息"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def sql_fuzzy_condition(**kwargs):
    _sql = ' '
    for k, v in kwargs.items():
        _sql += ' {} like \'%%{}%%\' AND'.format(k, v)
    return _sql[:-3]


def sql_exact_condition(**kwargs):
    _sql = ' '
    for k, v in kwargs.items():
        _sql += ' {} = \'{}\' AND'.format(k, v)
    return _sql[:-3]
