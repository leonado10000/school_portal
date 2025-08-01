# Generated by Django 4.2.10 on 2025-07-27 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("people", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubmissionRecord",
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
                ("submission_id", models.CharField(max_length=50)),
                ("add_date", models.DateField(auto_now_add=True)),
                (
                    "associated_batch",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.batch",
                    ),
                ),
                (
                    "associated_subject",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.subject",
                    ),
                ),
                (
                    "associated_teacher",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.teacher",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotebookSubmission",
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
                ("checked_date", models.DateField(blank=True, null=True)),
                ("incomplete_date", models.DateField(blank=True, null=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="people.student"
                    ),
                ),
                (
                    "submission_id",
                    models.ForeignKey(
                        default="sub_1",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notebooks.submissionrecord",
                    ),
                ),
            ],
        ),
    ]
