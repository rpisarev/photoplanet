from django import forms

from .models import Vote


class VoteForm(forms.ModelForm):
    """
    Form for voting in ajax
    """
    def __init__(self, user, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user

    class Meta:
        model = Vote
