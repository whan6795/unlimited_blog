import base64
import re, math
import datetime
from utils.response_code import RET
from utils.db_connection import db_util
from utils.tencent_cos import TencentCos
from utils.utils import gettime


def get_blog_info(title, label, blog_id, cur_page, page_size, login):
    if blog_id:
        _sql = 'SELECT title,concat(\'[\',GROUP_CONCAT(bl.label_name),\']\') as labels,b.add_date,b.edit_date,\
        case when u.nickname is not null then u.nickname else \'[已注销]\' end as author\
        ,content FROM label_of_blog as lob,blog_labels as bl,blog as b LEFT JOIN user as u ON b.author=u.id \
        WHERE bl.id=lob.label_id and b.id=lob.blog_id and b.id=%s' % blog_id
        # print(_sql)
        result = db_util(_sql)
        if result[0]['title']:
            return RET.OK, result[0], 'succeed'
        return RET.QUERYEMPTY, {}, '无此文章'
    _sql_re = 'SELECT title,concat(\'[\',GROUP_CONCAT(bl.label_name),\']\') as labels,b.add_date,b.edit_date,\
    case when u.nickname is not null then u.nickname else \'[已注销]\' end as author,left(content,50) as content FROM \
    label_of_blog as lob,blog_labels as bl,blog as b LEFT JOIN user as u ON b.author=u.id WHERE bl.id=lob.label_id AND b.id=lob.blog_id'
    _sql_count = 'SELECT COUNT(*) as total_records FROM blog as b'
    if not title and not label and login:
        _sql_re += ' ORDER BY id DESC LIMIT %d,%d;' % (cur_page, page_size)
        # print(_sql_re, '\n', _sql_count)
        res = db_util(_sql_re)
        total_records = db_util(_sql_count)[0]['total_records']
        total_page = math.ceil(total_records / page_size) if total_records else 1
    else:
        _sql_re += ' AND'
        _sql_count += ' WHERE'
        if title:
            _sql_title = ' title LIKE \'%%{}%%\' AND'.format(title)
            _sql_re += _sql_title
            _sql_count += _sql_title
        if label:
            label = eval(label)
            _sql_label = ' b.id IN (SELECT blog_id FROM label_of_blog WHERE'
            for i in label:
                _sql_label += ' label_id=%s OR' % i
            _sql_label = _sql_label[:-2]
            _sql_label += ') AND'
            _sql_re += _sql_label
            _sql_count += _sql_label
        if not login:
            _sql_login = ' status=1 AND'
            _sql_re += _sql_login
            _sql_count += _sql_login
        _sql_re = _sql_re[:-3]
        _sql_re += ' GROUP BY lob.blog_id ORDER BY b.id DESC LIMIT %d,%d;' % (cur_page, page_size)
        _sql_count = _sql_count[:-3]
        # print(_sql_re, '\n', _sql_count)
        res = db_util(_sql_re)
        total_records = db_util(_sql_count)[0]['total_records']
        total_page = math.ceil(total_records / page_size) if total_records else 1
    data = {
        'blog_list': res,
        "total_records": total_records,
        "total_page": total_page
    }
    if total_records == 0:
        return RET.QUERYEMPTY, {}, '无结果'
    return RET.OK, data, 'succeed'


def add_blog(title, label, content, user, _status):
    _sql = 'INSERT INTO blog (title,content,author,status) VALUES (%s,%s,%s,%s);'
    db_util(_sql, [title, content, user, _status])
    _sql = 'SELECT MAX(id) AS max_id FROM blog;'
    _id = db_util(_sql)[0]['max_id']
    if label:
        _sql = ''
        label = eval(label)
        for i in label:
            _sql += 'INSERT INTO label_of_blog (blog_id,label_id) VALUES (%s,%s);' % (_id, i)
        db_util(_sql)
    return RET.OK, {}, 'succeed'
    # _sql = 'INSERT INTO label_of_blog () VALUES ();'


def delete_blog(blog_id):
    _sql = 'DELETE FROM blog WHERE id=%s;' % blog_id
    _sql += 'DELETE FROM label_of_blog WHERE blog_id=%s;' % blog_id
    db_util(_sql)
    return RET.OK, {}, 'succeed'
