from django.conf.urls import url
from roller_auth import views as roller_auth

urlpatterns = [
    url(r'^api/signup/?$', roller_auth.APISignupView.as_view(), name='roller_auth__api_signup'),
    url(r'^api/login/?$', roller_auth.APILoginView.as_view(), name='roller_auth__api_login'),
    url(r'^api/logout/?$', roller_auth.APILogoutView.as_view(), name='roller_auth__api_logout'),
    url(r'^api/server/?$', roller_auth.ServerView.as_view(), name='roller_auth__server'),
    url(r'^api/users/me/?$', roller_auth.APIUsersMeView.as_view(), name='roller_auth__users__me'),
    url(r'^api/users/me/profile_picture/?$', roller_auth.APIUploadProfilePicture.as_view(), name='roller_auth__users__me__profile_picture'),

    url(r'^login$', roller_auth.LoginView.as_view(), name='roller_auth__login'),
    url(r'^logout$', roller_auth.LogoutView.as_view(), name='roller_auth__logout'),
]
