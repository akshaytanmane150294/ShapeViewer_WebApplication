from django.db import models

# class Prism(models.Model):
#     name = models.CharField(max_length=100)     # Prism ka naam jaise "Cube", "Cylinder"
#     type = models.CharField(max_length=100,default='Rectangular')     # Plugin ka type
#     height = models.FloatField(null=True, blank=True)
#     width = models.FloatField(null=True, blank=True)
#     length = models.FloatField(null=True, blank=True)
#     radius = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.name} ({self.type})"
    
class Prism(models.Model):
    designation = models.CharField(max_length=50,default='L40B20H100')        # 'L40B20H100'
    length = models.FloatField(null=True, blank=True)                          # 40.0
    width = models.FloatField(null=True, blank=True)                           # 20.0
    height = models.FloatField(null=True, blank=True)    # NULL allowed
    radius = models.FloatField(null=True, blank=True)    # 100.0
    prism_name = models.CharField(max_length=50,default='rectangular')         # 'rectangular'

    def __str__(self):
        return f"{self.designation} ({self.prism_name})"

