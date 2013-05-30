from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    """
    Model for Photo datail
    """
    photo_id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    user_avatar_url = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    created_time = models.DateTimeField(null=True)
    like_count = models.IntegerField(null=True)
    vote_count = models.IntegerField(default=0)

    def __unicode__ (self):
        return 'Photo by {name}'.format(name=self.username)


class Vote(models.Model):
    """
    Model for voting (rating)
    User from standart auth in django
    """
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    rating = models.IntegerField()

    def save(self):
        """
        Allow only one vote per user per photo.

        Change old vote in database if the same user submits
        another vote for the same photo.
        """

        other_votes = Vote.objects.filter(user=self.user, photo=self.photo).all()
        if other_votes and not other_votes[0].pk == self.pk:
            vote = other_votes[0]
            vote.vote_value = self.vote_value
            vote.save()
        else:
            super(Vote, self).save()

        # update vote count for a photo
        photo = self.photo
        photo.vote_count = Vote.objects.filter(photo=photo).aggregate(
            vote_count=models.Sum('vote_value'))['vote_count']
        photo.save()

    def __unicode__(self):
        return "{rating} from {user}".format(rating=self.rating, user=self.user)
