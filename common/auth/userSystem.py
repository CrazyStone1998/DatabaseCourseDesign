#!/usr/bin/python
# -*- coding: UTF-8 -*-

import redis
import hashlib
import time
from Hikarian import models

re = redis.StrictRedis(host='127.0.0.1',port='6379',db=0)

def md5(obj):

    passwd = hashlib.md5()
    passwd.update(obj.encode('utf8'))
    return passwd.hexdigest()[0:10]

def makepassword(user_id, passwd):
    '''
    自定义 函数 生成加密密码
    :param user_id:
    :param passwd:
    :return:
    '''
    passwd_hash = hashlib.sha1()
    passwd_hash.update((user_id + passwd + 'passwd').encode('utf8'))
    passwd = passwd_hash.hexdigest()
    return passwd

def checkpassword(user_id, passwd, passwdDatabase):
    '''
    自定义 函数 检测密码
    :param user_id:
    :param passwd:
    :param passwdDatabase:
    :return:
    '''
    passwd = makepassword(user_id, passwd)

    return passwd == passwdDatabase



class userSystem(object):

    def __init__(self, request, response=None, user_id=None, **kwargs):

        self.request = request
        self.response =response
        self.kwargs = kwargs
        self.user_id = user_id
        self.sessionID = None
        self.token = None

    def authentication(self, user_id, passwd):
        '''
        用户 登陆 认 证
        :param user_id:
        :param passwd:
        :return:
        '''

        error = []

        # 获取登陆对象
        userlogin = models.userInfo.objects.get_or_none(user_id=user_id)

        if userlogin is not None:
            # 设置 self 中维护的user_id，设置缓存时需要
            self.user_id = user_id
            # 检测 密码
            if checkpassword(user_id,passwd,userlogin.passwd):
                # 设置 缓存
                self.setCookieAndSession()

                return error

            else:
                error.append('The password is not right')
        else:
            # 用户对象 不存在
            error.append('user matching query does not exist.')

        return error

    def getUsername(self):
        '''
        获取用户 user_id
        :return:
        '''
        self.sessionID = self.request.session.get('sessionID')

        if re.exists('sessionID_%s' % self.sessionID):
            return re.hget('sessionID_%s' % self.sessionID, 'user_id').decode()

        else:
            return None

    def delCache(self):
        '''
        清楚 缓存 session登陆信息
        :return:
        '''
        if self.request.session.has_key('sessionID') and self.request.session.has_key('token'):
            sessionID = self.request.session.get('sessionID')

            if re.exists('sessionID_%s' % sessionID):
                re.delete('sessionID_%s' % sessionID)
            return True
        return False

    def testCookie(self):
        '''
        在login 中设置 request.session.set_test_cookie()
        如果返回 False 则说明 用户浏览器 关闭了 cookies
        如果返回 True 则说明 用户 浏览器 开启了 cookies
        :return:
        '''
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def getUserObject(self):
        '''
        返回 用户对象，
            有则说明用户已经登陆，并返回用户对象
            没有 就说明用户没有登陆
        :return:
        '''
        self.sessionID = self.request.session.get('sessionID')
        self.token = self.request.session.get('token')

        if re.exists('sessionID_%s' % self.sessionID):

            token_redis = re.hget('sessionID_%s' % self.sessionID,'token').decode()
            user_id_redis = re.hget('sessionID_%s' % self.sessionID,'user_id').decode()

            if token_redis == self.token:
                return user_id_redis
        return None

    def setCookieAndSession(self):
        '''
        设置 cookie and session
        :return:
        '''

        self.sessionID = self.request.session.get('sessionID')
        if not self.sessionID:
            # set cookie
            # md5 加密 随机生成
            hash = hashlib.sha256(self.user_id.encode("utf8"))
            token = hashlib.sha256((time.strftime('%H:%M:%S').encode("utf8")))
            # token = hashlib.sha256(self.user_id.encode("utf8"))

            hashID = hash.hexdigest()
            tokenID = token.hexdigest()

            self.request.session['sessionID'] = hashID
            self.request.session['token'] = tokenID
            self.sessionID = hashID
            self.token = tokenID

        # 判断缓存中是否存在该 sessionID
        if not re.exists('sessionID_%s' % self.sessionID):

            # set session
            re.hmset('sessionID_%s' % self.sessionID, {'user_id': self.user_id, 'token': self.token})

        return True



