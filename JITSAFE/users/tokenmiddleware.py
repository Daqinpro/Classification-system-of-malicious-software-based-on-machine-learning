from django.http import  JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
from rest_framework_jwt.settings import api_settings
import logging

logger = logging.getLogger(__name__)

class jwtAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        white_list = ["/user/login","/user/get_code","/user/register"]  # 请求白名单
        path = request.path
        if path not in white_list and not path.startswith("/media"):
            # 获取请求来的token
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                return JsonResponse({"code": 401, "msg": "Token未提供"})
            try:
                # 解析token
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return JsonResponse({"code": 401, "msg": "Token过期"})
            except InvalidTokenError:
                return JsonResponse({"code": 401, "msg": "Token验证失败"})
            except PyJWTError:
                return JsonResponse({"code": 401, "msg": "Token验证异常"})
        else:
            return None
