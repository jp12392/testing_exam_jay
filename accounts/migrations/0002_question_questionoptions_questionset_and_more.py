# Generated by Django 4.1.2 on 2022-10-15 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='question/')),
                ('type', models.CharField(choices=[('Radio', 'Radio'), ('CheckBox', 'CheckBox'), ('Matrix', 'Matrix')], default='Radio', max_length=15)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('marks', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'questions',
                'ordering': ('-created_on',),
            },
        ),
        migrations.CreateModel(
            name='QuestionOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='question/options/')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('marks', models.IntegerField(blank=True, null=True)),
                ('answer', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'question_options',
                'ordering': ('-created_on',),
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('enable_negative_marking', models.BooleanField(default=False)),
                ('negative_marking_percentage', models.IntegerField(blank=True, null=True)),
                ('ideal_timeto_complete', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'questions_set',
                'ordering': ('-created_on',),
            },
        ),
        migrations.AddIndex(
            model_name='questionset',
            index=models.Index(fields=['name', 'slug'], name='questions_s_name_4457f2_idx'),
        ),
        migrations.AddField(
            model_name='questionoptions',
            name='question',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.question'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_set',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.questionset'),
        ),
        migrations.AddIndex(
            model_name='questionoptions',
            index=models.Index(fields=['question'], name='question_op_questio_dc3834_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['question_set'], name='questions_questio_690a3b_idx'),
        ),
    ]
