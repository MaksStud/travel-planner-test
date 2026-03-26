from django.db import models
from rest_framework.serializers import ValidationError


class Project(models.Model):
    """Project model."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date', '-id']

    def delete(self, *args, **kwargs):
        """Delete project."""
        if self.places.filter(is_visited=True).exists():
            raise ValidationError("Cannot delete project: some places are already visited.")
        return super().delete(*args, **kwargs)

    def sync_status(self):
        """
        Sync project status.

        If all places are visited, set project to completed.
        If some places are not visited, set project to not completed.

        """
        places = self.places.all()
        if places.exists() and all(p.is_visited for p in places):
            if not self.is_completed:
                self.is_completed = True
                self.save(update_fields=['is_completed'])
        else:
            if self.is_completed:
                self.is_completed = False
                self.save(update_fields=['is_completed'])

    def __str__(self):
        return self.name


class Place(models.Model):
    """Place model."""
    external_id = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='places', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('external_id', 'project')

    def clean(self):
        if not self.pk and self.project.places.count() >= 10:
            raise ValidationError("Maximum 10 places per project allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.project.sync_status()

    def __str__(self):
        return f"{self.external_id} ({self.project.name})"
