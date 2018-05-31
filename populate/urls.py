from django.conf.urls import url
from sql_populate import urls
from populate import views
from . import populate_sql
print("here")
urlpatterns = [
#url(r'^run/$',populate_sql.main, name='main'),
url(r'^run/$',populate_sql.extract_input_output_main_from_blockchain, name='extract_input_output_main_from_blockchain'),
]
