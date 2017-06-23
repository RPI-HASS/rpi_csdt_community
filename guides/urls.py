from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.Home.as_view(), name="all"),
    url(r'^about/', views.About.as_view(), name="about"),
]
