from django.conf.urls import url
from app import urls
from website_api import views_ui_front
from website_api import address_api
from website_api import address_api_new
from website_api import search_transaction
from website_api import search_block


"""
API endpoints for accessing the website for Blockwala Bitcoin Explorer.
"""
urlpatterns = [
#url(r'^base_view/$',views_ui_front.base_view,name='base_view'),
url(r'^index/$',views_ui_front.index,name='index'),
#url(r'^recent_data/$',views_ui_front.recent_data,name='recent_data'),
url(r'^search/$',search_block.search_block_hash,name='search_block_hash'),
url(r'^recent_hundred_data/$',views_ui_front.recent_hundred_data,name='recent_hundred_data'),
url(r'^wrongQuery/$',views_ui_front.wrong_query,name='wrong_query'),
url(r'^searchTransaction/$',search_transaction.search_transaction_hash,name='search_transaction_hash'),
url(r'^searchAddress/$',address_api_new.search_address,name='search_address'),
url(r'^searchBlockHeight/$',views_ui_front.search_block_height,name='search_block_height'),
url(r'^wrongQuery/$',views_ui_front.wrong_query,name='wrong_query'),
url(r'^mainSearch/$',views_ui_front.main_search_bar,name='main_search_bar'),
url(r'^wallet/$',views_ui_front.wallet,name='wallet'),
]