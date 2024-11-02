from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee(sender, instance, created, **kwargs):
    if created and instance.role == 'employee':  
        Employee.objects.create(user=instance)
