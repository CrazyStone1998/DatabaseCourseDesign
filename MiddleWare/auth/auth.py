# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
#
# from django.utils.deprecation import MiddlewareMixin
# from common.auth.userSystem import userSystem
# from django.http import JsonResponse
# from weCheck.views import logout
# import re
#
# class authenticationMiddleWare(MiddlewareMixin):
#
#     # 判断登陆 权限控制
#     def process_request(self,request):
#         '''
#         Request 预处理函数
#         :param request:
#         :return:
#         '''
#         #错误信息
#         context = ''
#         if request.method == 'GET':
#             requestData = request.GET
#         else:
#             requestData = request.POST
#
#
#         if 'user' in request.path or 'group' in request.path or 'check' in request.path \
#             or 'schedule' in request.path or 'history' in request.path or 'record' in request.path:
#             # 如果用户没有认证，限制访问
#             if not request.session.has_key('sessionID') and not request.session.has_key('token') \
#                     and 'register' not in request.path and 'login' not in request.path:
#                 context = 'Please login'
#                 return JsonResponse({
#                     'status': 403,
#                     'message': context,
#                 })
#             elif request.session.has_key('sessionID') and request.session.has_key('token') \
#                     and 'register' not in request.path and 'logout' not in request.path \
#                     and 'login' not in request.path:
#                 try:
#
#                     #用户拥有session，登陆验证
#                     user = userSystem(request)
#                     if not user.getUserObject():
#                         #用户登出
#                         logout(request)
#
#                         context = 'your authentication exceed the time limit'
#                         return JsonResponse({
#                             'status': 403,
#                             'message': context,
#                         })
#                     '''
#
#                     权限管理
#
#                     pass
#
#
#                     '''
#                 except Exception as e:
#                     context = 'somthing is wrong'
#                     return JsonResponse({
#                         'status': 202,
#                         'message': context,
#                     })
#
