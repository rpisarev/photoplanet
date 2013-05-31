from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add = True)
    message = models.TextField()

    def __unicode__(self):
        return "Feedback by {user} as {name}".format(
            user=self.user, name=self.name
        )
