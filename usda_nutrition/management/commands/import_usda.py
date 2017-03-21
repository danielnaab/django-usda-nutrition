import csv
import os
import sys

from django.db import models, transaction
from django.core.management.base import BaseCommand

from usda_nutrition import models as usda


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data/sr28')


INPUT_FILES = (
    {
        'filename': 'DERIV_CD.txt',
        'model': usda.DerivationCode,
        'fields': ['code', 'description']
    }, {
        'filename': 'FD_GROUP.txt',
        'model': usda.FoodGroup,
        'fields': ['code', 'description']
    }, {
        'filename': 'FOOD_DES.txt',
        'model': usda.FoodDescription,
        'fields': ['ndb_no', 'food_group_id', 'long_desc', 'short_desc', 'com_name', 'manufacturer_name', 'survey']
    }, {
        'filename': 'WEIGHT.txt',
        'model': usda.Weight,
        'fields': ['food_description_id', 'sequence', 'amount', 'measure_description', 'gram_weight', 'number_data_points', 'standard_deviation']
    }, {
        'filename': 'SRC_CD.txt',
        'model': usda.SourceCode,
        'fields': ['source_code', 'description']
    }, {
        'filename': 'NUTR_DEF.txt',
        'model': usda.NutrientDefinition,
        'fields': ['nutrient_number', 'units', 'tagname', 'nutrient_description', 'num_decimal_places', 'sort_order']
    }, {
        'filename': 'FOOTNOTE.txt',
        'model': usda.Footnote,
        'fields': ['food_description_id', 'footnote_no', 'footnote_type', 'nutrient_definition_id', 'footnote_text']
    }
    # These tables aren't currently imported, as the corresponding models are
    # commented out of models.py.
    # }, {
    #     'filename': 'NUT_DATA.txt',
    #     'model': usda.NutrientData,
    #     'fields': ['food_description_id', 'nutrient_definition_id', 'nutrient_value', 'number_data_points', 'standard_error', 'source_code_id', 'derivation_code_id', 'ref_food_description_id', 'add_nutr_mark', 'num_studies', 'minimum', 'maximum', 'degrees_of_freedom', 'lower_error_bound', 'upper_error_bound', 'statistical_comments', 'modified_date', 'confidence_code']
    # }, {
    # {
    #     'filename': 'DATA_SRC.txt',
    #     'model': usda.DataSource,
    #     'fields': ['datasrc_id', 'authors', 'title', 'year', 'journal', 'vol_city', 'issue_state', 'start_page', 'end_page']
    # }, {
    #     'filename': 'DATSRCLN.txt',
    #     'model': usda.DataSourceLN,
    #     'fields': []
    # }, {
    #     'filename': 'LANGDESC.txt',
    #     'model': usda.LanguaLDescription,
    #     'fields': []
    # }, {
    #     'filename': 'LANGUAL.txt',
    #     'model': usda.LanguaL,
    #     'fields': []
)


def value_for_field(field, value):
    # Convert Y/N into a boolean.
    if type(field) == models.BooleanField:
        return {
            'Y': True,
            'N': False,
            '': None
        }[value]

    # Return the value, coercing empty strings to None.
    return value or None

def import_file(filename, model_cls, field_list):
    sys.stdout.write('Importing %s... ' % filename)
    sys.stdout.flush()

    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding='cp1252') as csvfile:
        new_instances = []
        reader = csv.reader(csvfile, delimiter='^', quotechar='~')
        for row in reader:
            new_instance = model_cls()
            for index, field in enumerate(field_list):
                value = value_for_field(model_cls._meta.get_field(field), row[index])
                setattr(new_instance, field, value)
            new_instances.append(new_instance)
        model_cls.objects.bulk_create(new_instances)

    print('Done!')


@transaction.atomic
def run():
    for info in INPUT_FILES:
        import_file(info['filename'], info['model'], info['fields'])

class Command(BaseCommand):
    help = 'Imports the USDA Nutrition Database (version SR28)'

    def handle(self, *args, **options):
        run()
