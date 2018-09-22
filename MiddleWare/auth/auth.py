#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.utils.deprecation import MiddlewareMixin
from common.auth.userSystem import userSystem
from django.http import JsonResponse
from Hikarian.views import logout
'''

中间件：
    用来处理，用户访问权限以及用户的登陆状态

'''
class authenticationMiddleWare(MiddlewareMixin):

    # 判断登陆 权限控制
    def process_request(self,request):
        '''
        Request 预处理函数
        :param request:
        :return:
        '''
        # 错误信息
        context = ''
        print(request.path)
        # 限制访问url列表,需要权限或者处于登陆状态
        if 'xadmin' not in request.path \
                and ('user' in request.path \
                or 'order' in request.path \
                or 'refund' in request.path \
                or 'search' in request.path)\
                :
            print('进入验证')
            # 如果用户没有认证，限制访问
            if not request.session.has_key('sessionID') \
                    and not request.session.has_key('token'):

                # 用户不具有登陆认证口令
                context = 'Please login'
                return JsonResponse({
                    'status':202,
                    'message':context,
                })


            # 如果用户拥有口令，但口令过期
            elif request.session.has_key('sessionID') \
                    and request.session.has_key('token'):

                #用户拥有session，登陆验证
                user = userSystem(request)

                if not user.getUserObject():

                    #用户登出
                    logout(request)
                    context = 'your authentication exceed the time limit or you has logged in another place.'
                    return JsonResponse({
                        'status':202,
                        'message':context,
                    })
                    '''
                    
                    渲染模板
                    
                    '''

                '''
                权限管理
                pass
                '''

