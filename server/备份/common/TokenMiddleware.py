from django.utils.deprecation import MiddlewareMixin

class token(MiddlewareMixin):
    # 到达主路由之前
    def process_request(self, request):
        return None

    # 响应给浏览器之前
    def process_response(self, request, response):
        return response
