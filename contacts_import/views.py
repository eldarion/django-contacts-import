from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from contacts_import.conf import settings


class ImportBeginView(TemplateView):
    
    template_name = "contacts_import/import_begin.html"


class ImportServiceView(FormView):
    
    template_name = "contacts_import/import_service.html"
    
    def dispatch(self, request, *args, **kwargs):
        try:
            Importer = settings.CONTACTS_IMPORT_IMPORTERS[kwargs["service"]]()
        except KeyError:
            raise Http404()
        self.importer = Importer()
        return super(ImportServiceView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["importer"] = self.importer
        return ctx
    
    def get_form_class(self):
        return self.importer.form_class
    
    def get_form(self, form_class):
        if form_class:
            return super(ImportServiceView, self).get_form(form_class)
    
    def form_valid(self, form):
        self.importer.run(form=form)
        return HttpResponse("done")
