from django.shortcuts import render
from django.views import View


class HomePage(View):
    template_name = "homepage/homepage.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)