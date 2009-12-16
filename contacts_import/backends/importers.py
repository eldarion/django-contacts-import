import httplib2
import vobject
import ybrowserauth

from django.conf import settings
from django.utils import simplejson as json

from celery.task import Task


class BaseImporter(Task):
    def run(self, credentials, persistance):
        status = None
        for contact in self.get_contacts(credentials):
            status = persistance.persist(contact, status, credentials)
        return status


class VcardImporter(BaseImporter):
    def get_contacts(self, credentials):
        for card in vobject.readComponents(credentials["stream"]):
            try:
                yield {
                    "email": card.email.value,
                    "name": card.fn.value
                }
            except AttributeError:
                # if a person doesn"t have an email or a name ignore them
                continue


class YahooImporter(BaseImporter):
    def get_contacts(self, credentials):
        ybbauth = ybrowserauth.YBrowserAuth(settings.BBAUTH_APP_ID, 
            settings.BBAUTH_SHARED_SECRET)
        ybbauth.token = credentials["bbauth_token"]
        address_book_json = ybbauth.makeAuthWSgetCall("http://address.yahooapis.com/v1/searchContacts?format=json&email.present=1&fields=name,email")
        address_book = json.loads(address_book_json)
        
        for contact in address_book["contacts"]:
            email = contact["fields"][0]["data"]
            try:
                first_name = contact["fields"][1]["first"]
            except (KeyError, IndexError):
                first_name = None
            
            try:
                last_name = contact["fields"][1]["last"]
            except (KeyError, IndexError):
                last_name = None
            
            if first_name and last_name:
                name = "%s %s" % (first_name, last_name)
            elif first_name:
                name = first_name
            elif last_name:
                name = last_name
            else:
                name = ""
            
            yield {
                "email": email,
                "name": name,
            }


GOOGLE_CONTACTS_URI = "http://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=1000"


class GoogleImporter(BaseImporter):
    def get_contacts(self, credentials):
        h = httplib2.Http()
        response, content = h.request(GOOGLE_CONTACTS_URI, headers={
            "Authorization": 'AuthSub token="%s"' % credentials["authsub_token"]
        })
        if response.status != 200:
            return
        results = json.loads(content)
        for person in results["feed"]["entry"]:
            for email in person.get("gd$email", []):
                yield {
                    "name": person["title"]["$t"],
                    "email": email["address"],
                }
