from django.db import models

class Question(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.text
