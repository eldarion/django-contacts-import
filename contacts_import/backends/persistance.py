from contacts_import.models import Contact


class BasePersistance(object):
    def persist(self, contact, status, credentials):
        if status is None:
            status = self.default_status()
        return self.persist_contact(contact, status, credentials)
    
    def default_status(self):
        return None
    
    def persist_contact(self, contact, status, credentials):
        return None


class ModelPersistance(BasePersistance):
    def default_status(self):
        return {
            "imported": 0,
            "total": 0,
        }
    
    def persist_contact(self, contact, status, credentials):
        obj, created = Contact.objects.get_or_create(user=credentials["user"], 
            email=contact["email"], defaults={"name": contact["name"]})
        status["total"] += 1
        if created:
            status["imported"] += 1
        return status


class InMemoryPersistance(BasePersistance):
    def default_status(self):
        return []
    
    def persist_contact(self, contact, status, credentials):
        status.append(contact)
        return status
