from celery.task import tasks

from contacts_import.backends import importers


tasks.register(importers.VcardImporter)
tasks.register(importers.GoogleImporter)
tasks.register(importers.YahooImporter)