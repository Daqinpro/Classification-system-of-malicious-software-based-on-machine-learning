import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from menus.models import MenuRoles, MenusSerializer, Menus
from roles.models import UserRoles
from users.models import User


class get_menus_view(View):
    def get(self,request):
        id=request.GET.get('id')
        user=User.objects.get(id=id)
        user_role=UserRoles.objects.get(user=user).role
        menus_id=MenuRoles.objects.filter(role=user_role).values('menu')
        # 根据关联菜单获id获取所有菜单且
        menus=Menus.objects.filter(id__in=menus_id,state=1)
        menus_data=MenusSerializer(menus,many=True)
        return JsonResponse({"code":200,"data":menus_data.data})
class get_menus_list_view(View):
    def get(self, request):
        page = request.GET.get('page')
        size = request.GET.get('size')
        menus = Menus.objects.all().order_by('id')  # 添加排序条件
        paginator = Paginator(menus, size)
        page_obj = paginator.page(page)
        page_obj = MenusSerializer(page_obj, many=True).data
        return JsonResponse({
            'code': 200,
            'msg': '获取成功',
            'data': page_obj,
            'total': paginator.num_pages,
        })

"""
更新
"""


class edit_menus_view(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            datas=data.get('form')
            menu_id = datas.get('id')
            new_name = datas.get('name')
            new_icon = datas.get('icon')
            new_state = datas.get('state')

            # 尝试获取菜单对象
            try:
                menu = Menus.objects.get(id=menu_id)
            except Menus.DoesNotExist:
                return JsonResponse({'code': 400, 'msg': '菜单不存在'})
            if menu_id == 6  or menu_id == 2 and new_state == 0:
                return JsonResponse({'code': 400, 'msg': '不能禁用此菜单'})
            # 更新菜单信息
            menu.name = new_name
            menu.icon = new_icon
            menu.state = new_state
            menu.save()
            return JsonResponse({'code': 200, 'msg': '编辑成功'})

        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': str(e)})