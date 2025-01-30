from django.urls import path
from .views import StaticUsersView, DynamicUsersView

urlpatterns = [
    # path('static-users/', static_users, name='static-users'),
    # path('dynamic-users/', dynamic_users, name='dynamic-users'),
    path('static-users-api/', StaticUsersView.as_view(), name='static-users-api'),
    path('dynamic-users-api/', DynamicUsersView.as_view(), name='dynamic-users-api'),
]
