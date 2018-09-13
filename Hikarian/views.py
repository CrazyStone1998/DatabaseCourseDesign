from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from common.auth.userSystem import userSystem,makepassword,checkpassword
from django.http import JsonResponse
from django.db.models import F,Q
from Hikarian.common import affair

# Create your tests here.
import hashlib
import time
from Hikarian import models

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
    # 判断request.method
    if request.method == 'GET':
        # 重定向到 登陆界面
        return redirect('/api/v1/login/')

    elif request.method == 'POST':

        # 获取用户 账户 和 密码
        user_id = request.POST.get('user_id')
        passwd = request.POST.get('passwd')
        # 获取user对象
        user = userSystem(request)
        # user登陆 认证
        # 判定新用户登陆 顶替旧的用户
        if user.getUsername() != user_id:
            user.delCache()
            # 清理 session
            request.session.flush()

        error = user.authentication(user_id=user_id, passwd=passwd)
        # error为空 则登陆成功
        # error不为空 则登陆不成功
        if not error:
            return JsonResponse({
                'status': 200,
                'message': 'OK',
                'data': {
                }

            })
        else:
            return JsonResponse({
                'status': 202,
                'message': error,
                'data': {
                }
            })


def logout(request):
    '''
    账号 登出
    :param request:
    :return:
    '''
    # 清理缓存
    pass

def register(request):

    # 错误信息列表
    error = ''

    # 后台获取并判断用户名和密码 是否为空
    user_id = request.POST.get('user_id')
    passwd = request.POST.get('passwd')

    # 正则判断 账号密码等正则信息
    if user_id is None or passwd is None:
        error = 'The user_id & passwd cannot be empty'
        # 获取并判断 用户名是否存在
    else:
        if not models.userInfo.objects.filter(Q(user_id=user_id) & Q(is_Delete=False)).exists():
            passwd = makepassword(user_id,passwd)
            user_name = request.POST.get('user_name')
            id_num = request.POST.get('id_num')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            # 调用 model类的 新建对象方法 存储用户对象
            models.userInfo.userInfoObject(user_id,passwd,user_name,id_num,email,phone)
            # 返回 json
            return JsonResponse({
                'status': 200,
                'message': 'OK',
            })
        else:
                error = 'Username already exists'

    return JsonResponse({
        'status': 202,
        'message': error,
    })


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
    # 获取用户对象
    user_id = request.GET.get('user_id')
    if user_id:
        user = models.userInfo.objects.get_or_none(user_id=user_id)
    else:
        user = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUsername())

    if user is not None:

        return JsonResponse({

            'status': 200,
            'message': 'SUCCESS',
            'data': {
                'user_id': user.user_id,
                'user_name': user.user_name,
                'id_num': user.id_num,
                'email': user.email,
                'phone':user.phone,

            }
        })
    else:
        error = 'user is not exist'
        return JsonResponse({
            'status': 202,
            'message': error
        })


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

    user = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUsername())

    if user:
        user.user_name = request.POST.get('user_name', user.user_name)
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        user.id_num = request.POST.get('id_num', user.id_num)
    else:
        error = 'user is not exist.'
        return JsonResponse(
            {
                'status': 202,
                'message': error,
            }
        )

    # 保存 修改
    user.save()

    return JsonResponse({
        'status': 200,
        'message': 'SUCCESS'
    })


def order(request):

    error = ''

    if request.method == 'GET':
        return redirect('/api/v1/order')
    elif request.method == 'POST':

        startstation = request.POST.get('startstation')
        endstation = request.POST.get('endstation')

        date = request.POST.get('date')

        if startstation and endstation and date:
            # 直达方式 余票
            for everytrain in affair.searchTrain_Direct(startstation, endstation):

                carriageArray = affair.searchTrainCarriage(everytrain.train_id)
                stationArray = affair.searchTrainStation(everytrain.train_id)
                # 计算每一个车厢的余票

                #初始化 座次-车站 矩阵

                # matrix = [[0]for _ in range(len(stationArray))] for _ in range()


        else:
            error = 'Please check your commit message : startstation & endstation & date'

            return JsonResponse(
                {
                    'status':202,
                    'message':error,
                }
            )


def refund(request):
    pass

def search(request):
    pass