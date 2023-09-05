from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView2, UserGoalsFormCreate, Retrieve_User, FitnessAPIView, BodyPartCRUD, ExerciseCRUD

urlpatterns = [

    path("api/token/", TokenObtainPairView.as_view(), name="token-obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup_view", UserRegistrationView2.as_view(), name="my_api_view"),
    path("goal_create", UserGoalsFormCreate.as_view(), name="goals_create"),
    path("retrieve_user/<str:email>/", Retrieve_User.as_view(), name="retrieve_user"),
    path("compute_exercises<int:counter>/", FitnessAPIView.as_view(), name="fitness"),
    path("retrieve_body_part/", BodyPartCRUD.as_view(), name="body part"),
    path("retrieve_exercise/", ExerciseCRUD.as_view(), name="exercise"),


]