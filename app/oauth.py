import json
import base64
import hashlib

import requests
from Crypto.Cipher import AES


class MpCodeError(Exception):
    pass


class OAuth:
    def __init__(self):
        self.session = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(
            pool_connections=20, pool_maxsize=20, max_retries=3
        )
        self.session.mount("https://", self.adapter)
        self.session.mount("http://", self.adapter)

    # step 0
    def get_auth_page_url(self, app_id, redirect_url, **kwargs):
        raise NotImplementedError

    # callback step 1
    def get_access_token(self, app_id, app_secret, oauth_code):
        raise NotImplementedError

    # callback step 2
    def get_userinfo(self, data):
        """data: return value of get_access_token"""
        raise NotImplementedError

    # callback step 3
    def serialize_userinfo(self, userinfo):
        """
        userinfo: return value of get_userinfo
        return value: {
            'nickname': '',
            'gender': 0,
            'avatar_url': '',
            'provider_uid': '',
            'openid': '',  # only wechat
        }
        """
        raise NotImplementedError

    # handle error
    def valid_data(self, data):
        """data: return value of get_access_token"""
        raise NotImplementedError


class WechatMiniAppOAuth(OAuth):
    """
    小程序流程和OAuth类似，但是：
    1. 没有step 0，客户端调wx.login()
    2. 没有step 2，userinfo来自客户端
    3. union_id来自客户端（加密过），用session_key解开
    """

    def get_access_token(self, app_id, app_secret, oauth_code):
        """
        {
            "openid": "OPENID",
            "session_key": "SESSIONKEY",
            // 满足UnionID返回条件时
            "unionid": "UNIONID"
        }
        //错误时返回JSON数据包(示例为Code无效)
        {
            "errcode": 40029,
            "errmsg": "invalid code"
        }
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        res = self.session.get(
            url,
            params={
                "appid": app_id,
                "secret": app_secret,
                "js_code": oauth_code,
                "grant_type": "authorization_code",
            },
            timeout=1,
        )
        result = res.json()
        if result.get("errcode"):
            if result["errcode"] == 40163:  # code been used
                raise MpCodeError("授权信息已过期")
            if result["errcode"] == 40029:  # invalid code
                raise MpCodeError("微信授权code错误")
            if result["errcode"] == -1:  # system error
                raise MpCodeError("微信服务器错误")
            if result["errcode"] == 41008:
                raise MpCodeError("请求缺少code")
            raise MpCodeError(f"{result['errcode']}: {result['errmsg']}")
        return result

    def decrypt_userinfo(self, data, access_token):
        """
        data: 来自客户端，格式为
        {
            "encryptedData": "string",
            "iv": "string",
            "rawData": "string",
            "signature": "string",
            "userInfo": {}  // 这个和_decrypt返回值类似，缺union_id和open_id
        }
        access_token: `get_access_token`的返回值
        """
        if not access_token.get("session_key") or any(
            k not in data for k in ("encryptedData", "iv", "rawData", "signature")
        ):
            raise Exception(data.get("errMsg") or "微信小程序未返回数据")
        session_key = access_token["session_key"]
        encrypted_data = data["encryptedData"]
        iv = data["iv"]
        raw_data = data["rawData"]
        signature = data["signature"]

        userinfo = self._decrypt(encrypted_data, session_key, iv, raw_data, signature)
        return userinfo

    def _decrypt(self, encrypted_data, session_key, iv, raw_data, signature):
        """
        return: {
            "openId": "OPENID",
            "nickName": "NICKNAME",
            "gender": GENDER,
            "city": "CITY",
            "province": "PROVINCE",
            "country": "COUNTRY",
            "avatarUrl": "AVATARURL",
            "unionId": "UNIONID",
            "watermark": {
                "appid":"APPID",
                "timestamp":TIMESTAMP
            }
        }
        """
        # 安卓5.0、5.1用户在昵称里有系统不支持的emoji时，传过来的raw_data会
        # 乱码，这边校验会失败，但是数据是可以解开的。所以把校验去掉了。
        # sign = hashlib.sha1((raw_data + session_key).encode()).hexdigest()
        # if sign != signature:
        #     raise SignatureNotMatch(400, 'wrong signature')
        _session_key = session_key
        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)
        aes = AES.new(session_key, AES.MODE_CBC, iv)

        s = aes.decrypt(encrypted_data)
        s = s[: -ord(s[len(s) - 1 :])]
        s = s.decode("utf-8", "ignore")
        try:
            decrypted_data = json.loads(s)
        except json.JSONDecodeError as e:
            sign = hashlib.sha1((raw_data + _session_key).encode()).hexdigest()
            if sign != signature:
                raise Exception("微信数据校验失败")
            raise e
        return decrypted_data

    def serialize_userinfo(self, userinfo):
        """userinfo: `decrypt_userinfo`的返回值"""
        if any(k not in userinfo for k in ("nickName", "openId")):
            raise Exception(userinfo.get("error") or "微信未返回数据")
        return {
            "nickname": userinfo["nickName"],
            "gender": 1 if userinfo.get("gender") == 1 else 0,
            "avatar_url": userinfo.get("avatarUrl", ""),
            "provider_uid": userinfo.get("unionId", ""),
            "openid": userinfo["openId"],
            "city": userinfo.get("city", ""),
            "province": userinfo.get("province", ""),
            "country": userinfo.get("country", ""),
            "language": userinfo.get("language", ""),
        }

    def valid_data(self, data):
        if not data:
            raise Exception("小程序未返回数据")
        if data.get("errcode"):
            raise Exception(data["errmsg"])


oauth_client = WechatMiniAppOAuth()


if __name__ == "__main__":

    oauth_client = WechatMiniAppOAuth()
    app_secret = "b8d40e8f690561a5354d5b27b0868a7a"
    app_id = "wxaef2b1a656821b49"
    code = "061iC6v61NskUM12Gmu61N2iv61iC6vl"
    access_token = oauth_client.get_access_token(app_id, app_secret, code)
    print(access_token)
    # access_token = {'session_key': 'oLRQzlwRyQbbPmVjv1SWgg==', 'openid': 'oK9RO5XBIBRH4ZZhTmXZGa9TllWU'}
    data = {
        "errMsg": "getUserInfo:ok",
        "rawData": "{\"nickName\":\"shingo\",\"gender\":2,\"language\":\"zh_CN\",\"city\":\"Guangyuan\",\"province\":\"Sichuan\",\"country\":\"China\",\"avatarUrl\":\"https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo7NNgMjk79r99eayDSG4iaeJuxasLYg5GgnV2PkJic4Tvz06touMjyOlVYIiaIPTghuibvryjfqSKbGg/132\"}",
        "userInfo": {
            "nickName": "shingo",
            "gender": 2,
            "language": "zh_CN",
            "city": "Guangyuan",
            "province": "Sichuan",
            "country": "China",
            "avatarUrl": "https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo7NNgMjk79r99eayDSG4iaeJuxasLYg5GgnV2PkJic4Tvz06touMjyOlVYIiaIPTghuibvryjfqSKbGg/132"
        },
        "signature": "daa677265824177b32489bfea25d72717cef6c25",
        "encryptedData": "fsF/SMEmSKd93ruSnsKJZ+OfXfurmbh7hcp7GpbaLwPVe+Of/EodjpYL7LtVJKKrL7iET14BOJeVsYsfjXPOSRNdYp6u9hWAx/RKou0LHOECX911FsxNVOA7ksrrb5c/bkmh0FtkhpwwzypPqa+XCYyfkMBJP5LE7VnNOEBhYtNnWwVvDkK9KdlTB24NHedQmel9UAOt5GM3fgXVoQ/G6pcig6pO7Kbbh5d5F6yi3ROGmjl/cZya2BLmVGSSPddZ/UICCKQI/S7xROuDS9XR5NEXzPJoV40QBgqVteurPGL33KnKPpuefk3j8uCFuYV5r7/wA17h8Fm4tLY7ng1HVQB7+EEw8jqIasECqq7ZsiPyz9WPUre5uIBf3rVnS3xMPyrVPygWuRyBPNh9WL6IIQXicLTMbRwIOp8kawxmLdEI85VMgSrK8aEprb0dMUHsPgl5jRRM59FGUeFBAobnS6KU+9Vblop8EHk01rTxD+Y=",
        "iv": "YWRQ7qwx5tKSJjacmhMDqQ=="
    }
    userinfo = oauth_client.decrypt_userinfo(data, access_token)

    print(userinfo)
