from django.db import migrations, models
import django.db.models.deletion


def migrate_image_categories_to_single(apps, schema_editor):
    ProjectImage = apps.get_model("UI", "ProjectImage")
    through_model = ProjectImage.categories.through

    first_category_by_image = {}
    for image_id, category_id in through_model.objects.order_by(
        "projectimage_id", "projectcategory_id"
    ).values_list("projectimage_id", "projectcategory_id"):
        if image_id not in first_category_by_image:
            first_category_by_image[image_id] = category_id

    for image in ProjectImage.objects.all():
        category_id = first_category_by_image.get(image.id)
        if category_id:
            image.category_id = category_id
            image.save(update_fields=["category"])


class Migration(migrations.Migration):

    dependencies = [
        ("UI", "0009_reset_project_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectimage",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="project_images",
                to="UI.projectcategory",
            ),
        ),
        migrations.RunPython(migrate_image_categories_to_single, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="projectimage",
            name="categories",
        ),
    ]
