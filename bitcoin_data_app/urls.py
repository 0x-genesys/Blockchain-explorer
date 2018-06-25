from django.conf.urls import url
from app import urls
from bitcoin_data_app import views
from . import run_migrations
print("here")
urlpatterns = [
	url(r'^get_transaction_details/$', views.get_transaction_details,name='get_transaction_details'),
	url(r'^get_block_details/$', views.get_block_details,name='get_block_details'),
]
