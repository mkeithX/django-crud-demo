from django.urls import path
from apps.users.views import Signup, ProfileListView, ProfileDetailView, DeleteAccountView, UpdateProfileView, AboutPageView
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),

    path("signup/", Signup.as_view(), name="signup"),
    path("profile/<str:pk>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path('update-profile/<str:pk>/', UpdateProfileView.as_view(), name="update-profile"),
    path("delete/<str:pk>/", DeleteAccountView.as_view(), name="delete-account"),
    
    path("recent/", ProfileListView.as_view(), name="all-users"),
    path("search/", views.SearchView.as_view(), name="search"),

    path("about/", AboutPageView.as_view(),name="about"),

]
