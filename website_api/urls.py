from django.conf.urls import url
from bitcoin_data_handler import urls
from website_api import views_ui_front

urlpatterns = [
url(r'^base_view/$',views_ui_front.base_view,name='base_view'),
url(r'^recent_data/$',views_ui_front.recent_data,name='recent_data'),
url(r'^search/$',views_ui_front.search_block_hash,name='search_block_hash'),
#url(r'^search_transaction_hash/$',views_ui_front.search_transaction_hash,name='search_transaction_hash'),
url(r'^recent_hundred_data/$',views_ui_front.recent_hundred_data,name='recent_hundred_data'),
]
