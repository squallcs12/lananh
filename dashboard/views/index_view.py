from django.views.generic.base import TemplateView
from photologue.models import Gallery


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    @staticmethod
    def display_latest_gallery():
        try:
            return {'gallery': Gallery.objects.latest('id')}
        except Gallery.DoesNotExist:
            return {}

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context.update(self.display_latest_gallery())

        return context
