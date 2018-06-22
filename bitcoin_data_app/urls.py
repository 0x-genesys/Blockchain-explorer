from django.conf.urls import url
from app import urls
from bitcoin_data_app import views
from . import populate_sql

urlpatterns = [
url(r'^run/$',populate_sql.extract_input_output_main_from_blockchain, name='extract_input_output_main_from_blockchain'),
url(r'^get_transaction_details/$',views.get_transaction_details,name='get_transaction_details'),
url(r'^get_block_details/$',views.get_block_details,name='get_block_details'),

]
