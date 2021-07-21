from rest_framework import serializers
from ..models.location import Provincials, Districts, Wards


class ListProvincialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincials
        fields = ['id', 'code', 'name']


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = Districts
        fields = ['id', 'name']


class ProvincialSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Provincials
        fields = ['id', 'code', 'name', 'districts']


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wards
        fields = ['id', 'name', 'prefix']


class DistrictsSerializer(serializers.ModelSerializer):
    wards = WardSerializer(read_only=True, many=True)

    class Meta:
        model = Districts
        fields = ['id', 'name', 'wards']