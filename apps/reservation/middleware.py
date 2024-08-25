import re

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class AdminEmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            "/addroom/",
            "/admi/",
            "/listroom/",
            "/list-users/",
            "/list-reserves/",
            "/delete_room/",
            "/update_room/",
            "/delete_booking/",
            "/delete_user/",
        ]
        if (
            request.path in protected_paths
            or re.match(r"^/update_room/\d+/?$", request.path)
            or re.match(r"^/delete_booking/\d+/?$", request.path)
            or re.match(r"^/delete_user/\d+/?$", request.path)
        ):
            if request.user.is_authenticated:
                if request.user.email != "ishimwegraciella17@gmail.com":
                    return HttpResponseRedirect(reverse("home"))
            else:
                messages.warning(
                    request, _("You must be connected to access this page.")
                )
                return HttpResponseRedirect(reverse("login"))

        response = self.get_response(request)
        return response
