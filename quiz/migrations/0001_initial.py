# Generated by Django 2.2.10 on 2021-06-27 11:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('type', models.CharField(choices=[('TA', 'Text answer'), ('SC', 'Single choice'), ('MC', 'Multiple choice')], default='TA', max_length=2)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('quiz_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.QuizQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='AnonymousUserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.IntegerField()),
                ('text_answer', models.TextField(null=True)),
                ('multiple_choice', models.ManyToManyField(blank=True, to='quiz.QuizQuestionAnswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='quiz.QuizQuestion')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quiz', to='quiz.Quiz')),
                ('single_choice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers_one_choice', to='quiz.QuizQuestionAnswer')),
            ],
            options={
                'unique_together': {('author', 'question')},
            },
        ),
    ]
