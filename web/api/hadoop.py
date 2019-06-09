#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-10 00:19
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import base64
import datetime
import hashlib
import logging
import os
import random
import string

from flask import Blueprint, request, make_response
from flask_jwt_extended import jwt_required, current_user

from service.hdfs_service import HDFSService
from web.result import Result

logger = logging.getLogger('api-hadoop')

hadoop = Blueprint('hadoop', __name__)


@hadoop.route('upload', methods=['POST'])
@jwt_required
def upload():
    print(request.files['picFile'].filename)
    file = request.files['picFile']
    if file:
        file_ext = get_file_ext(file.filename)
        file_category = set_type(file_ext)
        hdfs_path = datetime.date.today().strftime("/%Y/%m/%d/")
        hdfs_filename = get_hdfs_filename()
        user_id = current_user.id

        img_path = f"{hdfs_path}/{file_category}/{user_id}_{hdfs_filename}"

        # try:
        #     HDFSService().upload(path=img_path", data=file)
        # except Exception as err:
        #     logger.info(f'error: {err}')
        #     return Result.gen_failed(5000, msg='上传出现错误')

        data = base64.b64encode(file.stream.read()).decode('ascii')
        # print(data)
        return Result.gen_success(
            data={
                'base64': u"data:image/jpg;base64," + data,
                'img_path': img_path
            })

        # response = make_response(file.stream)
        # response.headers['Content-Type'] = 'image/jpg'
        # return response


@hadoop.route('download/<string:path>', methods=['GET'])
@jwt_required
def download(path):
    if path is not None and path != '':
        buf = HDFSService().download(path=path)
        filename = get_hdfs_filename()
        response = make_response(buf)
        try:
            response.headers.add('Content-Disposition', 'attachment', filename=filename.encode())
        except Exception as err:
            raise (err)
        return response


def get_md5(md5_str):
    md5 = hashlib.md5()
    md5.update(md5_str.encode('utf-8'))
    return md5.hexdigest()


def set_type(file_ext):
    DOCUMENTS = tuple('rtf odf ods gnumeric abw doc docx xls xlsx txt csv pdf'.split())
    IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())
    AUDIO = tuple('wav mp3 aac ogg oga flac'.split())
    VIDEO = tuple('avi rmvb rm divx mpg mpeg mpe wmv mp4 mkv vob'.split())
    if file_ext in DOCUMENTS:
        return 'doc'
    elif file_ext in IMAGES:
        return 'image'
    elif file_ext in AUDIO:
        return 'audio'
    elif file_ext in VIDEO:
        return 'video'
    else:
        return 'other'


def get_file_ext(filename):
    temp_name, file_ext = os.path.splitext(filename)
    return file_ext[1:]


def get_hdfs_filename():
    letter = string.ascii_letters + string.digits
    return ''.join(random.sample(letter, 10))
