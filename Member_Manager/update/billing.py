#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TouSIX-Manager is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.views.generic.edit import UpdateView
from Member_Manager.forms.billing import BillingForm
from Authentication.LoginMixin import LoginRequiredMixin
from Database.models import Contact, UserMembre
from django.contrib.messages.views import SuccessMessageMixin
from Member_Manager.update.UpdateMixin import UpdateUrlMixin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class BillingUpdateView(LoginRequiredMixin, UpdateView, UpdateUrlMixin, SuccessMessageMixin):
    """
    This view updates billing contact associated with the requesting user.
    """
    model = Contact
    form_class = BillingForm
    template_name = "update_member.html"
    success_url = "/member/update"
    success_message = "Changement contact facturation enregistré."
    context_object_name = "billing"

    def get_object(self, queryset=None):
        return UserMembre.objects.filter(user=self.request.user).first().membre.billing

    def get_form(self, form_class=None):
        return BillingForm(instance=self.get_object(), prefix="billing")

    def get(self, request, *args, **kwargs):
        return redirect(reverse("update member"))

    def form_valid(self, form):
        form.save()
        return redirect(reverse("update member"))

    def form_invalid(self, form):
        return self.render_to_response(self.create_context_data({"billing": form}))

    def post(self, request, *args, **kwargs):
        billing = BillingForm(data=request.POST, instance=self.get_object(), prefix="billing")

        if billing.is_valid():
            return self.form_valid(billing)
        else:
            return self.form_invalid(billing)