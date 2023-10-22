from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
