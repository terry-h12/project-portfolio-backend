from django.urls import path
from Project.views import (
    create_project_view
)

urlpatterns = [
    path('create/', create_project_view),
]