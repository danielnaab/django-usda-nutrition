# django-usda-nutrition

NOTE: [django-usda](https://github.com/notanumber/django-usda) also exists,
and has been tested more than this package.

This is a Django application which includes models corresponding to the USDA
Nutrition Database, as well as import scripts to pull the current version of
the dataset (SR28) into the Django-managed database.

## Dependencies

This packaged has only been tested with Python 3.5 and Django 1.9, but should
work with other versions. Feel free to submit pull requests for compatibility.

## Install

Install from `pip`:

    pip install django-usda-nutrition

## Usage

Add `usda_nutrition` to your `INSTALLED_APPS` and then:

    ./manage.py import_usda

## Notes

- The USDA database includes comprehensive information on how all nutritional
data is calculated and references to the corresponding source datasets. Because
that data is out of scope to use-cases that simply want to include the raw
nutritional content in an application, those tables are not imported with this
package. Nonetheless, the source CSV files, stubbed out models, and references
to them in the import management command and checked in. The corresponding code
is commented out and could be a starting point to anyone wanted to use that
data in a Django app.

- A single bad datapoint from `FOOTNOTE.txt` was manually removed.
