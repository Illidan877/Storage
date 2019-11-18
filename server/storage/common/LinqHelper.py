import datetime
import json
import logging

logger = logging.getLogger('log')


class LinqHelper:
    @staticmethod
    def res_format(int_code, list_msg):
        '''格式化返回结果

        :param int_code: 状态码
        :param list_msg: 请求结果 或 异常信息
        :return: dist
        '''
        dict_format = {
            'created_time': 'ctime',
            'updated_time': 'utime',
            'login_phone': 'lname',
            'vername': 'vname',
            'password': 'pwd',
        }
        if int_code == 200:
            list_formatmsg = []
            for model_itme in list(list_msg.values()):
                itme = {}
                for key, value in model_itme.items():
                    format_key = dict_format[key] if key in dict_format else key
                    if isinstance(value, datetime.datetime):
                        value = value.strftime('%Y:%m:%d %H:%M:%S')
                    itme[format_key] = value
                list_formatmsg.append(itme)
            if len(list_formatmsg) == 1:
                list_formatmsg = list_formatmsg[0]
            list_msg = list_formatmsg
        res_data = {'code': int_code, 'data': list_msg} if int_code == 200 else {'code': int_code, 'error': list_msg}

        return res_data

    @staticmethod
    def db_find(orm_script):
        '''捕获数据库查询异常

        :param orm: 查询语句:
        :return: (code,msg)
        '''
        try:
            queryset_res = orm_script()
            if not queryset_res:
                return (400, '没有找到数据')
            else:
                return (200, queryset_res)
        except Exception as e:
            logger.error('请求出错：{}'.format(e))
            return (500, '查找失败')

    # ----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def find_min(iterable_case, func_condition):
        '''
        返回可迭代对象中的最小值
        :param iterable_case:可迭代对象
        :param func_condition:条件
        :return:最小值对象
        '''
        min_value = iterable_case[0]
        for item in range(1, len(iterable_case)):
            if func_condition(min_value) > func_condition(iterable_case[item]):
                min_value = iterable_case[item]
        return min_value

    @staticmethod
    def delete_node(iterable_case, func_condition):
        '''
        根据条件删除可迭代对象中的元素
        :param iterable_case:可迭代对象
        :param func_condition:条件
        :return:None
        '''
        for item in range(len(iterable_case) - 1, -1, -1):
            if func_condition(iterable_case[item]):
                del iterable_case[item]

    @staticmethod
    def order_by_fall(iterable_case, func_condition):
        '''
        降序排列
        :param iterable_case:可迭代对象
        :param func_condition:条件
        :return:None
        '''
        for r in range(len(iterable_case) - 1):
            for c in range(r + 1, len(iterable_case)):
                if func_condition(iterable_case[r]) < func_condition(iterable_case[c]):
                    iterable_case[r], iterable_case[c] = iterable_case[c], iterable_case[r]
