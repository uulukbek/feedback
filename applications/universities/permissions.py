from rest_framework.permissions import BasePermission, SAFE_METHODS

from applications.feedback.models import Comment


class IsUniversityOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated or request.user.is_staff
        if request.method == 'DELETE':
            return request.user.is_authenticated and request.user == obj.owner
        return request.user.is_authenticated and (request.user == obj.owner or request.user.is_staff)
    
    
class IsFeedbackOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        try:
            return request.user.is_authenticated and request.user == Comment.objects.get(id=view.kwargs['pk']).owner
        except:
            return 'Something went wrong'

    