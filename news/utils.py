from django.urls import reverse_lazy


class DataMixin:
    paginate_by = 3
    def get_success_url(self):
        return reverse_lazy('Main')
