
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifiedByRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Statistic record',
                'verbose_name_plural': 'Statistic table',
            },
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=256)),
                ('is_busy', models.PositiveIntegerField(default=0)),
                ('classifications_amount', models.PositiveIntegerField(default=0)),
                ('directory_class', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'Directory',
                'verbose_name_plural': 'Directories',
            },
        ),
        migrations.CreateModel(
            name='DirectoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('is_bad', models.BooleanField(default=False)),
                ('dir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Directory')),
            ],
            options={
                'verbose_name': 'Directory Item',
                'verbose_name_plural': 'Directory Items',
            },
        ),
        migrations.CreateModel(
            name='RootDirectory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=256, unique=True)),
                ('dir_100', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Root Directory',
                'verbose_name_plural': 'Root Directories',
            },
        ),
        migrations.AddField(
            model_name='directory',
            name='root_dir',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.RootDirectory'),
        ),
        migrations.AddField(
            model_name='classifiedbyrelation',
            name='dir',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.Directory'),
        ),
        migrations.AddIndex(
            model_name='classifiedbyrelation',
            index=models.Index(fields=['user_id'], name='workspace_c_user_id_b3061d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='classifiedbyrelation',
            unique_together={('dir', 'user_id')},
        ),
    ]
