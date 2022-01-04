from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from Account.validators import valid_email, valid_username
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from Account.models import Account
from Account.serializers import AccountPasswordUpdateSerializer, RegistrationSerializer, AccountProfileSerializer, AccountUpdateSerializer

# from django.http import HttpResponse
# def home(request):
#     return HttpResponse('Home')

from Account.serializers import RegistrationSerializer
# Create your views here.
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    data = {}
    email = request.data.get('email', '0').lower()
    if valid_email(email) != None:
        data['error_message'] = 'Email is already in use!'
        data['response'] = 'ERROR'
        return Response(data)

    username = request.data.get('username', '0')
    if valid_username(username) != None:
        data['error_message'] = 'That username is already in use.'
        data['response'] = 'ERROR'
        return Response(data)

    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = 'Registration successful!'
    else:
        Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data)

# LOGIN
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        res = {}
        username = request.data.get('username')
        password = request.data.get('password')
        account = authenticate(username=username, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            res['response'] = 'Successful login!'
            res['user_id'] = account.pk
            res['username'] = account.username
            res['email'] = account.email
            res['first_name'] = account.first_name
            res['last_name'] = account.last_name
            res['bio'] = account.bio
            res['profile_pic'] = account.profile_pic
            res['github'] = account.github
            res['token'] = token.key
        else:
            res['response'] = 'ERROR'
            res['error_message'] = 'Invalid username/password'
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        return Response(res)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('Successfully Logged Out')

@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountUpdateSerializer(account, data=request.data, partial=True)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['response'] = 'Update success!'
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_password_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # print(request.data)
    serializer = AccountPasswordUpdateSerializer(account, data=request.data, partial=True)
    data = {}
    if serializer.is_valid():
        # print(account.password)
        # print(request.data['password'])
        account.set_password(request.data['password'])
        account.save()
        # print(account.password)
        data['response'] = 'Successfully changed password!'
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
