from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sf_proxy.views.proxy_tunnel'),
    url(r'^([^/\.]+)', 'sf_proxy.views.proxy_tunnel'),
    
)
