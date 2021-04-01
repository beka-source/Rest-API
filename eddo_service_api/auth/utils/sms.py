# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 下午1:22
# @Author  : Aydar
# @FileName: sms.py
# @Software: PyCharm
# @Telegram   ：aydardev

from random import choice

from flask_sqlalchemy import model

from eddo_service_api.auth.utils.sms_api import SMSC
from eddo_service_api.config import SEND_SMS_KZ
from eddo_service_api.models.mdl_verify_code import TblVerifyCode
from eddo_service_api.extensions import db

smsc = SMSC()


def generate_code():
    seeds = "1234567890"
    random_str = []
    for i in range(4):
        random_str.append(choice(seeds))
    return "".join(random_str)


def sen_mobile(mobile, send_type):
    code = generate_code()
    sms_content = SEND_SMS_KZ + str(code)
    mobile_content = "7" + mobile
    sms_status = smsc.send_sms(mobile_content, sms_content, sender="sms")
    verify_code = TblVerifyCode.query.filter_by(
        mobile=mobile,
        send_type=send_type
    ).order_by(TblVerifyCode.id.desc()).first()
    sum = 0
    if verify_code:
        sum = int(verify_code.sum_) + 1

    if sms_status[1] == '1':
        code_record = TblVerifyCode(
            mobile=mobile,
            code=code,
            send_type=send_type,
            sum_=sum
        )
        db.session.add(code_record)
        db.session.commit()
        return True
    else:
        return False


def send_simple_sms(mobile: str, sms: str) -> bool:
    sms_content = str(sms)
    mobile_content = "7" + (mobile[::-1][0:10])[::-1]
    sms_status = smsc.send_sms(mobile_content, sms_content, sender="sms")
    print(sms_status)
    if sms_status[1] == '1':
        return True
    else:
        return False
