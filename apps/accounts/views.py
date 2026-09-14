from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from apps.accounts.services.otp_service import OTPService
from apps.accounts.services.send_email import EmailService
from .models import user
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import( UserSerializer)

# Create your views here.
class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        if user.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=400)
        OTP=OTPService.request_otp(email)
        SUBJECT = 'Your OTP Code'
        BODY = f'Your OTP FOR CREATING ACCOUNT IN CLINIC BOOK IS : {OTP}'
        EmailService.send_email(SUBJECT, BODY, email)
        return Response({'message': 'OTP sent successfully.'}, status=200)
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    def post(self, request):
        email = request.data.get('email')
        if user.objects.filter(email=email).exists():
            OTP=OTPService.request_otp(email)
            SUBJECT = 'Your OTP Code'
            BODY = f'Your OTP FOR LOGIN IN CLINIC BOOK IS : {OTP}'
            EmailService.send_email(SUBJECT, BODY, email)
            return Response({'message': 'OTP sent successfully.'}, status=200)
        return Response({'error': 'User not found.'}, status=404)
    
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    def post(self, request):
        email = request.data.get('email')
        entered_otp = request.data.get('otp')
        user_role = request.data.get('user_role')
        is_valid, message = OTPService.verify_otp(email, entered_otp)
        print(is_valid)
        if is_valid:
            user_obj,created = user.objects.get_or_create(email=email, user_role=user_role)
            token = RefreshToken.for_user(user_obj)
            if created:
                return Response({'message': 'OTP verified and user created successfully.','user': self.serializer_class(user_obj).data,
                                 'refresh_token': str(token),'acces_token':str(token.access_token)},
                                   status=201)

            return Response({'message': 'OTP verified successfully.','user': self.serializer_class(user_obj).data,
                              'refresh_token': str(token),'acces_token':str(token.access_token)}, 
                              status=200)

        else:
            return Response({'error': message}, status=400)

