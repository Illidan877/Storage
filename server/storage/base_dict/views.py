import hashlib
import json
from django.core.paginator import Paginator, InvalidPage
from django.http import JsonResponse
from django.views import View
from base_dict.models import BaseType, Jurisdiction, Roles, Users
from common.LinqHelper import LinqHelper, logger


class BaseType_View(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method in ("POST", "DELETE", "PUT"):
            body = request.body
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
            tbody = json.loads(body)
            if (request.method in ("DELETE") and not tbody.get('id')) or (
                    request.method in ("POST") and not tbody.get('name')) or (
                    request.method in ("PUT") and not tbody.get('id')):
                return JsonResponse({'code': 500, 'error': "参数为空"})
            request.tbody = tbody
        if request.method in ("GET"):
            body = request.GET
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        pid = request.tbody.get('pid', -1)
        name = request.tbody.get('name')
        if LinqHelper.db_find(lambda: BaseType.objects.filter(pid=pid, name=name, is_active=True))[0] == 200:
            return JsonResponse({'code': 500, 'error': '这条数据已经存在，请不要重复添加'})
        code, data = LinqHelper.db_add(lambda: BaseType.objects.create(pid=pid, name=name))
        if code != 200:
            return JsonResponse({'code': code, 'error': data})
        return JsonResponse({'code': 200})

    def delete(self, request):
        id = request.tbody.get('id')
        code, data = LinqHelper.db_del(lambda: BaseType.objects.get(id=id, is_active=True))
        if code != 200:
            return JsonResponse({'code': code, 'error': data})
        return JsonResponse({'code': 200})

    def put(self, request):
        id = request.tbody.get('id')
        name = request.tbody.get('name')
        pid = request.tbody.get('pid')
        code, data_db = LinqHelper.db_find(lambda: BaseType.objects.filter(id=id, is_active=True))
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})
        type_obj = data_db[0]
        if name == type_obj.name and pid == type_obj.pid:
            return JsonResponse({'code': 500, 'error': "没有修改内容"})
        type_obj.name = name
        type_obj.pid = pid
        type_obj.save()
        return JsonResponse({'code': 200})

    def get(self, request):
        pid = request.GET.get('pid')
        page = request.GET.get('page')
        # 按类型查找
        if pid:
            func_db = lambda: BaseType.objects.filter(pid=pid, is_active=True)
        else:
            func_db = lambda: BaseType.objects.filter(is_active=True)
        code, data_db = LinqHelper.db_find(func_db)
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})
        # 分页格式化
        if page:
            data_format = {}
            data_db = list(data_db.values())
            data_paginator = Paginator(data_db, 10)
            code, data_page = LinqHelper.list_page(data_paginator, page)
            if code != 200:
                return JsonResponse({'code': code, 'error': data_page})
            data_format['pages'] = data_paginator.num_pages
            data_format['data'] = LinqHelper.list_format(data_page['data'],
                                                         {"name": "name", "pid": "pid", 'id': 'id'})
        else:
            data_format = LinqHelper.list_format(list(data_db.values()), {"name": "name", "pid": "pid", 'id': 'id'})
        return JsonResponse({'code': code, 'data': data_format})


class Jurisdiction_View(View):
    def dispatch(self, request, *args, **kwargs):
        body = request.body
        if request.method in ("DELETE", "PUT"):
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
            request.tbody = json.loads(body)
        elif request.method in ("GET"):
            body = request.GET
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
        else:
            return JsonResponse({'code': 500, 'error': "请求方式异常"})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        id = request.GET.get('id', 0)
        type = request.GET.get('type')
        pid = request.GET.get('pid')

        if type:
            type_que = BaseType.objects.filter(pid=type, is_active=True)
            types = []
            for i in type_que:
                types.append(i.id)

        if pid:
            func_db = lambda: Jurisdiction.objects.filter(pid=pid, is_active=True).order_by('order')
        elif id and type:
            func_db = lambda: Jurisdiction.objects.filter(id=id, type__in=types, is_active=True).order_by('order')
        elif id:
            func_db = lambda: Jurisdiction.objects.filter(id=id, is_active=True).order_by('order')
        elif type:
            func_db = lambda: Jurisdiction.objects.filter(type__in=types, is_active=True).order_by('order')
        else:
            return JsonResponse({'code': 400, 'data': '参数为空'})
        code, data_db = LinqHelper.db_find(func_db)
        print('\n' * 20)
        print(code, data_db)
        print(func_db)
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})
        res = []
        for i in data_db:
            res.append({
                'id': i.id,
                'pid': i.pid,
                'name': i.name,
                'type_id': i.type_id,
                'type': i.type.name,
                'order': i.order,
                'link': i.link,
                'params': i.params,
            })
        # data_format = LinqHelper.list_format(list(data_db.values()), {"name": "name", "pid": "pid"})
        return JsonResponse({'code': code, 'data': res})

    def put(self, request):
        jur = Jurisdiction.objects.filter(is_active=True)
        juris = {}
        for i in jur:
            juris[i.id] = i
        for i in json.loads(request.body):
            # 有则比对
            sign = self.get_sign(i)
            if i['id'] in juris:
                # 签名更改则更新数据
                if sign != juris[i['id']].sign:
                    juris[i['id']].name = i.get('name', "")
                    juris[i['id']].type_id = i.get('type_id')
                    juris[i['id']].link = i.get('link', "")
                    juris[i['id']].pid = i.get('pid')
                    juris[i['id']].sign = sign
                    juris[i['id']].order = i.get('order', 0)
                    juris[i['id']].params = i.get('params', "")
                    juris[i['id']].save()
                else:
                    pass
            else:
                Jurisdiction.objects.create(
                    id=i.get('id'),
                    pid=i.get('pid'),
                    name=i.get("name"),
                    type_id=i.get("type_id"),
                    order=i.get("order"),
                    link=i.get("link"),
                    params=i.get("params"),
                    sign=sign)
        return JsonResponse({'code': "200", 'data': '修改成功'})

    def delete(self, request):
        id = json.loads(request.body).get('id')
        if not id:
            return JsonResponse({'code': "400", 'error': "缺少id"})
        right = Jurisdiction.objects.get(id=id, is_active=True)
        right.delete()
        return JsonResponse({'code': "200", 'data': '删除成功'})

    def get_sign(self, data):
        hash = hashlib.md5()
        strall = ""
        for i in data.values():
            strall += str(i)
        hash.update(strall.encode())
        return hash.hexdigest()


class Roles_View(View):
    def dispatch(self, request, *args, **kwargs):
        body = request.body
        if request.method in ("DELETE", "PUT", "POST"):
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
            request.tbody = json.loads(body)
        elif request.method in ("GET"):
            body = request.GET
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
        else:
            return JsonResponse({'code': 500, 'error': "请求方式异常"})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        id = request.GET.get('id')
        if id:
            func_db = lambda: Roles.objects.filter(id=id, is_active=True)
        else:
            func_db = lambda: Roles.objects.filter(is_active=True)
        code, data_db = LinqHelper.db_find(func_db)
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})

        format = {"name": "name", "roleof": "roleof", 'id': 'id'}
        data_format = LinqHelper.list_format(list(data_db.values()), format)
        return JsonResponse({'code': code, 'data': data_format})

    def post(self, request):
        name = request.tbody.get('name')
        roleof = request.tbody.get('roleof', [])
        if not name:
            return JsonResponse({'code': 400, 'error': '角色名称为必填项'})
        if LinqHelper.db_find(lambda: Roles.objects.filter(name=name, roleof=roleof, is_active=True))[0] == 200:
            return JsonResponse({'code': 500, 'error': '这条数据已经存在，请不要重复添加'})
        code, data = LinqHelper.db_add(lambda: Roles.objects.create(name=name, roleof=roleof))
        if code != 200:
            return JsonResponse({'code': code, 'error': data})
        return JsonResponse({'code': 200})

    def put(self, request):
        id = request.tbody.get('id')
        name = request.tbody.get('name')
        roleof = request.tbody.get('roleof')
        roleof = [int(i) for i in json.loads(roleof)]
        if not roleof:
            return JsonResponse({'code': 400, 'error': '角色名称和角色权限为必填项'})
        # if LinqHelper.db_find(lambda: Roles.objects.filter(name=name, roleof=roleof, is_active=True)) == 200:
        #     return JsonResponse({'code': 500, 'error': '这条数据已经存在，请不重新修改'})

        code, data_db = LinqHelper.db_find(lambda: Roles.objects.filter(id=id, is_active=True))
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})
        type_obj = data_db[0]
        if name == type_obj.name and roleof == type_obj.roleof:
            return JsonResponse({'code': 500, 'error': "没有修改内容"})
        type_obj.roleof = roleof
        type_obj.save()
        return JsonResponse({'code': 200})

    def delete(self, request):
        id = request.tbody.get('id')
        code, data = LinqHelper.db_del(lambda: Roles.objects.get(id=id, is_active=True))
        if code != 200:
            return JsonResponse({'code': code, 'error': data})
        return JsonResponse({'code': 200})


class Users_View(View):
    def dispatch(self, request, *args, **kwargs):
        body = request.body
        if request.method in ("DELETE", "PUT", "POST"):
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
            request.tbody = json.loads(body)
        elif request.method in ("GET"):
            body = request.GET
            if body == b'':
                return JsonResponse({'code': 500, 'error': "参数为空"})
        else:
            return JsonResponse({'code': 500, 'error': "请求方式异常"})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        roles = request.GET.get('roles')
        page = request.GET.get('page')
        format_dict = {"name": "name", "password": "password", 'id': 'id', 'vname': 'vname', 'rolesto_id': 'rolesto_id'}
        # 按类型查找
        if not page and not roles:
            return JsonResponse({'code': 400, 'error': '缺少参数'})
        elif roles:
            func_db = lambda: Users.objects.filter(rolesto_id=roles, is_active=True)
        else:
            func_db = lambda: Users.objects.filter(is_active=True)
        print(roles)
        code, data_db = LinqHelper.db_find(func_db)
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})
        # 分页格式化
        if page:
            data_format = {}
            data_db = list(data_db.values())
            data_paginator = Paginator(data_db, 10)
            code, data_page = LinqHelper.list_page(data_paginator, page)
            if code != 200:
                return JsonResponse({'code': code, 'error': data_page})
            data_format['pages'] = data_paginator.num_pages
            data_format['current'] = page
            data_format['data'] = LinqHelper.list_format(data_page['data'], format_dict)
        else:
            data_format = LinqHelper.list_format(list(data_db.values()), format_dict)
        data_format['th'] = ["", '编号', '账号', '密码', '昵称', '角色']
        return JsonResponse({'code': code, 'data': data_format})

    def hash(self, str):
        hash = hashlib.sha256()
        hash.update((str + "son").encode())
        return hash.hexdigest()

    def post(self, request):
        name = request.tbody.get('name')
        password = request.tbody.get('password')
        vname = request.tbody.get('vname')
        name = request.tbody.get('name')
        if not name and not password:
            return JsonResponse({'code': 400, 'error': '缺少必填信息'})
        password = self.hash('123')
        if LinqHelper.db_find(lambda: Users.objects.filter(name=name, password=password))[0] == 200:
            return JsonResponse({'code': 500, 'error': '该用户已经注册'})
        code, data = LinqHelper.db_add(
            lambda: Users.objects.create(name=name, vname=vname, password=password, rolesto_id=42))
        if code != 200:
            return JsonResponse({'code': code, 'error': data})
        return JsonResponse({'code': 200})

    def delete(self, request):
        pass

    def put(self, request):
        id = request.tbody.get('id')
        if not id:
            return JsonResponse({'code': 400, 'error': '没有id'})
        password = request.tbody.get('password')
        vname = request.tbody.get('vname')
        name = request.tbody.get('name')
        rolesto_id = request.tbody.get('rolesto_id')
        if not password:
            return JsonResponse({'code': 400, 'error': '请输入有效密码'})
        password = self.hash(password)

        code, data_db = LinqHelper.db_find(lambda: Users.objects.filter(id=id, is_active=True))
        if code != 200:
            return JsonResponse({'code': code, 'error': data_db})
        type_obj = data_db[0]
        if password == type_obj.password:
            return JsonResponse({'code': 500, 'error': "没有修改内容"})
        type_obj.password = password
        type_obj.vname = vname
        type_obj.name = name
        type_obj.rolesto_id = rolesto_id
        type_obj.save()
        return JsonResponse({'code': 200})
