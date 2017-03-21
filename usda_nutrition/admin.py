from django.contrib import admin

from . import models


class ReadOnlyAdminMixin():
    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


class ReadOnlyAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass


class DerivationCodeAdmin(ReadOnlyAdmin):
    list_display = ('code', 'description')


class FoodDescriptionAdmin(ReadOnlyAdmin):
    list_display = ('ndb_no', 'food_group', 'short_desc')


class FoodGroupAdmin(ReadOnlyAdmin):
    list_display = ('code', 'description')


class FootnoteAdmin(ReadOnlyAdmin):
    list_display = ('pk', 'footnote_no', 'food_description', 'footnote_type')


class NutrientDefinitionAdmin(ReadOnlyAdmin):
    list_display = ('nutrient_number', 'tagname', 'nutrient_description')


class SourceCodeAdmin(ReadOnlyAdmin):
    list_display = ('source_code', 'description')


class WeightAdmin(ReadOnlyAdmin):
    list_display = ('food_description', 'amount', 'measure_description')


admin.site.register(models.DerivationCode, DerivationCodeAdmin)
admin.site.register(models.FoodDescription, FoodDescriptionAdmin)
admin.site.register(models.FoodGroup, FoodGroupAdmin)
admin.site.register(models.Footnote, FootnoteAdmin)
admin.site.register(models.NutrientDefinition, NutrientDefinitionAdmin)
admin.site.register(models.SourceCode, SourceCodeAdmin)
admin.site.register(models.Weight, WeightAdmin)
