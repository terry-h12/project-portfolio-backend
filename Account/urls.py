from django.urls import path
from Account.views import (
    registration_view,
    LoginView,
    logout_view,
    update_account_view,
    update_password_view
)

urlpatterns = [
    path('register/', registration_view),
    path('login/', LoginView.as_view()),
    path('logout/', logout_view),
    path('updateaccount/', update_account_view),
    path('changepassword/', update_password_view),
]
