# Generated by Django 3.2.7 on 2021-10-28 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_comment_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('regional', 'Regional'), ('scintific', 'Scientific'), ('physics', 'Physics'), ('chemistry', 'Chemistry'), ('mathematics', 'Mathematics'), ('biology', 'Biology'), ('sports', 'Sports'), ('ai', 'AI'), ('offtopic', 'Off-topic'), ('programming', 'Programming'), ('datascience', 'Data Science'), ('entrance_exam', 'Entrance Exam'), ('travel', 'Travel'), ('celebrity_talk', 'Celebrity_talk'), ('world', 'World'), ('astronomy', 'Astronomy'), ('engineering', 'Engineering'), ('technology', 'Technology')], default='off-topic', max_length=15),
        ),
    ]
