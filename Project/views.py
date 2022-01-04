from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from Project.serializers import ProjectCreateSerializer, ProjectSerializer, ProjectUpdateSerializer
from rest_framework.response import Response
# from rest_framework.generics import UpdateAPIView, ListAPIView
# from rest_framework.pagination import PageNumberPagination
# from Project.models import Project
# from django.db.models import Q
# from Account.serializers import AccountProfileSerializer
# import json
# from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def create_project_view(request):
    if request.method == 'POST':
        data = request.data.copy()
        print(request.user)
        data['account_id'] = request.user.pk
        serializer = ProjectCreateSerializer(data = data)

        data = {}
        if serializer.is_valid():
            #print("serialiser is valid")
            project = serializer.save()
            data['project_id'] = project.pk
            data['image_url'] = project.image_url
            # data['account_id'] = project.account_id.pk
            data['title'] = project.title
            data['description'] = project.description
            data['is_public'] = project.is_public
            data['backend_repo'] = project.backend_repo
            data['frontend_repo'] = project.frontend_repo
            data['website'] = project.website

            # if (project.is_shared is not None):
            #     data['is_shared'] = project.is_shared.pk
            # else:
            #     data['is_shared'] = None
            data['username'] = project.account_id.username
            # print("can return")
            print(data)
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)