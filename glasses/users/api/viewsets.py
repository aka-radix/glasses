from typing import Union

from rest_framework import (
    decorators,
    exceptions,
    mixins,
    response,
    viewsets,
)

from glasses.users.models import User

from .serializers import UserPreferencesSerializer, UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self) -> Union[User, None]:
        """Always return the request's user only."""

        try:
            return self.queryset.get(id=self.request.user.pk)
        except User.DoesNotExist as e:
            raise exceptions.PermissionDenied from e

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @decorators.action(methods=["patch"], detail=False)
    def set_currency(self, request, *args, **kwargs):
        serializer = UserPreferencesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return response.Response(serializer.data)
