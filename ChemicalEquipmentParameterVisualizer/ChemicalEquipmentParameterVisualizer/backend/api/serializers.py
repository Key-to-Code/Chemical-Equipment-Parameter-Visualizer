from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    type_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_at', 'total_count', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'type_distribution']
    
    def get_type_distribution(self, obj):
        return obj.get_type_distribution()

class DatasetDetailSerializer(serializers.ModelSerializer):
    type_distribution = serializers.SerializerMethodField()
    csv_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_at', 'total_count', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'type_distribution', 'csv_data']
    
    def get_type_distribution(self, obj):
        return obj.get_type_distribution()
    
    def get_csv_data(self, obj):
        import io
        import csv
        lines = obj.csv_file.strip().split('\n')
        reader = csv.DictReader(lines)
        return list(reader)
