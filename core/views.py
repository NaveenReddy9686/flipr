from django.http.response import JsonResponse
from django.shortcuts import render
from .serializers import *
from django.contrib.auth.models import User
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from snippets.models import Snippet
from .utils import *

@api_view(['GET', 'POST','PUT','DELETE'])
def view_all(request):
    """
    List all users snippets, or create a new snippet.
    """
    if request.method == 'GET':
        print('GET')
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        # new = request.data.dict()
        # print(new)
        data = User.objects.get(id=request.data.get('id'))
        print(data)
        serializer = UserSerializer(data, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        # new = request.data.dict()
        # print(new)
        print('IN DELETE')
        id = request.GET.get('id')
        password = request.GET.get('password')
        print(id)
        user = 0
        user = User.objects.get(id=id)
        if(user.password==password):        
            user.delete()
            return Response(user, status=status.HTTP_200_OK)
        else : 
            return Response(user, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_one(request,id):
    try :
        serializer = UserSerializer(User.objects.get(id=id))
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:    return Response('NOT FOUND',status=status.HTTP_400_BAD_REQUEST)


from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def export_csv(request):
    data = download_csv(request, User.objects.all())
    return HttpResponse(data, content_type='text/csv')
    # return response