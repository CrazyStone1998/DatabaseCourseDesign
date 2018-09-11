from django.shortcuts import render
from django.views.decorators.cache import never_cache


# Create your views here.

@never_cache
def hasLoggedIn(request):
    '''
    判断用户是否在线的一个函数
    目前划不清楚用途
    :param request:
    :return:
    '''
    pass



def login(request):
    '''
    登陆函数
    :param request:
    :return:
    '''
    pass


def logout(request):
    '''
    账号 登出
    :param request:
    :return:
    '''
    # 清理缓存
    pass

def register(request):
    pass


def user_splitter(request,GET=None,POST=None):
    '''
    获取用户信息 分流器
    根据 request.method 分配方法
    GET:view.userGET
    POST:view.userPOST
    :param request:
    :return:
    '''
    # 错误信息列表
    error = ''
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    else:
        error = 'request.method is WRONG'

@never_cache
def userGET(request):
    '''
    显示用户信息
    :param request:
    :return:
    '''
    # 错误信息列表
    error = ''
    assert request.method == 'GET'
    pass


@never_cache
def userPOST(request):
    '''
    修改用户信息
    :param request:
    :return:
    '''
    # 错误信息列表
    error = ''
    assert request.method == 'POST'

def order(request):
    pass

def refund(request):
    pass

def search(request):
    pass