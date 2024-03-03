from django.db import models
import uuid


class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.payment_id)

