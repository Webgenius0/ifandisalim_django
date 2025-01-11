from rest_framework import generics
from .models import Users
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, ChangePasswordSerializer, RequestOTPSerializer, VerifyOTPAndChangePasswordSerializer, UserSerializer
from django.http import Http404
# for reset password
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
class SignupAPIView(APIView):
    permission_classes = []
    def post(self, request):
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        if password == confirm_password: 
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError({'password_mismatch': 'Password fields didn not match.'})
        return Response(data, status=response)
    


class UserProfileList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        users = Users.objects.filter(email=request.user.email)
        serializer = UserSerializer(users, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "User profile retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data)
        


# class UserProfileDetail(APIView):
#     permission_classes = [IsAuthenticated]
#     def get_object(self, pk):
#         try:
#             return Users.objects.get(pk=pk)
#         except Users.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         users = self.get_object(pk)
#         serializer = UserSerializer(users)
#         return Response(serializer.data)



#  chenge old pass to new passrord 
class ChangePassword(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        try:
            obj = Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not obj.check_password(old_password):
            return Response({"error": "Old password does not match"}, status=400)

        obj.set_password(new_password)
        obj.save()
        return Response({"success": "Password changed successfully"}, status=200)
    


# for reset password by otp
def send_otp_email(email, otp_code):
    subject = "Your OTP Code for Password Reset"
    message = f"Your OTP code is {otp_code}. It will expire in 10 minutes."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


class RequestOTPAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = Users.objects.get(email=email)
        user.generate_otp()
        send_otp_email(user.email, user.otp_code)
        return Response({"detail": "OTP sent to your email."}, status=status.HTTP_200_OK)

class VerifyOTPAndChangePasswordAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPAndChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)

