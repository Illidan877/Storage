import time

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from dict_con.models import BaseClass, BaseType


class DictConClass(View):
    def get(self, request):
        id = request.GET.get('id')
        type_name = request.GET.get('sname')

        if id:
            data = BaseClass.objects.filter(id=id).values()[0]
            return JsonResponse({'code': 200, 'data': dict(data)})
        else:
            if type_name:
                data = BaseClass.objects.filter(type_name__contains=type_name)
            else:
                data = BaseClass.objects.all()
            data = list(data.values())
            for i in data:
                i['created_time'] = i['created_time'].strftime("%Y年%m月%d日 %H:%M:%S")
            all_data = len(data)
            res = {'code': 200, 'data': data, "draw": 1, "recordsFiltered": all_data,
                   "recordsTotal": all_data, }
            return JsonResponse(res)

    def post(self, request):
        body = request.body
        if body is None:
            return JsonResponse({'code': 400, 'error': '参数为空'})
        body = json.loads(body)
        type_name = body.get('type_name')
        if type_name is None:
            return JsonResponse({'code': 400, 'error': '类型名称为空'})
        if type_name is None or type_name == "":
            res = {'code': 400,
                   'error': 'The local name for elements or attributes cannot be null or an empty string.'}
            return JsonResponse(res)
        try:
            old = BaseClass.objects.filter(type_name=type_name)
            if old.exists():
                res = {'code': 500, 'error': '这个类型名称已经存在'}
            else:
                BaseClass.objects.create(type_name=type_name, is_active=True)
                res = {'code': 200, 'data': '添加成功'}
        except Exception as e:
            res = {'code': 500, 'error': '数据库添加异常'}
        return JsonResponse(res)

    def put(self, request):
        body = request.body
        if body is None:
            return JsonResponse({'code': 400, 'error': '参数为空'})
        body = json.loads(body)
        id = body.get('id')
        type_name = body.get('type_name')
        created_time = body.get('created_time')
        is_active = body.get('is_active')
        old = BaseClass.objects.get(id=id)
        if old.type_name == type_name and old.created_time == created_time and old.is_active == is_active:
            return JsonResponse({'code': 400, 'error': '没有修改'})
        try:
            old.type_name = type_name
            old.created_time = created_time
            old.is_active = is_active
            old.save()
            res = {'code': 200, 'data': '修改成功'}

        except Exception as e:
            raise e
            res = {'code': 500, 'error': '数据修改异常'}
        return JsonResponse(res)

    def delete(self, request):
        body = request.body
        if body is None:
            return JsonResponse({'code': 400, 'error': '参数为空'})
        body = json.loads(body)
        id = body.get('id')
        if id is None or type(id) != list:
            return JsonResponse({'code': 400, 'error': '参数类型不正确'})
        try:
            old = BaseClass.objects.filter(id__in=id, is_active=True)
            if old.exists():
                old.delete()
                res = {'code': 200, 'error': '删除成功'}
            else:
                res = {'code': 400, 'error': '没有这个类型'}
        except Exception as e:
            res = {'code': 500, 'error': '数据修改异常'}
        return JsonResponse(res)








class DictConType(View):
    def get(self, request):
        id = request.GET.get('id')
        type_name = request.GET.get('sname')

        if id:
            data = BaseType.objects.filter(id=id).values()[0]
            return JsonResponse({'code': 200, 'data': dict(data)})
        else:
            if type_name:
                data = BaseType.objects.filter(type_name__contains=type_name)
            else:
                data = BaseType.objects.all()
            resp = []
            for i in data:
                resp.append({
                    'id': i.id,
                    'parent_class_type_id': i.parent_class_type.type_name,
                    'created_time': i.created_time.strftime("%Y年%m月%d日 %H:%M:%S"),
                    'updated_time': i.updated_time,
                    'type_name': i.type_name,
                    'parent_type': i.parent_type,

                })

            data = list(data.values())

            all_data = len(resp)
            res = {'code': 200, 'data': resp, "draw": 1, "recordsFiltered": all_data,
                   "recordsTotal": all_data, }
            return JsonResponse(res)

    def post(self, request):
        return JsonResponse({'data': 'qwe'})

    def put(self, request):
        return JsonResponse({'data': 'qwe'})

    def delete(self, request):
        return JsonResponse({'data': 'qwe'})







def dict_con(request):
    if request.method == "GET":
        return JsonResponse({'data': 'ok'})
    if request.method == "POST":
        return JsonResponse({'data': 'ok'})
    if request.method == "DELETE":
        return JsonResponse({'data': 'ok'})
    if request.method == "PUT":
        return JsonResponse({'data': 'ok'})
