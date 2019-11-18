import datetime
import hashlib
import re
import logging
from django.core.paginator import Paginator, InvalidPage

logger = logging.getLogger('log')

from django.http import HttpResponse, JsonResponse
from django.views import View

from users.models import TUser

from common.LinqHelper import *


class TUser_View(View):
    def get(self, request):
        uid = request.GET.get('id')
        page = request.GET.get('page')
        if uid:
            uid = int(uid)
            code, data = LinqHelper.db_find(lambda: TUser.objects.filter(id=uid))
            res = LinqHelper.res_format(code, data)
        elif page:
            if re.compile(r'\d').match(page):
                page = int(float(page))
            else:
                return JsonResponse({"code": 400, 'error': '无效页码1'})
            code, data = LinqHelper.db_find(lambda: Paginator(TUser.objects.filter(), 10))
            try:
                res = {}
                res['code'] = 200
                res['data'] = LinqHelper.res_format(code, data.page(page).object_list)['data']
                print('\n' * 20)
                print(res)
                res['pages'] = data.num_pages
                res['current'] = page

            except InvalidPage as e:
                logger.error('添加失败：{}'.format(e))
                return JsonResponse({"code": 400, 'error': '无效页码2'})
        return JsonResponse(res)

    def post(self, request):
        if request.body == b'':
            return JsonResponse({"code": 500, 'error': '请求体为空'})
        try:
            body = json.loads(request.body.decode())
        except Exception as e:
            return JsonResponse({"code": 500, 'error': '参数格式不正确'})

        phone = body.get('phone')
        phone = phone if isinstance(phone, str) else str(phone)
        password = body.get('pwd')
        vername = body.get('vname')
        if not phone and not password:
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
            TUser.objects.create(login_phone=phone, password=password, vername=vername)
        except Exception as e:
            logger.error('添加失败：{}'.format(e))
            return JsonResponse({"code": 500, 'error': '添加数据失败'})
        return JsonResponse({"code": 200})

    def delete(self, request):
        pass

    def put(self, request):
        pass
