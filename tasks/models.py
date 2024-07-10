from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel
from invoices.utils import generate_reference
from projects.models import Project

User = get_user_model()


class Task(TimeStampedModel, UniversalIdModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_tasks"
    )
    name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    story_points = models.CharField(max_length=10, blank=True, null=True, unique=True)

    TASK_STATUS = (
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )
    status = models.CharField(max_length=100, choices=TASK_STATUS, default="todo")

    TASK_PRIORITY = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )
    priority = models.CharField(max_length=100, choices=TASK_PRIORITY, default="low")
    due_date = models.DateField()

    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["created_at"]


@receiver(pre_save, sender=Task)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


@receiver(pre_save, sender=Task)
def story_points_pre_save(sender, instance, **kwargs) -> None:
    if instance.story_points is None or instance.story_points == "":
        instance.story_points = generate_reference()
