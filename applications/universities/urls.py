from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.universities.views import UniversitiesViewSet

router = DefaultRouter()
router.register('', UniversitiesViewSet)


urlpatterns = [
    path('favourites/', UniversitiesViewSet.as_view({'get': 'get_favourites'})),
    path('<int:pk>/favourite/', UniversitiesViewSet.as_view({'post':'favourite'})),
    path('<int:pk>/rating/', UniversitiesViewSet.as_view({'post': 'rating'})),
    path('<int:pk>/like/', UniversitiesViewSet.as_view({'post': 'like'})),
    path('<int:pk>/comment/', UniversitiesViewSet.as_view({'post': 'add_comment'})),
    path('comment/<int:pk>/', UniversitiesViewSet.as_view({'delete': 'delete_comment'})),
    path('', include(router.urls)),  
]