from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'cms_users_put.views.mi_login'),
    url(r'^logout$', 'cms_users_put.views.mi_logout'),
    url(r'^cumple$', 'cms_users_put.views.home'),
    url(r'^annotated/css/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.STATIC_URL}),
    url(r'^annotated/(.*)$', 'cms_users_put.views.plantilla'),
    url(r'^cumple/(.*)$', 'cms_users_put.views.info'),
    url(r'^(.*)$', 'cms_users_put.views.notfound'),

)
