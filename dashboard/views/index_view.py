from django.views.generic.base import TemplateView
from photologue.models import Gallery


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    @staticmethod
    def display_latest_gallery():
        gallery = Gallery.objects.latest('id')
        if gallery:
            return {'gallery': gallery}
        return {}

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context.update(self.display_latest_gallery())

        return context
