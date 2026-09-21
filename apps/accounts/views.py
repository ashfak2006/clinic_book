import logging
from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from apps.accounts.services.otp_service import OTPService
from apps.accounts.services.send_email import EmailService
from .serializers import (
    RequestOTPSerializer,
    UserSerializer,
    UsernameLoginSerializer,
    VerifyOTPSerializer,
)

logger = logging.getLogger(__name__)
User = get_user_model()


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        tags=["Accounts"],
        summary="Request OTP for user sign-up",
        description="Sends a 6-digit OTP code to the provided email if the email is not already registered.",
        request=RequestOTPSerializer,
        responses={
            200: inline_serializer(
                name="SignUpSuccessResponse",
                fields={"message": serializers.CharField(default="OTP sent successfully.")},
            ),
            400: OpenApiResponse(description="User with this email already exists or invalid request."),
            500: OpenApiResponse(description="Failed to send OTP email."),
        },
    )
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower()

        # if User.objects.filter(email=email).exists():
        #     return Response(
        #         {"error": "User with this email already exists."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        otp = OTPService.request_otp(email)
        subject = "Your OTP Code - Clinic Book"
        body = f"Your OTP for creating your account in Clinic Book is: {otp}"
        email_sent = EmailService.send_email(subject, body, email)

        if not email_sent:
            return Response(
                {"error": "Failed to send OTP email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        tags=["Accounts"],
        summary="Request OTP for user login",
        description="Sends a 6-digit OTP code to the provided email for an existing user.",
        request=RequestOTPSerializer,
        responses={
            200: inline_serializer(
                name="LoginOTPSuccessResponse",
                fields={"message": serializers.CharField(default="OTP sent successfully.")},
            ),
            404: OpenApiResponse(description="User not found."),
            500: OpenApiResponse(description="Failed to send OTP email."),
        },
    )
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower()

        if not User.objects.filter(email=email).exists():
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp = OTPService.request_otp(email)
        subject = "Your OTP Code - Clinic Book"
        body = f"Your OTP for login in Clinic Book is: {otp}"
        email_sent = EmailService.send_email(subject, body, email)

        if not email_sent:
            return Response(
                {"error": "Failed to send OTP email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)


class UsernameLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        tags=["Accounts"],
        summary="Login with username and password",
        description="Authenticates a user via email and password, returning JWT access and refresh tokens.",
        request=UsernameLoginSerializer,
        responses={
            200: inline_serializer(
                name="UsernameLoginResponse",
                fields={
                    "message": serializers.CharField(default="Authenticated successfully."),
                    "user": UserSerializer(),
                   
                },
            ),
            400: OpenApiResponse(description="Invalid emil or password."),
            403: OpenApiResponse(description="This account is inactive."),
        },
    )
    def post(self, request):
        serializer = UsernameLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            return Response(
                {"error": "Invalid email "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user_obj.is_active:
            return Response(
                {"error": "This account is inactive."},
                status=status.HTTP_403_FORBIDDEN,
            )
        print(password)
        if not user_obj.check_password(password):
            return Response(
                {"error": "Invalid password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user_obj)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user_data = UserSerializer(user_obj).data

        response = Response(
            {
                "message": "Authenticated successfully.",
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )

        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=15 * 60,
            path="/",
        )

        # Refresh token
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
            path="/",
        )

        return response
        


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        tags=["Accounts"],
        summary="Verify OTP for login or sign-up",
        description="Verifies the OTP sent to the email. If the user does not exist, registers a new user with the specified role. Returns JWT tokens and user details.",
        request=VerifyOTPSerializer,
        responses={
            200: inline_serializer(
                name="VerifyOTPLoginResponse",
                fields={
                    "message": serializers.CharField(default="OTP verified successfully."),
                    "user": UserSerializer(),
                    "refresh_token": serializers.CharField(),
                    "access_token": serializers.CharField(),
                    "acces_token": serializers.CharField(),
                },
            ),
            201: inline_serializer(
                name="VerifyOTPSignUpResponse",
                fields={
                    "message": serializers.CharField(default="OTP verified and user created successfully."),
                    "user": UserSerializer(),
                    "refresh_token": serializers.CharField(),
                    "access_token": serializers.CharField(),
                    "acces_token": serializers.CharField(),
                },
            ),
            400: OpenApiResponse(description="Invalid or expired OTP."),
        },
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].lower()
        entered_otp = serializer.validated_data["otp"]
        user_role = serializer.validated_data.get("user_role", "patient")

        is_valid, message = OTPService.verify_otp(email, entered_otp)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.filter(email=email).first()
        created = False

        if not user_obj:
            # Create new user for signup flow
            user_obj = User.objects.create(
                email=email,
                user_role=user_role,
                is_active=True,
            )
            created = True

        refresh = RefreshToken.for_user(user_obj)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        user_data = UserSerializer(user_obj).data

        response_payload = {
            "message": (
                "OTP verified and user created successfully."
                if created
                else "OTP verified successfully."
            ),
            "user": user_data,
        }
        response =  Response(
            response_payload,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=15 * 60,
            path="/",
        )
        
                # Refresh token
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
            path="/",
        )
        
        return response

