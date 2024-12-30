from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class RecordLedgers(BaseModel):
    title = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class EntryQueue(BaseModel):
    record_ledgers= models.ForeignKey(RecordLedgers, on_delete=models.SET_NULL, null=True)
    column_title = models.CharField(max_length=10, blank=False, null=True)

    
class EntryValue(BaseModel):
    column = models.ForeignKey(EntryQueue, related_name="entryvaluechild", on_delete=models.SET_NULL, null=True)
    entries_value =  models.CharField(max_length=50, blank=True, null=True)
