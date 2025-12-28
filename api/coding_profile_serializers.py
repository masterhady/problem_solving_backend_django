from rest_framework import serializers
from api.coding_platform_models import CodingProfile, LeetCodeAnalysisHistory, Employee, EmployeeGoal

class CodingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class LeetCodeAnalysisHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeetCodeAnalysisHistory
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGoal
        fields = '__all__'
