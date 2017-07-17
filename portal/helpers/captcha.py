# -*- coding: utf-8 -*-
# Code for Life
#
# Copyright (C) 2017, Ocado Innovation Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ADDITIONAL TERMS – Section 7 GNU General Public Licence
#
# This licence does not grant any right, title or interest in any “Ocado” logos,
# trade names or the trademark “Ocado” or any other trademarks or domain names
# owned by Ocado Innovation Limited or the Ocado group of companies or any other
# distinctive brand features of “Ocado” as may be secured from time to time. You
# must not distribute any modification of this program using the trademark
# “Ocado” or claim any affiliation or association with Ocado or its employees.
#
# You are not authorised to use the name Ocado (or any of its trade names) or
# the names of any author or contributor in advertising or for publicity purposes
# pertaining to the distribution of this program, without the prior written
# authorisation of Ocado.
#
# Any propagation, distribution or conveyance of this program must include this
# copyright notice and these terms. You must not misrepresent the origins of this
# program; modified versions of the program must be marked as such and not
# identified as the original program.
from portal import app_settings
import requests


# Adapted from https://djangopy.org/how-to/making-django-form-google-recaptcha-powered/, accessed on 28 June 2017
def check_recaptcha(request):
    get_request = request.POST.get("g-recaptcha-response")
    url = "https://www.google.com/recaptcha/api/siteverify"
    my_param = {
        'secret': app_settings.RECAPTCHA_PRIVATE_KEY,
        'response': get_request,
        'remoteip': get_client_ip(request)
    }
    verify_plain = requests.get(url, params=my_param, verify=True)
    print str(verify_plain)
    print str(verify_plain.content)
    verify_plain.raise_for_status()
    verify = verify_plain.json()
    print str(verify)
    status = verify.get("success", False)
    return status


# From https://djangopy.org/how-to/making-django-form-google-recaptcha-powered/, accessed on 28 June 2017
def get_client_ip(request):
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if client_ip:
        ip = client_ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
