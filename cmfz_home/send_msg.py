import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key  # 账户的唯一标识
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, mobile, code):
        param = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【毛信宇test】您的验证码是{code}".format(code=code)
        }
        req = requests.post(self.single_send_url, data=param)
