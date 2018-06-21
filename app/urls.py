"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from website_api import views_ui_front

urlpatterns =[

    # url(r'^admin/',admin.site.urls),
    url(r'^core/', include('bitcoin_data_app.urls')),
    url(r'^ui/', include('website_api.urls')),
    #
    # url(r'^search/$',views_ui_front.search_block_hash,name='search_block_hash'),
    # url(r'^searchTransaction/$',views_ui_front.search_transaction_hash,name='search_transaction_hash'),
    #
    # url(r'^searchAddress/$',views_ui_front.search_address,name='search_address'),
    # #url(r'^recentHundredData/(?P<pk>\d+)/$',views_ui_front.recent_hundred_data,name='recent_hundred_data'),
    # url(r'^searchBlockHeight/$',views_ui_front.search_block_height,name='search_block_height'),
    # url(r'^wrongQuery/$',views_ui_front.wrong_query,name='wrong_query'),
    #
    # url(r'^mainSearch/$',views_ui_front.main_search_bar,name='main_search_bar'),
]
