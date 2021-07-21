from django.urls import path
from .views import location

urlpatterns = [
    path("locations", location.LocationListView.as_view()),
    path("locations/<int:id>", location.ProvincialView.as_view()),
    path("district/<int:id>", location.DistrictsView.as_view()),
]
