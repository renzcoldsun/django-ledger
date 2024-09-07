"""
Django Ledger created by Miguel Sanda <msanda@arrobalytics.com>.
Copyright© EDMA Group Inc licensed under the GPLv3 Agreement.

Contributions to this module:
Miguel Sanda <msanda@arrobalytics.com>
"""

from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import RedirectView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings as global_settings

from django_ledger.models.entity import EntityModel
from django_ledger.views.mixins import DjangoLedgerSecurityMixIn

class RootUrlView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse('django_ledger:login')
        return reverse('django_ledger:home')


class DashboardView(DjangoLedgerSecurityMixIn, ListView):
    template_name = 'django_ledger/entity/home.html'
    PAGE_TITLE = _('My Dashboard')
    context_object_name = 'entities'
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_subtitle'] = self.request.user.get_full_name()
        context['header_subtitle_icon'] = 'ei:user'
        return context

    def get_queryset(self):
        if global_settings.DJANGO_LEDGER_UTILS:
            po = __import__(global_settings.DJANGO_LEDGER_UTILS)
            utils = po.utils
            e = utils.getEntity()
            UserModel = get_user_model()
            if global_settings.ENTITY_USER:
                user_model = UserModel.objects.get(
                    username__exact=global_settings.ENTITY_USER)
                return EntityModel.objects.for_user(
                    user_model=user_model
                ).order_by('-created')
            else:
                return EntityModel.objects.for_user(
                    user_model=self.request.user
                ).order_by('-created')
        else:
            return EntityModel.objects.for_user(
                user_model=self.request.user
            ).order_by('-created')
