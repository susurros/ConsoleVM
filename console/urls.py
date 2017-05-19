from django.conf.urls import include, url
from console.toolset.vhost import update_db_init
from django.contrib.auth import views as auth_views
from . import views
from . import ajax

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'console/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', views.dash_vm),
    url(r'^vmachine/$', views.dash_vm),
    url(r'vhost/$', views.dash_vhost),
    url(r'^vmachine/new/$',views.form_vm),
    url(r'^vhost/new/$', views.form_vhost),
    url(r'^vhost/datastore/$', views.dash_datastore),
    url(r'^vhost/datastore/new/$', views.form_datastore),
    url(r'^vhost/network/$', views.dash_network),
    url(r'^vhost/network/new/$', views.form_network),
    url(r'^ajax/startvm/$', ajax.start_vm),
    url(r'^ajax/stopvm/$', ajax.stop_vm),
    url(r'^ajax/pausevm/$', ajax.pause_vm),
    url(r'^ajax/mngsnap/$', ajax.mng_snap),
    url(r'^ajax/mksnap/$', ajax.mk_snap),
    url(r'^ajax/delsnap/?$', ajax.del_snap),
    url(r'^ajax/rstsnap/$', ajax.rst_snap),
    url(r'^ajax/modifyvm/$', ajax.modify_vm),
    url(r'^ajax/clonevm/$', ajax.clone_vm),
    url(r'^ajax/deletevm/$', ajax.delete_vm),
    url(r'^ajax/deletevh/$', ajax.delete_vhost),
    url(r'^ajax/delnet/?$', ajax.del_net),
    url(r'^ajax/deldstore/?$', ajax.del_dstore),
    url(r'^ajax/vm_update_query/$', ajax.vm_update_query),
    url(r'^ajax/vhost_update_query/$', ajax.vhost_update_query),
    url(r'^ajax/net_update_query/$', ajax.net_update_query),
    url(r'^ajax/dstore_update_query/$', ajax.dstore_update_query),
    url(r'^ajax/updatedb/$', ajax.updatedb),
    url(r'^ajax/form_vm/$', ajax.form_vm),
    url(r'^ajax/control_vm/$', ajax.control_vh),
    url(r'^ajax/remote/$', ajax.remote),
]

#update_db_init()