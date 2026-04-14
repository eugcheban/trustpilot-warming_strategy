
from django.db import models
from django.utils import timezone

class User(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	proxy_address = models.GenericIPAddressField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	mlx_profile_id = models.CharField(max_length=255, null=True, blank=True)
	

	def __str__(self):
		return self.name or self.email


class UserActivityLog(models.Model):
	class Status(models.TextChoices):
		PENDING = "pending", "Pending"
		IN_PROGRESS = "in_progress", "In progress"
		SUCCESS = "success", "Success"
		FAILED = "failed", "Failed"

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_logs")
	action = models.CharField(max_length=255)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	started_at = models.DateTimeField(default=timezone.now)
	finished_at = models.DateTimeField(null=True, blank=True)
	duration = models.DurationField(null=True, blank=True)
	details = models.TextField(null=True, blank=True)
	error_message = models.TextField(null=True, blank=True)
	metadata = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "User activity log"
		verbose_name_plural = "User activity logs"

	def save(self, *args, **kwargs):
		if self.started_at and self.finished_at:
			self.duration = self.finished_at - self.started_at
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.user} - {self.action} ({self.status})"