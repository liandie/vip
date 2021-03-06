# Generated by Django 2.0 on 2018-08-20 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animename', models.CharField(db_index=True, max_length=49, unique=True, verbose_name='电视名')),
                ('animeource', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='电视源')),
                ('animecount', models.IntegerField(blank=True, default=0, null=True, verbose_name='目前更新集数')),
                ('animegrade', models.CharField(blank=True, default='', max_length=12, null=True, verbose_name='电视等级')),
                ('animelanguage', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='电视语言')),
                ('animetype', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='电视类型')),
                ('animedecade', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='电视年代')),
                ('animeregion', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='电视地区')),
                ('pdate', models.CharField(blank=True, max_length=16, null=True, verbose_name='更新时间')),
                ('animeimageurl', models.CharField(blank=True, max_length=360, null=True, verbose_name='显示图片路径')),
                ('animeurl', models.TextField(blank=True, default='', null=True, verbose_name='电视链接接口集合')),
                ('animeurl2', models.TextField(blank=True, default='', null=True, verbose_name='电视破解链接')),
            ],
        ),
        migrations.CreateModel(
            name='Documentary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentaryname', models.CharField(db_index=True, max_length=49, unique=True, verbose_name='纪录片名')),
                ('documentarysource', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='纪录片源')),
                ('documentarycount', models.IntegerField(blank=True, default=0, null=True, verbose_name='目前更新集数')),
                ('documentarygrade', models.CharField(blank=True, default='', max_length=12, null=True, verbose_name='电视等级')),
                ('documentarylanguage', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='纪录片语言')),
                ('documentarytype', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='纪录片类型')),
                ('documentarydecade', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='纪录片年代')),
                ('documentaryregion', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='纪录片地区')),
                ('pdatetime', models.CharField(blank=True, max_length=16, null=True, verbose_name='更新时间')),
                ('documentaryimageurl', models.TextField(blank=True, default='', null=True, verbose_name='显示图片路径')),
                ('documentaryurl', models.TextField(blank=True, default='', null=True, verbose_name='电视链接接口集合')),
                ('documentaryurl2', models.TextField(blank=True, default='', null=True, verbose_name='电视破解链接')),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moviesname', models.CharField(db_index=True, max_length=49, unique=True, verbose_name='电影名')),
                ('moviessource', models.CharField(blank=True, max_length=9, null=True, verbose_name='电影源')),
                ('moviesgrade', models.CharField(blank=True, max_length=9, null=True, verbose_name='电影等级')),
                ('movieslanguage', models.CharField(blank=True, max_length=9, null=True, verbose_name='电影语言')),
                ('moviestype', models.CharField(blank=True, max_length=36, null=True, verbose_name='电影类型')),
                ('moviesdecade', models.CharField(blank=True, max_length=16, null=True, verbose_name='电影年代')),
                ('moviesregion', models.CharField(blank=True, max_length=25, null=True, verbose_name='电影地区')),
                ('pdatetime', models.CharField(blank=True, max_length=16, null=True, verbose_name='更新时间')),
                ('moviesimageurl', models.CharField(blank=True, max_length=360, null=True, verbose_name='显示图片路径')),
                ('moviesurl', models.CharField(blank=True, max_length=100, null=True, verbose_name='视频链接接口')),
                ('moviesurl2', models.TextField(blank=True, null=True, verbose_name='视频破解链接')),
            ],
        ),
        migrations.CreateModel(
            name='Tvseries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tvname', models.CharField(db_index=True, max_length=49, unique=True, verbose_name='电视名')),
                ('tvource', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='电视源')),
                ('tvcount', models.IntegerField(blank=True, default=0, null=True, verbose_name='目前更新集数')),
                ('tvgrade', models.CharField(blank=True, default='', max_length=12, null=True, verbose_name='电视等级')),
                ('tvlanguage', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='电视语言')),
                ('tvtype', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='电视类型')),
                ('tvdecade', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='电视年代')),
                ('tvregion', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='电视地区')),
                ('pdate', models.CharField(blank=True, max_length=16, null=True, verbose_name='更新时间')),
                ('tvimageurl', models.CharField(blank=True, max_length=360, null=True, verbose_name='显示图片路径')),
                ('tvurl', models.TextField(blank=True, default='', null=True, verbose_name='电视链接接口集合')),
                ('tvurl2', models.TextField(blank=True, default='', null=True, verbose_name='电视破解链接')),
            ],
        ),
        migrations.CreateModel(
            name='Videosum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videosumname', models.CharField(db_index=True, max_length=49, unique=True, verbose_name='电视名')),
                ('videosumource', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='电视源')),
                ('videosumcount', models.IntegerField(blank=True, default=0, null=True, verbose_name='目前更新集数')),
                ('videosumgrade', models.CharField(blank=True, default='', max_length=12, null=True, verbose_name='电视等级')),
                ('videosumlanguage', models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='电视语言')),
                ('videosumtype', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='电视类型')),
                ('videosumdecade', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='电视年代')),
                ('videosumregion', models.CharField(blank=True, default='', max_length=49, null=True, verbose_name='电视地区')),
                ('videosumimageurl', models.CharField(blank=True, max_length=360, null=True, verbose_name='显示图片路径')),
                ('videosumurl', models.TextField(blank=True, default='', null=True, verbose_name='电视链接接口集合')),
                ('videosumurl2', models.TextField(blank=True, default='', null=True, verbose_name='电视破解链接')),
                ('pdatetime', models.CharField(blank=True, max_length=16, null=True, verbose_name='更新时间')),
            ],
        ),
    ]
