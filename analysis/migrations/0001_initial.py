# Generated by Django 4.2.16 on 2024-09-16 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("username", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("full_name", models.CharField(max_length=255)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "profile_picture",
                    models.ImageField(blank=True, null=True, upload_to="profiles/"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Visitor", "Visitor"),
                            ("Staff", "Staff"),
                            ("Admin", "Admin"),
                        ],
                        max_length=50,
                    ),
                ),
                ("access_level", models.IntegerField(default=1)),
                ("last_recognition_time", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                (
                    "face_image",
                    models.ImageField(blank=True, null=True, upload_to="face_images/"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="custom_user_set", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True, related_name="custom_user_set", to="auth.permission"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
