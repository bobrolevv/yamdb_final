from django.urls import path

from .views import SignupAPIView, TokenAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view()),
    path('token/', TokenAPIView.as_view(), name='token_obtain_pair'),
]
