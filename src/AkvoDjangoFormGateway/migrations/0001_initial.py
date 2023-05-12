# Generated by Django 4.2.1 on 2023-05-12 07:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='AkvoGatewayForm',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default=None, null=True)),
                ('version', models.IntegerField(default=1)),
                (
                    'uuid',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
            ],
            options={
                'db_table': 'ag_form',
            },
        ),
        migrations.CreateModel(
            name='AkvoGatewayQuestion',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('order', models.BigIntegerField(default=None, null=True)),
                ('text', models.TextField()),
                (
                    'type',
                    models.IntegerField(
                        choices=[
                            (1, 'Geo'),
                            (2, 'Text'),
                            (3, 'Number'),
                            (4, 'Option'),
                            (5, 'Multiple_Option'),
                            (6, 'Photo'),
                            (7, 'Date'),
                        ]
                    ),
                ),
                ('required', models.BooleanField(default=True)),
                (
                    'form',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ag_form_questions',
                        to='AkvoDjangoFormGateway.akvogatewayform',
                    ),
                ),
            ],
            options={
                'db_table': 'ag_question',
            },
        ),
        migrations.CreateModel(
            name='AkvoGatewayQuestionOption',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('order', models.BigIntegerField(default=None, null=True)),
                (
                    'code',
                    models.CharField(default=None, max_length=255, null=True),
                ),
                ('name', models.TextField()),
                (
                    'question',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ag_question_question_options',
                        to='AkvoDjangoFormGateway.akvogatewayquestion',
                    ),
                ),
            ],
            options={
                'db_table': 'ag_option',
            },
        ),
        migrations.CreateModel(
            name='AkvoGatewayData',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.TextField()),
                ('geo', models.JSONField(default=None, null=True)),
                ('phone', models.CharField(max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=None, null=True)),
                (
                    'form',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ag_form_data',
                        to='AkvoDjangoFormGateway.akvogatewayform',
                    ),
                ),
            ],
            options={
                'db_table': 'ag_data',
            },
        ),
        migrations.CreateModel(
            name='AkvoGatewayAnswer',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.TextField(default=None, null=True)),
                ('value', models.FloatField(default=None, null=True)),
                ('options', models.JSONField(default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=None, null=True)),
                (
                    'data',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ag_data_answer',
                        to='AkvoDjangoFormGateway.akvogatewaydata',
                    ),
                ),
                (
                    'question',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ag_question_answer',
                        to='AkvoDjangoFormGateway.akvogatewayquestion',
                    ),
                ),
            ],
            options={
                'db_table': 'ag_answer',
            },
        ),
    ]