from django.conf.urls import url
from sql_populate import urls
from populate import views
from . import populate_sql
print("here")
urlpatterns = [
#url(r'^run/$',populate_sql.main, name='main'),
url(r'^run/$',populate_sql.extract_input_output_main_from_blockchain, name='extract_input_output_main_from_blockchain'),
url(r'^get_transaction_details/$',views.get_transaction_details,name='get_transaction_details'),
url(r'^get_block_details/$',views.get_block_details,name='get_block_details'),
#url(r'^get_input_details/$',views.get_input_details,name='get_input_details'),
#url(r'^get_output_details/$',views.get_output_details,name='get_output_details'),

]
