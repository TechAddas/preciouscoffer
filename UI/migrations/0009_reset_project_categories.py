from django.db import migrations
from django.utils.text import slugify


def reset_project_categories(apps, schema_editor):
    ProjectCategory = apps.get_model("UI", "ProjectCategory")
    categories = [
        "Basement",
        "Extension",
        "Outbuilding",
        "Refurbishment",
    ]

    ProjectCategory.objects.all().delete()

    for name in categories:
        ProjectCategory.objects.create(name=name, slug=slugify(name))


def noop_reverse(apps, schema_editor):
    # Keep current categories on reverse; no-op by design.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("UI", "0008_rename_project_story_fields"),
    ]

    operations = [
        migrations.RunPython(reset_project_categories, noop_reverse),
    ]
