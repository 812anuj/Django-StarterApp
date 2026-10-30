from django.urls import path
from a_user.views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', profile_edit_view, name='profile_edit'),
    path('onbording/', profile_edit_view, name='profile_onbording'),
    path('@<username>', profile_view, name='profile_view'),
    path('settings/', profile_settings_view, name='profile_settings'),
    path('emailchange/', profile_emailchange, name='profile_emailchange'),
    path('delete/', profile_delete_view, name='profile_delete'),
]