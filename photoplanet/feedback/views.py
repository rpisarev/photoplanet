from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from .models import Feedback
from .forms import FeedbackForm


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/fb.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FeedbackCreateView, self).form_valid(form)
