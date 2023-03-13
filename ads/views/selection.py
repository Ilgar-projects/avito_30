from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.permissions import IsSelectionOwner
from ads.serializers import SelectionSerialiser, SelectionCreateSerialiser


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerialiser
    serializer_classes = {
        'create': SelectionCreateSerialiser,
    }

    default_permission = [AllowAny(), ]
    permission_list = {"create": [IsAuthenticated()],
                       "update": [IsAuthenticated(), IsSelectionOwner()],
                       "partial_update": [IsAuthenticated(), IsSelectionOwner()],
                       "destroy": [IsAuthenticated(), IsSelectionOwner()],
                       }

    def get_permissions(self):
        return self.permission_list.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)