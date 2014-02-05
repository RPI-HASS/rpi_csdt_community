from rest_framework import viewsets, routers

from project_share.models import Project

class ProjectViewSet(viewsets.ModelViewSet):
    model = Project

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
