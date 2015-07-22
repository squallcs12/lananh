from django.conf.urls import include, url
from dashboard.views.index_view import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
