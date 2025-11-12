from django.db import models
from django.contrib.auth.models import User
import json

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    csv_file = models.TextField()
    
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    equipment_type_distribution = models.TextField(default='{}')
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_type_distribution(self):
        return json.loads(self.equipment_type_distribution)
    
    def set_type_distribution(self, distribution_dict):
        self.equipment_type_distribution = json.dumps(distribution_dict)
