from django.core.urlresolvers import reverse
from settings.settings import is_sell_available, is_purchase_available
from django.http import Http404
import re


class TransactionsAvailableMiddleware:
    def process_request(self, request):
        if re.compile(reverse("sell:index")).match(request.path_info) and not is_sell_available():
            raise Http404

        if re.compile(reverse("purchase:index")).match(request.path_info) and not is_purchase_available():
            raise Http404