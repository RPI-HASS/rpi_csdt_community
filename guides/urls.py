from django.conf.urls import url

from guides.views import Home, About

urlpatterns = [
    url(r"^$", Home.as_view(), name="all"),
    url(r'^about/', About.as_view(), name="about"),
]
