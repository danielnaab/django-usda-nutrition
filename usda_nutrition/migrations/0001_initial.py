# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-21 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DerivationCode',
            fields=[
                ('code', models.CharField(help_text='Derivation Code.', max_length=4, primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='Description of derivation code giving specific information on how the value was determined.', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='FoodDescription',
            fields=[
                ('ndb_no', models.CharField(help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.', max_length=5, primary_key=True, serialize=False)),
                ('long_desc', models.CharField(help_text='200-character description of food item.', max_length=200)),
                ('short_desc', models.CharField(help_text='60-character abbreviated description of food item. Generated from the 200-character description using abbreviations in Appendix A. If short description is longer than 60 characters, additional abbreviations are made.', max_length=60)),
                ('com_name', models.CharField(blank=True, help_text='Other names commonly used to describe a food, including local or regional names for various foods, for example, “soda” or “pop” for “carbonated beverages.”', max_length=100, null=True)),
                ('manufacturer_name', models.CharField(blank=True, help_text='Indicates the company that manufactured the product, when appropriate.', max_length=65, null=True)),
                ('survey', models.NullBooleanField(help_text='Indicates if the food item is used in the USDA Food and Nutrient Database for Dietary Studies (FNDDS) and thus has a complete nutrient profile for the 65 FNDDS nutrients.')),
                ('refuse_description', models.CharField(blank=True, help_text='Description of inedible parts of a food item (refuse), such as seeds or bone.', max_length=135, null=True)),
                ('refuse', models.PositiveSmallIntegerField(blank=True, help_text='Percentage of refuse.', null=True)),
                ('scientific_name', models.CharField(blank=True, help_text='Scientific name of the food item. Given for the least processed form of the food (usually raw), if applicable.', max_length=65, null=True)),
                ('nitrogen_factor', models.DecimalField(blank=True, decimal_places=2, help_text='Y Factor for converting nitrogen to protein (see p. 12).', max_digits=6, null=True)),
                ('protein_factor', models.DecimalField(blank=True, decimal_places=2, help_text='Factor for calculating calories from protein (see p. 14).', max_digits=6, null=True)),
                ('fat_factor', models.DecimalField(blank=True, decimal_places=2, help_text='Factor for calculating calories from fat (see p. 14).', max_digits=6, null=True)),
                ('cho_factor', models.DecimalField(blank=True, decimal_places=2, help_text='Factor for calculating calories from carbohydrate (see p. 14).', max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodGroup',
            fields=[
                ('code', models.CharField(help_text='4-digit code identifying a food group. Only the first 2 digits are currently assigned. In the future, the last 2 digits may be used. Codes may not be consecutive.', max_length=4, primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='Name of food group.', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Footnote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('footnote_no', models.CharField(help_text='Sequence number. If a given footnote applies to more than one nutrient number, the same footnote number is used. As a result, this file cannot be indexed and there is no primary key.', max_length=4)),
                ('footnote_type', models.CharField(choices=[('D', 'footnote adding information to the food description'), ('M', 'footnote adding information to measure description'), ('N', 'footnote providing additional information on a nutrient value. If the Footnt_typ = N, the Nutr_No will also be filled in.')], help_text='Type of footnote.', max_length=1)),
                ('footnote_text', models.CharField(help_text='Footnote text.', max_length=200)),
                ('food_description', models.ForeignKey(help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.', on_delete=django.db.models.deletion.CASCADE, to='usda_nutrition.FoodDescription')),
            ],
        ),
        migrations.CreateModel(
            name='NutrientDefinition',
            fields=[
                ('nutrient_number', models.CharField(help_text='Unique 3-digit identifier code for a nutrient.', max_length=3, primary_key=True, serialize=False)),
                ('units', models.CharField(help_text='Units of measure (mg, g, μg, and so on).', max_length=7)),
                ('tagname', models.CharField(blank=True, help_text='International Network of Food Data Systems (INFOODS) Tagnames.† A unique abbreviation for a nutrient/food component developed by INFOODS to aid in the interchange of data.', max_length=20, null=True)),
                ('nutrient_description', models.CharField(help_text='Name of nutrient/food component.', max_length=60)),
                ('num_decimal_places', models.CharField(help_text='Number of decimal places to which a nutrient value is rounded.', max_length=1)),
                ('sort_order', models.PositiveSmallIntegerField(help_text='Used to sort nutrient records in the same order as various reports produced from SR.')),
            ],
        ),
        migrations.CreateModel(
            name='SourceCode',
            fields=[
                ('source_code', models.CharField(help_text='A 2-digit code indicating type of data.', max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='Description of source code that identifies the type of nutrient data.', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveSmallIntegerField(help_text='Sequence number.')),
                ('amount', models.DecimalField(decimal_places=3, help_text='Unit modifier (for example, 1 in “1 cup”).', max_digits=8)),
                ('measure_description', models.CharField(help_text='Description (for example, cup, diced, and 1-inch pieces).', max_length=84)),
                ('gram_weight', models.DecimalField(decimal_places=1, help_text='Gram weight.', max_digits=8)),
                ('number_data_points', models.PositiveSmallIntegerField(blank=True, help_text='Number of data points.', null=True)),
                ('standard_deviation', models.DecimalField(blank=True, decimal_places=3, help_text='Standard deviation.', max_digits=10, null=True)),
                ('food_description', models.ForeignKey(help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.', on_delete=django.db.models.deletion.CASCADE, to='usda_nutrition.FoodDescription')),
            ],
        ),
        migrations.AddField(
            model_name='footnote',
            name='nutrient_definition',
            field=models.ForeignKey(help_text='Unique 3-digit identifier code for a nutrient to which footnote applies.', null=True, on_delete=django.db.models.deletion.CASCADE, to='usda_nutrition.NutrientDefinition'),
        ),
        migrations.AddField(
            model_name='fooddescription',
            name='food_group',
            field=models.ForeignKey(help_text='4-digit code indicating food group to which a food item belongs.', on_delete=django.db.models.deletion.CASCADE, to='usda_nutrition.FoodGroup'),
        ),
    ]
