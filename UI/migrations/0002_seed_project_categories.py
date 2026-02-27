from django.db import migrations
from django.utils.text import slugify


def seed_project_categories(apps, schema_editor):
    ProjectCategory = apps.get_model("UI", "ProjectCategory")
    default_categories = [
        "Residential",
        "Commercial",
        "Kitchen",
        "Ceiling",
        "Interior",
        "Exterior",
        "Bathroom",
        "Living Room",
        "Office",
        "Renovation",
    ]

    for name in default_categories:
        ProjectCategory.objects.get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )


def unseed_project_categories(apps, schema_editor):
    ProjectCategory = apps.get_model("UI", "ProjectCategory")
    slugs = [
        "residential",
        "commercial",
        "kitchen",
        "ceiling",
        "interior",
        "exterior",
        "bathroom",
        "living-room",
        "office",
        "renovation",
    ]
    ProjectCategory.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("UI", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_project_categories, unseed_project_categories),
    ]
