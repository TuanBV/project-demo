
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import render, redirect
from django.views import View



# Create your views here.
from rest_framework import generics
from .models import New
from .serializers import NewSerializer

class NewListView(generics.ListAPIView):
    queryset = New.objects.all().order_by('-id')  # Hiển thị tin mới nhất trước
    serializer_class = NewSerializer

class NewDetailView(generics.RetrieveAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered successfully"}, status=201)

class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"error": "Invalid credentials"}, status=401)

class NewCreateView(generics.CreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        image = request.FILES.get('image')
        if image:
            data['image'] = image
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class NewUpdateView(generics.UpdateAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [IsAuthenticated]

class NewDeleteView(generics.DestroyAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [IsAuthenticated]


class ProductView(View):
    def get(self, request):
        # topwears = Product.objects.filter(category='TW')
        # laptops = Product.objects.filter(category='L')
        # mobiles = Product.objects.filter(category='M')
        return render(request, 'home.html')

