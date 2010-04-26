from contacts_import.models import TransientContact


class BasePersistance(object):
    def persist(self, contact, status, credentials):
        if status is None:
            status = self.default_status()
        return self.persist_contact(contact, status, credentials)
    
    def persist_contact(self, contact, status, credentials):
        return status


class ModelPersistance(BasePersistance):
    
    def persist_contact(self, contact, status, credentials):
        obj, created = TransientContact.objects.get_or_create(
            owner = credentials["user"],
            email = contact["email"],
            defaults = {"name": contact["name"]}
        )
        status["total"] += 1
        if created:
            status["imported"] += 1
        return status


class InMemoryPersistance(BasePersistance):
    
    def persist_contact(self, contact, status, credentials):
        # @@@ no longer works (need to conform to status contract which could
        # be done by adding a new key or emulating a dict and store contacts
        # that way)
        return status
