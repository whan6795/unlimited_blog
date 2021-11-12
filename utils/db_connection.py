from django.db import connection


def db_util(_sql, params=None):
    with connection.cursor() as c:
        if params:
            for i in range(len(params)):
                params[i] = '\'' + str(params[i]) + '\''
            _sql = _sql % tuple(params)
        c.execute(_sql)
        re = c.fetchall()
        desc = c.description
        # print(re, desc)
    return [dict(zip([col[0] for col in desc], row)) for row in re]
