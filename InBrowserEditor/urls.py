from django.conf.urls import patterns, include, url
from editor.views import HomeView,preview,save

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'InBrowserEditor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

#Main site redirects
urlpatterns += patterns('',
    url(r'^(index.html)?$', HomeView.as_view()),
    url(r'^save/$', save),
    url(r'^preview/$', preview),
) 