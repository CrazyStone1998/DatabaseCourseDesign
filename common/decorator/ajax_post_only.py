# coding=utf-8

from django.http import JsonResponse

def ajax_post_only(func):
    '''
    装饰器
    过滤掉非ajax post请求

    :param func:
    :return:
    '''
    def wrapper(request,*args,**kwargs):
        error = []
        if request.method == 'POST':
            return func(request,*args,**kwargs)
        else:
            error.append('request.method is not POST')
            return JsonResponse({
                'status':202,
                'message':error,
            })
    return wrapper
