# -*- coding: utf-8 -*-
from accounts.models import User

class WeiboBackend:

    def authenticate(self, weibo_user=None, token=None):

        try:
            user = User.objects.get(id=token.uid)
            user.auth_token = token.access_token
            user.expired_time = token.expires_in

        except BaseException:
            user = User(id=token.uid, name=weibo_user.screen_name, \
                image_url=weibo_user.avatar_large or weibo_user.profile_image_url, \
                statuses_count=weibo_user.statuses_count, \
                friends_count=weibo_user.friends_count, \
                followers_count=weibo_user.followers_count, \
                verified=weibo_user.verified, \
                verified_type=weibo_user.verified_type, \
                auth_token=token.access_token, \
                expired_time=token.expires_in,
                #last_sync=datetime.today(),
                #create_time=datetime.today(),
                )

        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
