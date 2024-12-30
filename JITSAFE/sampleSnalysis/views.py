import concurrent.futures
import hashlib
import uuid
import pandas as pd
from django.core.paginator import Paginator
from django.db import transaction
from django.views import View
import os
from django.conf import settings
from sampleSnalysis.models import UserFiles, UserFilesSerializer, UserModel, UserModelDataId, UserModelResult, \
    UserModelSerializer, UserModelResultSerializer, UserModelDataIdSerializer
from users.models import User
from django.http import JsonResponse
import joblib
import numpy as np
import json
"""
随机字符串
"""
def get_random_str():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()

class UploadExcelView(View):
    def post(self, request):
        uploaded_excel = request.FILES.get('excel')
        name = request.POST.get("name")
        id = request.POST.get("id")
        user = User.objects.get(id=id)
        if not uploaded_excel:
            return JsonResponse({
                "code": 500,
                "msg": "请上传文件"
            })
        if not name:
            return JsonResponse({
                "code": 500,
                "msg": "请输入备注"
            })
        new_name = get_random_str()
        file_path = os.path.join(settings.MEDIA_ROOT, 'sampleFiles', new_name + os.path.splitext(uploaded_excel.name)[1])
        try:
            # 使用多线程处理文件保存
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(save_file, uploaded_excel, file_path)
            # 将file_path解析成xxxx.xlsx
            relative_path = os.path.relpath(file_path, os.path.join(settings.MEDIA_ROOT, 'sampleFiles'))
            UserFiles.objects.create(name=name, url=relative_path, user=user, path=file_path)
            clear_files()
            return JsonResponse({"code": 200, "msg": "上传成功"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, "msg": "上传失败"})
def save_file(uploaded_excel, file_path):
    # 增大chunk size以减少读写次数
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_excel.chunks(chunk_size=8192):
            destination.write(chunk)
"""
自动清理非数据库中的文件
"""
def clear_files():
    file_list = os.listdir(os.path.join(settings.MEDIA_ROOT, 'sampleFiles'))
    for file in file_list:
        if not UserFiles.objects.filter(path=os.path.join(settings.MEDIA_ROOT, 'sampleFiles', file)).exists():
            os.remove(os.path.join(settings.MEDIA_ROOT, 'sampleFiles', file))
"""
获取数据
"""
class GetFilesView(View):
    def get(self, request):
        id = request.GET.get("id")
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('size', 10)
        user = User.objects.get(id=id)
        data_list=UserFiles.objects.filter(user=user)
        #序列化
        serializer_data = UserFilesSerializer(data_list, many=True).data
        paginator = Paginator(serializer_data, page_size)
        page_obj = paginator.get_page(page_number)
        return JsonResponse({
            "code": 200,
            "msg": "获取成功",
            "data": list(page_obj.object_list),
            "total": paginator.count,
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
        })
"""
删除
"""
class DeleteFileView(View):
    def post(self, request):
        data=json.loads(request.body.decode('utf-8'))
        id=data.get("id")
        user_file = UserFiles.objects.get(id=id)
        user_file.delete()
        clear_files()
        return JsonResponse({"code": 200, "msg": "删除成功"})
"""
分析模型
"""
# 在类外部加载模型
model = joblib.load('sampleSnalysis/trained_model.joblib')

class AnalysisModelView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            file_id = data.get("file_id")
            user_file = UserFiles.objects.get(id=file_id)
            user = User.objects.get(id=id)
            # 判断模型是否存在
            check_UserModel=UserModel.objects.filter(user=user, UserFile=user_file).exists()
            if check_UserModel:
                data=UserModel.objects.get(user=user, UserFile=user_file)
                datas=UserModelSerializer(data).data
                return JsonResponse({"code": 200, "msg": "分析成功", "data": datas})
            path = user_file.path
            _, file_extension = os.path.splitext(path.lower())

            if file_extension == '.csv':
                datas = pd.read_csv(path)
            elif file_extension in ['.xlsx', '.xls']:
                datas = pd.read_excel(path, engine='openpyxl')
            else:
                return JsonResponse({"code": 400, "msg": "不支持的文件格式"})

            if datas.empty:
                return JsonResponse({"code": 400, "msg": "文件内容为空"})

            malware_counts = {malware: 0 for malware in ["Ramnit", "Lollipop2", "Kelihos_ver3", "Vundo", "Simda", "Tracur", "Kelihos_ver1", "Obfuscator.ACY", "Gatak"]}
            results = []

            for index, row in datas.iterrows():
                result = predictModel(row[1:].tolist(), model)
                results.append({
                    "file_id": row.iloc[0],
                    "result": result
                })
                for malware, count in result.items():
                    malware_counts[malware] += count

            with transaction.atomic():
                usermodel = UserModel.objects.create(
                    user=user,
                    UserFile=user_file,
                    Ramnit=malware_counts["Ramnit"],
                    Lollipop2=malware_counts["Lollipop2"],
                    Kelihos_ver3=malware_counts["Kelihos_ver3"],
                    Vundo=malware_counts["Vundo"],
                    Simda=malware_counts["Simda"],
                    Tracur=malware_counts["Tracur"],
                    Kelihos_ver1=malware_counts["Kelihos_ver1"],
                    Obfuscator_ACY=malware_counts["Obfuscator.ACY"],
                    Gatak=malware_counts["Gatak"]
                )

                for result in results:
                    usermodeldataid = UserModelDataId.objects.create(
                        usermodel=usermodel,
                        file_id=result["file_id"]
                    )
                    UserModelResult.objects.create(
                        usermodeldataid=usermodeldataid,
                        Ramnit=result["result"]["Ramnit"],
                        Lollipop2=result["result"]["Lollipop2"],
                        Kelihos_ver3=result["result"]["Kelihos_ver3"],
                        Vundo=result["result"]["Vundo"],
                        Simda=result["result"]["Simda"],
                        Tracur=result["result"]["Tracur"],
                        Kelihos_ver1=result["result"]["Kelihos_ver1"],
                        Obfuscator_ACY=result["result"]["Obfuscator.ACY"],
                        Gatak=result["result"]["Gatak"]
                    )

            return JsonResponse({"code": 200, "msg": "分析成功", "data": malware_counts})

        except Exception as e:
            return JsonResponse({"code": 500, "msg": f"分析失败: {str(e)}"})


def predictModel(datas, model):
    features = np.array(datas).reshape(1, -1)
    prediction = model.predict(features)
    malware_names = ["Ramnit", "Lollipop2", "Kelihos_ver3", "Vundo", "Simda", "Tracur", "Kelihos_ver1", "Obfuscator.ACY", "Gatak"]
    result_dict = {malware_names[i]: int(prediction[0][i]) for i in range(len(malware_names))}
    return result_dict
"""
修改备注
"""
class ChangeRemarksView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        id = data.get("id")
        name = data.get("name")
        user_file = UserFiles.objects.get(id=id)
        user_file.name = name
        user_file.save()
        return JsonResponse({"code": 200, "msg": "修改成功"})
"""
历史模型获取查询
"""
class HistoryModelView(View):
    def get(self, request):
        remark = request.GET.get("remark", "").strip()  # 去除首尾空格
        id = request.GET.get("id")
        page = int(request.GET.get("page", 1))
        size = int(request.GET.get("size", 10))

        try:
            user = User.objects.get(id=id)
            user_files = UserFiles.objects.filter(user=user, name__icontains=remark).order_by('-id')
            user_models = UserModel.objects.filter(UserFile__in=user_files).order_by('-id')
            user_model_data_ids = UserModelDataId.objects.filter(usermodel__in=user_models).order_by('-id')
            user_model_results = UserModelResult.objects.filter(usermodeldataid__in=user_model_data_ids).order_by('-id')

            # 分页处理
            paginator = Paginator(user_model_results, size)
            page_obj = paginator.get_page(page)

            # 构建返回数据
            result_data = []
            for result in page_obj.object_list:
                user_model_data_id = result.usermodeldataid
                user_model = user_model_data_id.usermodel
                user_file = user_model.UserFile

                data = {
                    "id": user_file.id,
                    "name": user_file.name,
                    "file_id": user_model_data_id.file_id,
                    "Ramnit": result.Ramnit,
                    "Lollipop2": result.Lollipop2,
                    "Kelihos_ver3": result.Kelihos_ver3,
                    "Vundo": result.Vundo,
                    "Simda": result.Simda,
                    "Tracur": result.Tracur,
                    "Kelihos_ver1": result.Kelihos_ver1,
                    "Obfuscator_ACY": result.Obfuscator_ACY,
                    "Gatak": result.Gatak
                }
                result_data.append(data)

            return JsonResponse({
                "code": 200,
                "msg": "查询成功",
                "data": result_data,
                "total": paginator.count,
                "pages": paginator.num_pages,
                "current_page": page_obj.number
            })

        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, "msg": f"查询失败: {str(e)}"})








