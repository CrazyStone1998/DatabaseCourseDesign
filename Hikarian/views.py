from django.shortcuts import render
from django.views.decorators.cache import never_cache
from common.decorator.ajax_post_only import ajax_post_only
from common.auth.userSystem import userSystem


# Create your views here.

@never_cache
def hasLoggedIn(request):
    '''
    判断用户是否在线的一个函数
    目前划不清楚用途
    :param request:
    :return:
    '''
    if request.method == 'GET':

        if request.session.has_key('sessionID') and request.session.has_key('token'):
            # 用户拥有session，登陆验证
            user = userSystem(request)
            if not user.getUserObject():
                print('--------------------')
                print('用户在线判断')



@ajax_post_only
def login(request):
    '''
    登陆函数
    :param request:
    :return:
    '''

    # 获取用户 账户 和 密码
    username = request.POST.get('username')
    password = request.POST.get('password')

    # 获取user对象
    user = userSystem(request)
    # user登陆 认证
    # 判定新用户登陆 顶替旧的用户
    if user.getUsername() != username:
        user.delCache()
        # 清理 session
        request.session.flush()

    error,userType = user.authentication(username=username,password=password)
    # error为空 则登陆成功
    # error不为空 则登陆不成功
    if not error:
       print('登陆成功')


@ajax_post_only
def logout(request):
    '''
    账号 登出
    :param request:
    :return:
    '''
    # 清理缓存
    user = userSystem(request)
    user.delCache()
    # 清理 session
    request.session.flush()

    print('用户登出')


@ajax_post_only
def register(request):
    # 错误信息列表
    error = ''
    # 后台获取并判断用户名和密码 是否为空
    username = request.POST.get('username')
    passwd = request.POST.get('password')
    if username is None or passwd is None:
        error = 'The username&passwd cannot be empty'
        # 获取并判断 用户名是否存在
    else:
        img = request.FILES.get('profile')
        # 检测用户 大脸照是否为人脸
        result = BaiduAPI.facerecognize(img.read())
        # 用户大脸照 判定成功
        if result['result'] == 'SUCCESS':
            if not models.user.objects.filter(Q(username=username)&Q(isDelete=False)).exists():

                passwd   = make_password(passwd)
                name     = request.POST.get('name')
                userType = request.POST.get('userType')
                profile  = settings.ICON_URL+'static/weCheck/img/'+username+'.jpg'
                # 将 用户 大脸照 写入 本地文件中
                imgPath  = os.path.join(settings.BASE_DIR,'static','weCheck','img',username+'.jpg')
                # 判断用户 大脸照 是否存在 若存在 重写
                if os.path.exists(imgPath):
                    os.remove(imgPath)
                with open(imgPath,'wb+') as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                # 调用 model类的 新建对象方法 存储用户对象
                models.user.userObject(username,passwd,name,profile,userType,)
                # 返回 json
                return JsonResponse({
                                     'status':200,
                                     'message':'OK'
                                                })
            else:
                error = 'Username already exists'
        else:
            # 用户大脸照 判定失败
            error = result['msg']
    return JsonResponse({
            'status':202,
            'message':error,
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
    username = request.GET.get('id')
    if username:
        user = models.user.objects.get_or_none(username=username)
    else:
        user = models.user.objects.get_or_none(username=userSystem(request).getUsername())

    if user is not None:

        return JsonResponse({

            'status': 200,
            'message': 'success',
            'data': {
                'username': user.username,
                'profile': user.profile,
                'name': user.name,
                'userType':user.userType

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

    user = models.user.objects.get_or_none(username=userSystem(request).getUsername())

    user.name = request.POST.get('name',user.name)

    img = request.FILES.get('profile')
    if img:
        # 修改 大脸照
        user.profile = settings.ICON_URL + 'static/weCheck/img/' + user.username + '.jpg'
        # 将 用户 大脸照 写入 本地文件中
        imgPath = os.path.join(settings.BASE_DIR,'static', 'weCheck', 'img', user.username + '.jpg')
        # 判断用户 大脸照 是否存在 若存在 重写
        if os.path.exists(imgPath):
            os.remove(imgPath)
        with open(imgPath, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
    # 保存 修改
    user.save()

    return JsonResponse({
        'status':200,
        'message':'success'
    })

