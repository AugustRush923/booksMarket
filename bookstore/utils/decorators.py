from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def login_required(view_func):
    """登录判断装饰器"""

    def wrapper(request, *args, **kwargs):
        if request.session.has_key('islogin'):
            # session有缓存证明已经登录
            return view_func(request, *args, **kwargs)
        # 没有登录则跳转到登录页面
        return redirect(reverse('user:login'))

    return wrapper
