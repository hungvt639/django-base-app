from rest_framework import generics, status, permissions
from rest_framework.response import Response
from ..models.location import Provincials, Districts, Wards
from ..serializer.location import ListProvincialsSerializer, ProvincialSerializer, DistrictsSerializer


class LocationListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        values = Provincials.objects.all()
        serializer = ListProvincialsSerializer(values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProvincialView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            value = Provincials.objects.get(id=id)
            serializer = ProvincialSerializer(value)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Không có tỉnh này"}, status=status.HTTP_400_BAD_REQUEST)


class DistrictsView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            value = Districts.objects.get(id=id)
            serializer = DistrictsSerializer(value)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Không có quận/huyện này"}, status=status.HTTP_400_BAD_REQUEST)