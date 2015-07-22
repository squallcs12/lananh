from django.conf.urls import url

logout_context = {
    'template_name': 'registration/logged_out.html',
}

password_reset_context = {
    'template_name': 'registration/password_reset.html',
}

password_change_context = {
    'template_name': 'registration/password_change.html',
}

password_change_done_context = {
    'template_name': 'registration/password_change_done.html',
}

password_reset_done = {
    'template_name': 'registration/password_reset_done.html',
}

password_reset_confirm = {
    'template_name': 'registration/password_reset_confirm.html',
}

password_reset_complete = {
    'template_name': 'registration/password_reset_complete.html',
}


urlpatterns = [
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', logout_context, 'logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', password_change_context, 'password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',
        password_change_done_context, 'password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        password_reset_context, 'password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
        password_reset_done, 'password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        password_reset_complete, name='password_reset_complete'),
]
