#file:D:\pythonDemo\JITSAFE\users\views.py
import hashlib

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
import json
from rest_framework_jwt.settings import api_settings

from roles.models import UserRoles, Roles
from .models import User, UserSerializer, Enroll
import random
import string  # 导入 string 模块
from django.core.mail import send_mail

"""
登录
"""
class login_view(View):
    def post(self, request):
        try:
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body.decode('utf-8'))
            # 获取用户名和密码
            username = data.get('username')
            password = data.get('password')
            # 查看用户是否存在
            check_username = User.objects.filter(username=username).exists()
            if check_username is False:
                return JsonResponse({'code': 450, 'msg': '账号未注册'})
            # 检查用户名和密码是否匹配
            check_user = User.objects.filter(username=username, password=password).exists()
            if check_user:
                user = User.objects.get(username=username, password=password)
                # 查看状态是否启用
                if user.state == 0:
                    return JsonResponse({'code': 400, 'msg': '用户已停用'})
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                # 将用户对象传进去获得对象属性
                payload = jwt_payload_handler(user)
                # 生成字符串 token
                token = jwt_encode_handler(payload)
                # 使用序列化器将用户对象序列化
                serializer = UserSerializer(user)
                user_data = serializer.data
                 # 更新登录时间
                return JsonResponse({'code': 200, 'msg': '登录成功', 'token': token, 'user': user_data})
            else:
                return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})

"""
获取验证码
"""
class get_code_view(View):
    def post(self, request):
        try:
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            # 判断是否存在
            check_user = User.objects.filter(username=username).exists()
            if check_user:
                return JsonResponse({'code': 400, 'msg': '账号已存在'})
            captcha = "".join(random.sample(string.digits, 4))

            send_mail(
                '恶意软件分类深度学习系统登录验证码',
                '您的验证码是：' + captcha,
                None,
                [username],
            )

        # 创建或者更新验证码
            Enroll.objects.update_or_create(email=username, defaults={'code': captcha})
            return JsonResponse({'code': 200, 'msg': '验证码发送成功'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
注册
"""
class register_view(View):
    def post(self, request):
        try:
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body.decode('utf-8'))
            # 获取用户名和密码
            username = data.get('username')
            password = data.get('password')
            # 验证码
            code = data.get('auth_code')
            # 验证码
            enroll = Enroll.objects.filter(email=username).first()
            if enroll and enroll.code == code:
                # 验证码正确，创建用户
                user=User.objects.create(username=username, password=password,state=1)
                UserRoles.objects.create(role=Roles.objects.get(id=1),user=user)
                return JsonResponse({'code': 200, 'msg': '注册成功'})
            else:
                return JsonResponse({'code': 400, 'msg': '验证码错误'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
获取所有用户账号
"""
class getUserView(View):
    def get(self, request):
        page_number = request.GET.get('page', 1)  # 获取页码，默认为1
        page_size = request.GET.get('size', 10)  # 获取每页大小，默认为10
        username = request.GET.get('username')
        id=request.GET.get('id')
        # 排除id的用户
        user_id=User.objects.filter(id=id).first()
        users=User.objects.exclude(id=user_id.id).order_by('id')
        try:
            if username:
                user = users.filter(username__icontains=username)
            else:
                user = users.all()
            data=[]
            for user_id in user:
                role=UserRoles.objects.filter(user=user_id).first()
                data_dict={
                    'id': user_id.id,
                    'username': user_id.username,
                    'role':role.role.id,
                    'state':user_id.state
                }
                data.append(data_dict)
            paginator = Paginator(data, page_size)
            page_obj = paginator.get_page(page_number)
            page_obj = list(page_obj)
            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': page_obj,
                'total': paginator.num_pages,
            })
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
添加
"""
class addUserView(View):
    def post(self, request):
        try:
            datas = json.loads(request.body.decode('utf-8'))
            data= datas.get('form')
            username = data.get('username')
            password = data.get('password')
            role = data.get('role')
            state = data.get('state')
            if User.objects.filter(username=username).exists():
                return JsonResponse({'code': 400, 'msg': '账号已存在'})
            User.objects.create(username=username, password=password,state=state)
            UserRoles.objects.create(role=Roles.objects.get(id=role), user=User.objects.get(username=username))
            return JsonResponse({'code': 200, 'msg': '添加成功'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
编辑用户
"""
class editUserView(View):
    def post(self, request):
        try:
            datas = json.loads(request.body.decode('utf-8'))
            data= datas.get('form')
            id=data.get('id')
            state = data.get('state')
            role=data.get('role')
            UserRoles.objects.filter(user=User.objects.get(id=id)).update(role=Roles.objects.get(id=role))
            User.objects.filter(id=id).update(state=state)
            return JsonResponse({'code': 200, 'msg': '修改成功'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
删除账号
"""
class deleteUserView(View):
    def post(self, request):
        try:
            datas = json.loads(request.body.decode('utf-8'))
            id = datas.get('id')
            User.objects.filter(id=id).delete()
            return JsonResponse({'code': 200, 'msg': '删除成功'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
# 密码重置
# """
class resetPasswordView(View):
    def post(self, request):
        try:
            datas = json.loads(request.body.decode('utf-8'))
            id = datas.get('id')
            print(id)
            password = '123456'
            # 创建md5对象
            md5 = hashlib.md5()
            # 更新md5对象，注意要转码为utf-8
            md5.update(password.encode('utf-8'))
            # 获取加密后的结果，返回的是字节串，通常我们会将其转换成十六进制字符串表示
            md5_password = md5.hexdigest()
            User.objects.filter(id=id).update(password=md5_password)
            return JsonResponse({'code': 200, 'msg': '重置成功！重置密码为123456'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': str(e)})
"""
修改密码
"""
class changePasswordView(View):
    def post(self, request):
        try:
            datas = json.loads(request.body.decode('utf-8'))
            id=datas.get('id')
            oldPassword=datas.get('oldpassword')
            newPassword=datas.get('newpassword')
            user=User.objects.get(id=id)
            if user.password==oldPassword:
                User.objects.filter(id=id).update(password=newPassword)
                return JsonResponse({'code': 200, 'msg': '修改成功'})
            else:
                return JsonResponse({'code': 400, 'msg': '旧密码错误'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})