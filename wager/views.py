from rest_framework import generics
from rest_framework.response import Response
from .serializer import pick1Serializer
from .models import pick1


class pick1View(generics.GenericAPIView):
    serializer_class = pick1Serializer

    def get(self, request):
        pick1_data = pick1.objects.all().order_by("-draw_number")[:15]
        serializer = self.get_serializer(pick1_data, many=True)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
