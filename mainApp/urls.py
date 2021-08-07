from django.urls import path
from . import views


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenRefreshSlidingView,
)
...

schema_view = get_schema_view(
   openapi.Info(
      title="EXPIENCES API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('register/', views.RegisterView.as_view(), name='register'),
   path('login/', views.LoginAPIView.as_view(), name='login'),
   path('request-password/', views.RequestNewPasswordAPIView.as_view(), name='request_password'),
   path('reset-password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
   path('verify-token/<uidb64>/<token>/', views.VerifyResetPasswordTokenAPIView.as_view(), name='verify_token'),
   path('verify-email/', views.VerifyEmailView.as_view() , name='verify_email'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),

]


