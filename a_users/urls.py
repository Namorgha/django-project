from django.urls import path
from a_users.views import *

urlpatterns = [
    path('', profile_view, name="profile"),
    path('edit/', profile_edit_view, name='profile-edit'),
    path('settings/', profile_settings_views, name='profile-settings'),
    path('anboarding/', profile_edit_view, name="profile-onboarding"),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('emailverify/', profile_emailverify, name="profile-emailverify"),
    path('delete/', profile_delete_view, name="profile-delete"),
]
