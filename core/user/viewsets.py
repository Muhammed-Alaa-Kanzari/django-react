from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from core.user.serializers import UserSerializer
from core.user.models import User
from core.abstract.viewsets import AbstractViewSet


class UserViewSet(AbstractViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('patch', 'get')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):

        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])

        self.check_object_permissions(self.request, obj)
        return obj