from django.views.generic import TemplateView


# Create your views here.


class Home(TemplateView):
    template_name = "guides/guides.html"


class About(TemplateView):
    template_name = "guides/about.html"
