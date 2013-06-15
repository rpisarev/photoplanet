from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    """
    Model for Photo detail
    """
    photo_id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=100)
    user_avatar_url = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    created_time = models.DateTimeField(null=True)
    like_count = models.IntegerField(null=True)
    vote_count = models.IntegerField(default=0)
    is_spam = models.BooleanField(default=False)

    def __unicode__(self):
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

        other_votes = Vote.objects.filter(
            user=self.user, photo=self.photo
        ).all()
        if other_votes and not other_votes[0].pk == self.pk:
            vote = other_votes[0]
            vote.rating = self.rating
            vote.save()
        else:
            super(Vote, self).save()

        # update vote count for a photo
        Photo.objects.filter(photo_id=self.photo_id).update(
            vote_count=Vote.objects.filter(photo=self.photo).aggregate(
                vote_count=models.Sum('rating'))['vote_count']
        )

    def __unicode__(self):
        return "{rating} from {user}".format(
            rating=self.rating, user=self.user
        )
