from django.conf.urls import url

from guides.views import Home

urlpatterns = [
    url(r"^$", Home.as_view(), name="all"),
]
