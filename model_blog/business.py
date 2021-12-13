import base64
import re, math
import datetime
from utils.response_code import RET
from utils.db_connection import db_util
from utils.tencent_cos import TencentCos
from utils.utils import gettime


# 门户
def get_blog_portal(title, author, cur_page, page_size, user_id):
    _sql_re = """SELECT title,b.add_date,b.edit_date,
    case when u.nickname is not null then u.nickname else '[已注销]' end as author,left(content,20) as content 
    FROM blog AS b LEFT JOIN label_of_blog as lob ON b.id=lob.blog_id 
    LEFT JOIN user as u ON b.author=u.id 
    WHERE 1=1"""
    _sql_count = 'SELECT COUNT(*) as total_records FROM blog as b{user} WHERE 1=1'
    if title:
        _sql_title = ' AND b.title LIKE \'%%%%{}%%%%\''.format(title)
        _sql_re += _sql_title
        _sql_count += _sql_title
    if user_id:
        _sql_count = _sql_count.format(user=' LEFT JOIN user AS u ON b.author=u.id')
        _sql_user = ' AND b.author=%s OR (b.author!=%s AND b.status=1)' % user_id
        _sql_re += _sql_user
        _sql_count += _sql_user
    else:
        _sql_count = _sql_count.format(user='')
        _sql_user = ' AND b.status=1'
        _sql_re += _sql_user
        _sql_count += _sql_user
    _sql_re += ' ORDER BY b.id DESC LIMIT {},{};'.format(cur_page, page_size)
    _sql_count += ';'
    res = db_util(_sql_re)
    total_records = db_util(_sql_count)[0]['total_records']
    if total_records:
        total_page = math.ceil(total_records / page_size) if total_records else 1
        data = {
            'blog_list': res,
            "total_records": total_records,
            "total_page": total_page
        }
        return RET.OK, data, 'succeed'
    return RET.QUERYEMPTY, {}, '无结果'


# 个人主页-查看
def get_blog(title, label, blog_id, cur_page, page_size, user_id):
    if blog_id:
        # TODO status=0时情况
        _sql = 'SELECT title,concat(\'[\',GROUP_CONCAT(DISTINCT bl.label_name),\']\') as labels,b.add_date,b.edit_date,\
        case when u.nickname is not null then u.nickname else \'[已注销]\' end as author,content \
        FROM blog AS b LEFT JOIN label_of_blog as lob ON b.id=lob.blog_id \
        LEFT JOIN blog_labels as bl ON (lob.label_id=bl.id AND bl.user_id = b.author) \
        LEFT JOIN user as u ON b.author=u.id \
        WHERE b.id=%s' % blog_id
        # print(_sql)
        result = db_util(_sql)
        if result[0]['title']:
            return RET.OK, result[0], 'succeed'
        return RET.QUERYEMPTY, {}, '无此文章'
    _sql_re = 'SELECT title,label.labels,b.add_date,b.edit_date,\
    case when u.nickname is not null then u.nickname else \'[已注销]\' end as author,left(content,20) as content \
    FROM blog AS b LEFT JOIN label_of_blog as lob ON b.id=lob.blog_id \
    LEFT JOIN blog_labels AS bl ON (lob.label_id=bl.id AND bl.user_id=b.author) \
    LEFT JOIN user as u ON b.author=u.id \
    LEFT JOIN \
    (SELECT b.id,concat(\'[\',GROUP_CONCAT(DISTINCT bl.label_name),\']\') as labels FROM blog AS b \
    LEFT JOIN label_of_blog AS lob ON b.id=lob.blog_id \
    LEFT JOIN blog_labels AS bl ON (lob.label_id=bl.id AND bl.user_id = b.author)) AS label ON label.id=b.id \
    WHERE 1=1'
    _sql_count = 'SELECT COUNT(*) as total_records FROM blog as b{user} WHERE 1=1'
    if title:
        _sql_title = ' AND b.title LIKE \'%%%%{}%%%%\''.format(title)
        _sql_re += _sql_title
        _sql_count += _sql_title
    if user_id:
        _sql_count = _sql_count.format(user=' LEFT JOIN user AS u ON b.author=u.id')
        _sql_user = ' AND b.author=%s OR (b.author!=%s AND b.status=1)' % user_id
        _sql_re += _sql_user
        _sql_count += _sql_user
    else:
        _sql_count = _sql_count.format(user='')
        _sql_user = ' AND b.status=1'
        _sql_re += _sql_user
        _sql_count += _sql_user
    _sql_re += ' ORDER BY b.id DESC LIMIT {},{};'.format(cur_page, page_size)
    _sql_count += ';'
    res = db_util(_sql_re)
    total_records = db_util(_sql_count)[0]['total_records']
    if total_records:
        total_page = math.ceil(total_records / page_size) if total_records else 1
        data = {
            'blog_list': res,
            "total_records": total_records,
            "total_page": total_page
        }
        return RET.OK, data, 'succeed'
    return RET.QUERYEMPTY, {}, '无结果'


# 个人主页-新增
def add_blog(title, label, content, user, _status):
    _sql = 'INSERT INTO blog (title,content,author,status) VALUES (%s,%s,%s,%s);'
    db_util(_sql, [title, content, user, _status])
    _sql = 'SELECT MAX(id) AS max_id FROM blog;'
    res = db_util(_sql)
    _id = res[0]['max_id'] if res else 0
    if label:
        _sql = ''
        label = eval(label)
        for i in label:
            _sql += 'INSERT INTO label_of_blog (blog_id,label_id) VALUES (%s,%s);' % (_id, i)
        db_util(_sql)
    return RET.OK, {}, 'succeed'
    # _sql = 'INSERT INTO label_of_blog () VALUES ();'


# 个人主页-删除
def delete_blog(blog_id):
    _sql = 'DELETE FROM blog WHERE id=%s;' % blog_id
    _sql += 'DELETE FROM label_of_blog WHERE blog_id=%s;' % blog_id
    db_util(_sql)
    return RET.OK, {}, 'succeed'


# 个人主页-修改
def edit_blog(blog_id, title, label, content, user, _status):
    pass
