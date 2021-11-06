from rest_framework import serializers
from scanner.models import Repo_Dependency_Pair, Dependency

class Repo_Dependency_Pair_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Repo_Dependency_Pair
        fields = '__all__'


class Dependency_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = '__all__'