import base64
import re, math
import datetime
from utils.response_code import RET
from utils.db_connection import db_util
from utils.tencent_cos import TencentCos
from utils.utils import gettime


def upload_img_to_ali_oss(base64file):
    spl_image_b64 = re.split(r"[:;,]", base64file)
    image_type = re.split(r"/", spl_image_b64[1])
    image = base64.urlsafe_b64decode(spl_image_b64[3])
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    tencent_cos = TencentCos()
    file_name = '%s.%s' % (now_time, image_type[1])
    result = tencent_cos.put_file(file_name, image)
    return result


def delete_picture_from_cos(file_list):
    tencent_cos = TencentCos()
    tencent_cos.delete_files(file_list)
    # img_path = db_util('SELECT image_path FROM ywg_genesis_image_info WHERE image_id=\'%s\';' % img_id)
    # if not img_path:
    #     return False
    # img_path = img_path[0]['image_path']
    # aliyun_oss = AliyunOss()
    # aliyun_oss.delete_file(img_path)
    return True


def upload_img(base64file, img_name, img_type_id, user_id):
    """
    :param base64file:base64格式文件
    :return:阿里云上传结果
    """
    result = upload_img_to_ali_oss(base64file)
    if result['status'] == 200:
        _sql = 'INSERT INTO ywg_genesis_image_info (image_name,image_type_id,image_path,creator_id,add_date) VALUES (%s,%s,%s,%s,%s);'
        db_util(_sql, [img_name, img_type_id, result['url'], user_id, gettime()])
        return RET.OK, {}, 'succeed'
    else:
        print(result['detail'].resp)
        err_detail = {
            'ali_status': result['detail'].status,
            'ali_documents': 'https://help.aliyun.com/document_detail/32039.html'
        }
        return RET.THIRDERR, err_detail, 'fail'


def get_picture_list(page_size, cur_page, img_name):
    if img_name == 'all':
        total_records = db_util('SELECT COUNT(*) AS total_records FROM ywg_genesis_image_info;')[0]['total_records']
        total_page = math.ceil(total_records / page_size) if total_records else 1
        _sql = 'SELECT image_id,image_name,image_path FROM ywg_genesis_image_info ORDER BY image_id DESC LIMIT %d,%d;' % (cur_page, page_size)
        # print(_sql)
        detail = {
            'picture_list': db_util(_sql),
            'total_page': total_page,
            'total_records': total_records
        }
        return RET.OK, detail, 'succeed'
    else:
        total_records = db_util(
            'SELECT COUNT(*) AS total_records FROM ywg_genesis_image_info WHERE image_name LIKE \'%%{}%%\';'.format(
                img_name))[0]['total_records']
        total_page = math.ceil(total_records / page_size) if total_records else 1
        _sql = 'SELECT image_id,image_name,image_path from ywg_genesis_image_info WHERE image_name LIKE \'%%{}%%\' ORDER BY image_id DESC LIMIT {},{};'.format(
            img_name, cur_page, page_size)
        detail = {
            'picture_list': db_util(_sql),
            'total_page': total_page,
            'total_records': total_records
        }
        return RET.OK, detail, 'succeed'


def delete_picture_from_ali_oss(img_id):
    pass
    return True


def delete_picture(img_id):
    flag = delete_picture_from_ali_oss(img_id)
    if flag:
        db_util('DELETE FROM ywg_genesis_image_info WHERE image_id=%s;' % img_id)
        return RET.OK, {}, 'succeed'
    return RET.PARAMERR, {}, '图片id错误'


def update_picture_info(img_id, img_name, img_type_id, img_path):
    if not img_path.startswith('https://'):
        flag = delete_picture_from_ali_oss(img_id)
        if not flag:
            return RET.PARAMERR, {}, '图片id错误'
        result = upload_img_to_ali_oss(img_path)
        if result['status'] == 200:
            img_path = result['url']
        else:
            print(result['detail'].resp)
            err_detail = {
                'ali_status': result['detail'].status,
                'ali_documents': 'https://help.aliyun.com/document_detail/32039.html'
            }
            return RET.THIRDERR, err_detail, '上传阿里云失败'
    _sql = 'UPDATE ywg_genesis_image_info SET image_name=%s,image_type_id=%s,image_path=%s,edit_date=%s WHERE image_id=%s;'
    db_util(_sql, [img_name, img_type_id, img_path, gettime(), img_id])
    return RET.OK, {}, 'succeed'


def get_picture_info(img_id):
    _sql = 'SELECT image_name,image_path,image_type_id FROM ywg_genesis_image_info WHERE image_id=%s;'
    result = db_util(_sql, [img_id])
    if not result:
        return RET.PARAMERR, {}, '图片id错误'
    return RET.OK, result[0], 'succeed'


def get_picture_type_list(image_type_name, cur_page, page_size):
    _sql_records = 'SELECT COUNT(*) AS total_records FROM ywg_genesis_image_type'
    _sql_list = 'SELECT image_type_id,image_type_name FROM ywg_genesis_image_type'
    if image_type_name != 'all':
        _sql_records += ' WHERE image_type_name LIKE \'%%{}%%\''.format(image_type_name)
        _sql_list += ' WHERE image_type_name LIKE \'%%{}%%\''.format(image_type_name)
    _sql_list += ' ORDER BY image_type_id DESC LIMIT {},{};'.format(cur_page, page_size)
    _sql_records += ';'

    total_records = db_util(_sql_records)[0]['total_records']
    total_page = math.ceil(total_records / page_size) if total_records else 1
    detail = {
        'type_list': db_util(_sql_list),
        'total_page': total_page,
        'total_records': total_records
    }
    return RET.OK, detail, 'succeed'


def add_picture_type(image_type_name, user_id):
    _sql = 'INSERT INTO ywg_genesis_image_type (image_type_name,creator_id,add_date) VALUES (%s,%s,%s);'
    db_util(_sql, [image_type_name, user_id, gettime()])
    return RET.OK, {}, 'succeed'


def delete_picture_type(image_type_id):
    _sql = 'DELETE FROM ywg_genesis_image_type WHERE image_type_id=%s;'
    db_util(_sql, [image_type_id])
    return RET.OK, {}, 'succeed'


def update_picture_type(image_type_id, image_type_name):
    _sql = 'UPDATE ywg_genesis_image_type set image_type_name=%s,edit_date=%s WHERE image_type_id=%s;'
    db_util(_sql, [image_type_name, gettime(), image_type_id])
    return RET.OK, {}, 'succeed'


def get_picture_type_info(image_type_id):
    _sql = 'SELECT image_type_id,image_type_name FROM ywg_genesis_image_type WHERE image_type_id=%s;'
    result = db_util(_sql, [image_type_id])
    if result:
        return RET.OK, result[0], 'succeed'
    return RET.PARAMERR, {}, '图片id错误'


def get_picture_type_list_all():
    _sql = 'SELECT image_type_id,image_type_name FROM ywg_genesis_image_type;'
    return RET.OK, db_util(_sql), 'succeed'
