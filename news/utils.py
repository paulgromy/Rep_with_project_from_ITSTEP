from django.urls import reverse_lazy


class DataMixin:
    def get_success_url(self):
        return reverse_lazy('Main')
