"""music_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from weibologin import views
from django.contrib import staticfiles
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    #weibologin.views
	url(r'^$', 'weibologin.views.home',name='home'),
	url(r'login/$', 'weibologin.views.log',name='log'),
    url(r'logout/$', 'weibologin.views.userlogout',name='logout'),
    url(r'register/$', 'weibologin.views.register',name='register'),
    url(r'weiboLogin/$', 'weibologin.views.weiboLogin',name='weiboLogin'),
    url(r'registersave/$', 'weibologin.views.registersave',name='registersave'),
    url(r'^logincheck/$', 'weibologin.views.logincheck', name='logincheck'),
    url(r'^tasteTest/$', 'weibologin.views.tasteTest', name='tasteTest'),
    url(r'^weiboLogcheck/$', 'weibologin.views.weiboLogcheck', name='tasteTest'),
    url(r'^personalInformation/$','weibologin.views.personalInformation',name='personalInformation'),
    url(r'^loginAPI','weibologin.views.loginAPI',name='loginAPI'),#登录接口
    #url(r'^logout/$', 'searchSystem.views.logout', name='logout'),
    url(r'^admin/', admin.site.urls),
    #searchSystem.views. 直播
    url(r'^search/$', 'searchSystem.views.search'),
    #url(r'^searchprogram/$', 'searchSystem.views.searchprogram',name='searchprogram'),
    #url(r'^searchprogramAPI/$', 'searchSystem.views.searchprogramAPI',name='searchprogramAPI'),
    #url(r'^achives/$', 'searchSystem.views.achives', name = 'achives'),
	#url(r'^live/$', 'searchSystem.views.displayArea', name = 'liveArea'),
    url(r'^liveArea/$', 'searchSystem.views.displayArea', name = 'liveArea'),
    url(r'^liveType/$', 'searchSystem.views.displayType', name='liveType'),
   # url(r'live/^$', 'searchSystem.views.home'),
    #url(r'^time/plus/(?P<offset>\d+)/$','searchSystem.views.hours_ahead'),
    url(r'^live/radio/$','searchSystem.views.displayRadio',name='displayRadio'),
    url(r'^live/radio/play/$','searchSystem.views.radioPlay',name='radioPlay'),
     url(r'^collect/$','searchSystem.views.collect',name='collect'),
    #接口
     url(r'^liveRadioBjAPI/$','searchSystem.views.liveRadioBjAPI',name='liveRadioBjAPI'),


    #personalRecommend.views
    url(r'^personalRecommend/$','personalRecommend.views.personalHome',name='personalHome'),
    url(r'^collectProgram/$','personalRecommend.views.collectProgram',name='collectProgram'),
    url(r'^programScore/$','personalRecommend.views.programScore',name='programScore'),
    url(r'^getUserPlayPause/$','personalRecommend.views.getUserPlayPause',name='getUserPlayPause'),

    #接口user_collectAPI
    #方法一
    url(r'^usercollectAPI/$','personalRecommend.views.usercollectAPI',name='usercollectAPI'),
    #方法二
    #\d表示输入1个以上的数字
    # url(r'^usercollectAPI2/(?P<userID>\d+)/$','personalRecommend.views.usercollectAPI2',name='usercollectAPI2'),
    url(r'^personalRecommendAPI','personalRecommend.views.personalRecommendAPI',name='personalRecommendAPI'),#用户推荐节目接口
    url(r'^stationCollectAPI/$','searchSystem.views.stationCollectAPI',name='stationCollectAPI'),#电台收藏提交
    url(r'^programCollectAPI/$','personalRecommend.views.programCollectAPI',name='programCollectAPI'),#节目收藏提交
    url(r'^registerAPI','weibologin.views.registerAPI',name='registerAPI'),#注册接口
    url(r'^age_sexsubmitAPI','weibologin.views.age_sexsubmitAPI',name='age_sexsubmitAPI'),#注册年龄、性别提交接口
    url(r'^weiboLoginAPI', 'weibologin.views.weiboLoginAPI', name='weiboLoginAPI'),  # 微博授权登录接口
    url(r'^changepasswordAPI','user_info.views.changepasswordAPI',name='changepasswordAPi'),#用户资料修改修改密码接口
    url(r'^tastesubmitAPI','weibologin.views.tastesubmitAPI',name='tastesubmitAPI'),#兴趣提交接口


       #个人信息
    url(r'^personalInformation/$','weibologin.views.personalInformation',name='personalInformation'),#个人信息显示页面
    url(r'^personalTaste/$','weibologin.views.personalTaste',name='personalTaste'),#个人信息显示页面
    url(r'^changepassword/$', 'user_info.views.change_pwd', name='changepassword'),#密码修改功能
    url(r'^user_program_collect', 'user_info.views.program_collect', name='user_program_collect'),  # 用户收藏的节目
    url(r'^user_station_collect','user_info.views.station_collect',name='user_staiton_collect'),#用户收藏的电台
    url(r'^program_collect_delete','user_info.views.program_collect_delete',name='program_collect_delete'),#用户收藏节目单项删除
    url(r'^station_collect_delete','user_info.views.station_collect_delete',name='station_collect_delete'),#用户收藏电台单项删除
    url(r'^p_collect_delete_all','user_info.views.program_collect_delete_all',name='program_collect_delete_all'),#用户收藏节目全选删除 ~
    url(r'^collect_multi_delete','user_info.views.program_collect_multi_delete',name='program_collect_multi_delete'),#用户收藏节目多选删除~
    url(r'^s_collect_delete_all','user_info.views.station_collect_delete_all',name='station_collect_delete'),#用户收藏电台全选删除~
    url(r'^multi_delete_sta','user_info.views.station_collect_multi_delete',name='station_collect_delete'),#用户收藏电台多选删

]

#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )