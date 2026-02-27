from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("UI", "0007_alter_project_unique_vision_goal_1_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="unique_vision_goal_1",
            new_name="the_vision",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="unique_vision_goal_2",
            new_name="the_brief",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="unique_vision_goal_3",
            new_name="the_transformation",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="unique_vision_goal_4",
            new_name="the_outcome",
        ),
    ]
