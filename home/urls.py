from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views


app_name = 'home'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^login/$', views.crud.login, name='login'),
	url(r'^loginsubmit/$', views.crud.loginsubmit, name='loginsubmit'),
	url(r'^admin/$', views.crud.admin, name='admin'),
	url(r'^logout/$', views.crud.logout, name='logout'),
	url(r'^additem/$', views.crud.additem, name='additem'),
	url(r'^([0-9]+)/edit/$', views.crud.edit, name='edit'),
	url(r'^([0-9]+)/delete/$', views.crud.delete, name='delete'),
	url(r'^update/$', views.crud.update, name='update'),
	url(r'^([0-9]+)/details/$', views.crud.details, name='details'),
	url(r'^([0-9]+)/addtocart/$', views.crud.addtocart, name='addtocart'),
	url(r'^cart/$', views.crud.cart, name='cart'),
	url(r'^emptycart/$', views.crud.emptycart, name='emptycart'),
	url(r'^([0-9]+)/updatequantity/$', views.crud.updatequantity, name='updatequantity'),
	url(r'^([0-9]+)/removecart/$', views.crud.removecart, name='removecart')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)