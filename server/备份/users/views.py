import datetime
import hashlib
import re
import logging
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse, JsonResponse
from django.views import View

from users.models import TUser, TRight, TRole

from common.LinqHelper import *

logger = logging.getLogger('log')


class QWE(View):
    # 处理业务
    def post(self):
        pass

    # 封装冗余
    def select_表名_功能名(self):
        pass


class TUser_View(View):
    def get(self, request):
        uid = request.GET.get('id')
        page = request.GET.get('page')
        if uid:
            uid = int(uid)
            code, data = LinqHelper.db_find(lambda: TUser.objects.filter(id=uid, is_active=True))
            res = LinqHelper.res_format(code, data)
        elif page:
            if re.compile(r'\d').match(page):
                page = int(float(page))
            else:
                return JsonResponse({"code": 400, 'error': '无效页码1'})
            code, data = LinqHelper.db_find(lambda: Paginator(TUser.objects.filter(is_active=True), 10))
            try:
                res = {}
                res['code'] = 200
                res['data'] = LinqHelper.res_format(code, data.page(page).object_list)['data']
                res['pages'] = data.num_pages
                res['current'] = page
            except InvalidPage as e:
                logger.error('查询失败：{}'.format(e))
                return JsonResponse({"code": 400, 'error': '无效页码2'})
            res['header'] = {f.name: f.verbose_name for f in TUser._meta.fields}
        return JsonResponse(res)

    def post(self, request):
        if request.body == b'':
            return JsonResponse({"code": 500, 'error': '请求体为空'})
        try:
            body = json.loads(request.body.decode())
        except Exception as e:
            return JsonResponse({"code": 500, 'error': '参数格式不正确'})

        phone = body.get('lname')

        phone = phone if isinstance(phone, str) else str(phone)
        password = body.get('pwd')
        vername = body.get('vname')
        tRole_id = body.get('type')

        if not phone or not password or not tRole_id:
            return JsonResponse({"code": 500, 'error': '请将信息完善'})
        # if not re.match(r"^1[35678]\d{9}$", phone):
        #     return JsonResponse({"code": 500, 'error': '请输入有效的手机号码'})
        code, res = LinqHelper.db_find(lambda: TUser.objects.filter(login_phone=phone))
        if code == 200 and len(res) > 0:
            return JsonResponse({"code": 500, 'error': '该手机号已经被注册'})
        vername = vername if vername else phone
        hash = hashlib.sha256('898oaFs09f'.encode('utf8'))
        hash.update(password.encode())
        password = hash.hexdigest()
        try:
            TUser.objects.create(login_phone=phone,
                                 password=password,
                                 vername=vername,
                                 tRole_id=tRole_id,
                                 count=0,
                                 is_active=True)
        except Exception as e:
            logger.error('添加失败：{}'.format(e))
            return JsonResponse({"code": 500, 'error': '添加数据失败'})
        return JsonResponse({"code": 200})

    def delete(self, request):

        if request.body == b'':
            return JsonResponse({"code": 500, 'error': '请求体为空'})
        try:
            body = json.loads(request.body.decode())
        except Exception as e:
            return JsonResponse({"code": 500, 'error': '参数格式不正确'})

        uids = body.get('uids')
        try:
            users = TUser.objects.filter(id__in=uids, is_active=True)
            for user in users:
                user.is_active = False
                user.save()
        except Exception as e:
            logger.error('删除异常：{}'.format(e))
            return JsonResponse({"code": 500, 'error': '删除异常'})
        return JsonResponse({'code': 200})

    def put(self, request):
        pass


class TRole_View(View):
    def get(self, request):
        uid = request.GET.get('id')
        page = request.GET.get('page')
        if uid:
            uid = int(uid)
            code, data = LinqHelper.db_find(lambda: TRole.objects.filter(id=uid, is_active=True))
            res = LinqHelper.res_format(code, data)
        elif page:
            if re.compile(r'\d').match(page):
                page = int(float(page))
            else:
                return JsonResponse({"code": 400, 'error': '无效页码1'})
            code, data = LinqHelper.db_find(lambda: Paginator(TRole.objects.filter(is_active=True), 10))
            try:
                res = {}
                res['code'] = 200
                res['data'] = LinqHelper.res_format(code, data.page(page).object_list)['data']
                res['pages'] = data.num_pages
                res['current'] = page
            except InvalidPage as e:
                logger.error('查询失败：{}'.format(e))
                return JsonResponse({"code": 400, 'error': '无效页码2'})
        return JsonResponse(res)


class TRight_View(View):
    def get(self, request):
        type = request.GET.get('type')
        page = request.GET.get('page')
        iid = request.GET.get('iid')
        id = request.GET.get('id')
        type_list = request.GET.get('type_list')

        if id:
            data = list(TRight.objects.filter(is_active=True).order_by('order').values())
            res = LinqHelper.list_to_relationlist(data, int(id))
        elif iid:
            data = TRight.objects.filter(is_active=True, id=iid).order_by('order')
            res = list(data.values())

        elif type_list:
            res = list(TRight.objects.filter(type_id=type_list).order_by('order').values())
        elif page:
            if re.compile(r'\d').match(page):
                page = int(float(page))
            else:
                return JsonResponse({"code": 400, 'error': '无效页码1'})
            if type:
                sql = TRight.objects.filter(is_active=True, type_id=type)
            else:
                sql = TRight.objects.filter(is_active=True)
            code, data = LinqHelper.db_find(lambda: Paginator(sql, 10))
            try:
                res = {}
                res['code'] = 200
                res['data'] = LinqHelper.res_format(code, data.page(page).object_list)['data']
                res['pages'] = data.num_pages
                res['current'] = page
            except InvalidPage as e:
                logger.error('查询失败：{}'.format(e))
                return JsonResponse({"code": 400, 'error': '无效页码2'})
            res['header'] = {f.name: f.verbose_name for f in TRight._meta.fields}
            return JsonResponse(res)

        elif type:
            data = list(TRight.objects.filter(type_id=type, is_active=True).order_by('order').values())
            if not id:
                id = 0
            res = LinqHelper.list_to_tree(data, id, lambda m: m['type_id'] == int(type))
        else:
            data = list(TRight.objects.filter(is_active=True).order_by('order').values())
            res = data

        return JsonResponse({'code': 200, 'data': res})

    def put(self, request):
        old = TRight.objects.filter(is_active=True)
        old_dic = {}
        for i in old:
            old_dic[i.id] = i

        for i in json.loads(request.body):
            # 有则比对
            sign = get_sign(i)
            if i['id'] in old_dic:
                # 签名更改则更新数据
                if sign != old_dic[i['id']].sign:
                    print('\n' * 50)
                    print(i)

                    print(old_dic[i['id']].type_id, i.get('type_id'))
                    print(i.get('right_name'))
                    old_dic[i['id']].right_name = i.get('right_name')
                    old_dic[i['id']].type_id = i.get('type_id')
                    old_dic[i['id']].link = i.get('link')
                    old_dic[i['id']].parent = i.get('parent')
                    old_dic[i['id']].sign = sign
                    old_dic[i['id']].order = i.get('order')
                    old_dic[i['id']].params = i.get('params')
                    old_dic[i['id']].save()
                else:
                    pass
            else:
                TRight.objects.create(id=i['id'], parent=i['parent'],
                                      right_name=i['right_name'],
                                      type_id=i['type_id'],
                                      link=i['link'],
                                      order=i['order'],
                                      params=i['params'],
                                      sign=sign)

        return JsonResponse({'code': "200", 'data': '修改成功'})

    def delete(self, request):
        id = json.loads(request.body).get('id')
        right = TRight.objects.get(id=id)
        right.delete()
        return JsonResponse({'code': "200", 'data': '删除成功'})


def get_sign(obj):
    hash = hashlib.md5()
    strall = ""
    for i in obj.values():
        strall += str(i)
    hash.update(strall.encode())
    return hash.hexdigest()
