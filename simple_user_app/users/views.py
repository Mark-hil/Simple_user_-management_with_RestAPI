from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import User
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Hard-coded users endpoint
def static_users(request):
    users = [
        {"id": 1, "firstname": "Mark", "lastname": "Ampomah", "age": 24, "email": "Markhill@gmial.com"},
        {"id": 2, "firstname": "Caleb", "lastname": "Osam", "age": 30, "email": "caleb@gmail.com"},
    ]
    return JsonResponse({"status": "success", "src": "hard-coded", "data": users}, safe=False)

# Dynamic users (GET and POST)
@csrf_exempt
def dynamic_users(request):
    if request.method == 'GET':
        users = User.objects.all().values("id", "firstname", "lastname", "age", "email")
        return JsonResponse({"status": "success", "src": "database", "data": list(users)}, safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            firstname = body.get("firstname")
            lastname = body.get("lastname")
            age = body.get("age")
            email = body.get("email")

            if not all([firstname, lastname, age, email]):
                return JsonResponse({"status": "error", "message": "All fields are required."}, status=400)

            user = User.objects.create(firstname=firstname, lastname=lastname, age=age, email=email)
            return JsonResponse({"status": "success", "message": "User created successfully.", "data": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "age": user.age,
                "email": user.email
            }}, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

# Static Users Endpoint
class StaticUsersView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))  # Cache for 2 hours
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        cached_users = cache.get("static_users_api")
        if cached_users:
            return Response({"status": "success", "src": "cache", "data": cached_users})

        users = [
            {"id": 1, "firstname": "Mark", "lastname": "Ampomah", "age": 24, "email": "Markhill@gmial.com"},
            {"id": 2, "firstname": "Caleb", "lastname": "Osam", "age": 30, "email": "caleb@gmail.com"},
        ]
        
        cache.set("static_users_api", users, timeout=300)  # Ensure correct key

        return Response({"status": "success", "src": "hard-coded", "data": users})

# Dynamic Users Endpoint
class DynamicUsersView(APIView):
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        cached_users = cache.get("dynamic_users_api")
        if cached_users:
            return Response({"status": "success", "src": "cache", "data": cached_users})

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        cache.set("dynamic_users_api", serializer.data, timeout=300)  # Ensure correct key

        return Response({"status": "success", "src": "database", "data": serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("dynamic_users_api")  # Invalidate cache to update list
            return Response({"status": "success", "message": "User created successfully.", "data": serializer.data}, status=201)

        return Response({"status": "error", "message": serializer.errors}, status=400)
