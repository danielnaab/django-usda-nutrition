"""
Models corresponding to the USDA Nutritional Database tables.

The help text on each field is, in general, a verbatim copy of the text in the
USDA documentation. For more information, view the PDF (data/sr28/sr28_doc.pdf).

Several of the tables corresponding to data sources are included at the end of
this module, but commented out.
"""
from django.db import models


class FoodGroup(models.Model):
    code = models.CharField(max_length=4, primary_key=True, help_text='4-digit code identifying a food group. Only the first 2 digits are currently assigned. In the future, the last 2 digits may be used. Codes may not be consecutive.')
    description = models.CharField(max_length=60, help_text='Name of food group.')

    def __str__(self):
        return self.description


class FoodDescription(models.Model):
    ndb_no = models.CharField(max_length=5, primary_key=True, help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.')
    food_group = models.ForeignKey(FoodGroup, help_text='4-digit code indicating food group to which a food item belongs.')
    long_desc = models.CharField(max_length=200, help_text='200-character description of food item.')
    short_desc = models.CharField(max_length=60, help_text='60-character abbreviated description of food item. Generated from the 200-character description using abbreviations in Appendix A. If short description is longer than 60 characters, additional abbreviations are made.')
    com_name = models.CharField(max_length=100, null=True, blank=True, help_text='Other names commonly used to describe a food, including local or regional names for various foods, for example, “soda” or “pop” for “carbonated beverages.”')
    manufacturer_name = models.CharField(max_length=65, null=True, blank=True, help_text='Indicates the company that manufactured the product, when appropriate.')
    survey = models.NullBooleanField(help_text='Indicates if the food item is used in the USDA Food and Nutrient Database for Dietary Studies (FNDDS) and thus has a complete nutrient profile for the 65 FNDDS nutrients.')
    refuse_description = models.CharField(max_length=135, null=True, blank=True, help_text='Description of inedible parts of a food item (refuse), such as seeds or bone.')
    refuse = models.PositiveSmallIntegerField(null=True, blank=True, help_text='Percentage of refuse.')
    scientific_name = models.CharField(max_length=65, null=True, blank=True, help_text='Scientific name of the food item. Given for the least processed form of the food (usually raw), if applicable.')
    nitrogen_factor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Y Factor for converting nitrogen to protein (see p. 12).')
    protein_factor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Factor for calculating calories from protein (see p. 14).')
    fat_factor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Factor for calculating calories from fat (see p. 14).')
    cho_factor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Factor for calculating calories from carbohydrate (see p. 14).')

    def __str__(self):
        return self.short_desc


class NutrientDefinition(models.Model):
    nutrient_number = models.CharField(primary_key=True, max_length=3, help_text='Unique 3-digit identifier code for a nutrient.')
    units = models.CharField(max_length=7, help_text='Units of measure (mg, g, μg, and so on).')
    tagname = models.CharField(max_length=20, blank=True, null=True, help_text='International Network of Food Data Systems (INFOODS) Tagnames.† A unique abbreviation for a nutrient/food component developed by INFOODS to aid in the interchange of data.')
    nutrient_description = models.CharField(max_length=60, help_text='Name of nutrient/food component.')
    num_decimal_places = models.CharField(max_length=1, help_text='Number of decimal places to which a nutrient value is rounded.')
    sort_order = models.PositiveSmallIntegerField(help_text='Used to sort nutrient records in the same order as various reports produced from SR.')

    def __str__(self):
        return self.nutrient_description


FOOTNOTE_CHOICES = (
    ('D', 'footnote adding information to the food description'),
    ('M', 'footnote adding information to measure description'),
    ('N', 'footnote providing additional information on a nutrient value. If the Footnt_typ = N, the Nutr_No will also be filled in.')
)


class Footnote(models.Model):
    food_description = models.ForeignKey(FoodDescription, related_name='footnotes', help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.')
    footnote_no = models.CharField(max_length=4, help_text='Sequence number. If a given footnote applies to more than one nutrient number, the same footnote number is used. As a result, this file cannot be indexed and there is no primary key.')
    footnote_type = models.CharField(max_length=1, help_text='Type of footnote.', choices=FOOTNOTE_CHOICES)
    nutrient_definition = models.ForeignKey(NutrientDefinition, null=True, help_text='Unique 3-digit identifier code for a nutrient to which footnote applies.')
    footnote_text = models.CharField(max_length=200, help_text='Footnote text.')

    def __str__(self):
        return '%s: %s' % (self.footnote_no, self.footnote_text)


class SourceCode(models.Model):
    source_code = models.CharField(primary_key=True, max_length=2, help_text='A 2-digit code indicating type of data.')
    description = models.CharField(max_length=60, help_text='Description of source code that identifies the type of nutrient data.')

    def __str__(self):
        return '%s: %s' % (self.source_code, self.description)


class DerivationCode(models.Model):
    code = models.CharField(max_length=4, primary_key=True, help_text='Derivation Code.')
    description = models.CharField(max_length=120, help_text='Description of derivation code giving specific information on how the value was determined.')

    def __str__(self):
        return self.code


class Weight(models.Model):
    food_description = models.ForeignKey(FoodDescription, related_name='weights', help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.')
    sequence = models.PositiveSmallIntegerField(help_text='Sequence number.')
    amount = models.DecimalField(max_digits=8, decimal_places=3, help_text='Unit modifier (for example, 1 in “1 cup”).')
    measure_description = models.CharField(max_length=84, help_text='Description (for example, cup, diced, and 1-inch pieces).')
    gram_weight = models.DecimalField(max_digits=8, decimal_places=1, help_text='Gram weight.')
    number_data_points = models.PositiveSmallIntegerField(blank=True, null=True, help_text='Number of data points.')
    standard_deviation = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, help_text='Standard deviation.')

    def __str__(self):
        return '%s %s %s' % (self.amount, self.measure_description, self.food_description)


# class NutrientData(models.Model):
#     food_description = models.ForeignKey(FoodDescription, related_name='nutrient_data', help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.')
#     nutrient_definition = models.ForeignKey(NutrientDefinition, help_text='Unique 3-digit identifier code for a nutrient.')
#     nutrient_value = models.DecimalField(max_digits=13, decimal_places=3, help_text='Amount in 100 grams, edible portion. (Nutrient values have been rounded to a specified number of decimal places for each nutrient. Number of decimal places is listed in the Nutrient Definition file.)')
#     number_data_points = models.PositiveSmallIntegerField(help_text='Number of data points is the number of analyses used to calculate the nutrient value. If the number of data points is 0, the value was calculated or imputed.')
#     standard_error = models.DecimalField(max_digits=11, decimal_places=3, blank=True, null=True, help_text='Standard error of the mean. Null if cannot be calculated. The standard error is also not given if the number of data points is less than three.')
#     source_code = models.ForeignKey(SourceCode, help_text='Code indicating type of data.')
#     derivation_code = models.ForeignKey(DerivationCode, blank=True, null=True, help_text='Data Derivation Code giving specific information on how the value is determined. This field is populated only for items added or updated starting with SR14. This field may not be populated if older records were used in the calculation of the mean value.')
#     ref_food_description = models.ForeignKey(FoodDescription, blank=True, null=True, help_text='NDB number of the item used to calculate a missing value. Populated only for items added or updated starting with SR14.')
#     add_nutr_mark = models.NullBooleanField(help_text='Indicates a vitamin or mineral added for fortification or enrichment. This field is populated for ready-to- eat breakfast cereals and many brand-name hot cereals in food group 08.')
#     num_studies = models.PositiveSmallIntegerField(null=True, blank=True, help_text='Number of studies.')
#     minimum = models.DecimalField(max_digits=13, decimal_places=3, help_text='Minimum value.')
#     maximum = models.DecimalField(max_digits=13, decimal_places=3, help_text='Maximum value.')
#     degrees_of_freedom = models.PositiveSmallIntegerField(null=True, blank=True, help_text='Degrees of freedom.')
#     lower_error_bound = models.DecimalField(max_digits=13, decimal_places=3, help_text='Lower 95% error bound.')
#     upper_error_bound = models.DecimalField(max_digits=13, decimal_places=3, help_text='Upper 95% error bound.')
#     statistical_comments = models.CharField(max_length=10, null=True, blank=True, help_text='Statistical comments. See definitions below.')
#     modified_date = models.CharField(max_length=10, null=True, blank=True, help_text='Indicates when a value was either added to the database or last modified.')
#     confidence_code = models.CharField(max_length=1, null=True, blank=True, help_text='Confidence Code indicating data quality, based on evaluation of sample plan, sample handling, analytical method, analytical quality control, and number of samples analyzed. Not included in this release, but is planned for future releases.')


# class DataSource(models.Model):
#     datasrc_id = models.CharField(max_length=6, primary_key=True, help_text='Unique ID identifying the reference/source.')
#     authors = models.CharField(max_length=255, null=True, blank=True, help_text='List of authors for a journal article or name of sponsoring organization for other documents.')
#     title = models.CharField(max_length=255, help_text='Title of article or name of document, such as a report from a company or trade association.')
#     year = models.CharField(max_length=4, null=True, blank=True, help_text='Year article or document was published.')
#     journal = models.CharField(max_length=135, null=True, blank=True, help_text='Name of the journal in which the article was published.')
#     vol_city = models.CharField(max_length=16, null=True, blank=True, help_text='Volume number for journal articles, books, or reports; city where sponsoring organization is located.')
#     issue_state = models.CharField(max_length=5, null=True, blank=True, help_text='Issue number for journal article; State where the sponsoring organization is located.')
#     start_page = models.CharField(max_length=5, null=True, blank=True, help_text='Starting page number of article/document.')
#     end_page = models.CharField(max_length=5, null=True, blank=True, help_text='Ending page number of article/document.')


# class DataSourceLN(models.Model):
#     #ndb_no = models.ForeignKey(NutrientData, max_length=5, help_text='5-digit Nutrient Databank number that uniquely identifies a food item. If this field is defined as numeric, the leading zero will be lost.')
#     #nutr_no = models.ForeignKey(max_length=3, help_text='Unique 3-digit identifier code for a nutrient.')
#     #datasrc_id = models.ForeignKey(max_length=6, help_text='Unique ID identifying the reference/source.')



# class LanguaLDescription(models.Model):
#     """
#     http://www.langual.org/
#     """
#     pass


# class LanguaL(models.Model):
#     pass
