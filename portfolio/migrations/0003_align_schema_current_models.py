# Remplace l’ancien schéma (Category, Contact, etc.) par User + Technology + Project actuels.
# Attention : toute donnée des anciennes tables portfolio_* concernées est supprimée.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_alter_project_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="Project"),
        migrations.DeleteModel(name="Technology"),
        migrations.DeleteModel(name="Category"),
        migrations.DeleteModel(name="Contact"),
        migrations.DeleteModel(name="ImageProjet"),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=255)),
                (
                    "role",
                    models.CharField(
                        choices=[("admin", "Admin"), ("user", "User")],
                        default="user",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="Technology",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, unique=True)),
                (
                    "imageTechnologie",
                    models.URLField(
                        blank=True,
                        help_text="URL de l'image/icone de la technologie",
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("project_name", models.CharField(max_length=200, unique=True)),
                ("project_description", models.TextField()),
                (
                    "technology_used",
                    models.TextField(
                        help_text="Technologies utilisées (séparées par des virgules)"
                    ),
                ),
                (
                    "project_image",
                    models.URLField(help_text="URL de l'image du projet"),
                ),
                ("github_link", models.URLField(blank=True, null=True)),
                ("demo_link", models.URLField(blank=True, null=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-date_creation"],
            },
        ),
    ]
