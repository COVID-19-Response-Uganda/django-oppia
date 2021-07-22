import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import FormView, TemplateView
from tastypie.models import ApiKey
from django.http import HttpResponse

import profile
from helpers.mixins.PermissionMixins import AdminRequiredMixin
from oppia.models import Points, Award, Tracker
from profile.forms import UploadProfileForm, \
    UserSearchForm, \
    DeleteAccountForm
from profile.models import UserProfile, CustomField, UserProfileCustomField
from profile.views.utils import get_paginated_users, \
    get_filters_from_row, \
    get_query
from quiz.models import QuizAttempt, QuizAttemptResponse

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


@staff_member_required
def search_users(request):
    users = User.objects

    filtered = False
    search_form = UserSearchForm(request.GET, request.FILES)
    if search_form.is_valid():
        filters = get_filters_from_row(search_form)
        if filters:
            users = users.filter(**filters)
            filtered = True

    if not filtered:
        users = users.all()

    query_string = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        filter_query = get_query(query_string, ['username',
                                                'first_name',
                                                'last_name',
                                                'email', ])
        users = users.filter(filter_query)

    ordering = request.GET.get('order_by', None)
    if ordering is None:
        ordering = 'first_name'

    users = users.order_by(ordering)
    paginator = Paginator(users, profile.SEARCH_USERS_RESULTS_PER_PAGE)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)

    return render(request, 'profile/search_user.html',
                  {'quicksearch': query_string,
                   'search_form': search_form,
                   'advanced_search': filtered,
                   'page': users,
                   'page_ordering': ordering})


@staff_member_required
def export_users(request):

    ordering, users = get_paginated_users(request)
    for user in users:
        try:
            user.apiKey = user.api_key.key
        except ApiKey.DoesNotExist:
            # if the user doesn't have an apiKey yet, generate it
            user.apiKey = ApiKey.objects.create(user=user).key

    template = 'export-users.html'
    if request.is_ajax():
        template = 'users-paginated-list.html'

    return render(request, 'profile/' + template,
                  {'page': users,
                   'page_ordering': ordering,
                   'users_list_template': 'export'})

@staff_member_required
def export_all_users(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="allusers.csv"' 
    writer = csv.writer(response)
    # write the header first
    heading = ["First Name", "Last Name", "Username", "Email",  "Phone Number", "Registration Date"]
    # add custom field labels to heading
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    custom_fields = CustomField.objects.all()
    for custom_field in custom_fields:
        heading.append(custom_field.label)
    writer.writerow(heading)
    
    for user in users:
        mylist = []
        mylist.append(user.first_name)
        mylist.append(user.last_name)
        mylist.append(user.username)
        mylist.append(user.email)
        mylist.append(user.userprofile.phone_number)
        datejoined = user.date_joined
        datestr = datejoined.strftime("%d/%m/%Y")
        mylist.append(datestr)
       
        # add custom fields
        for custom_field in custom_fields:
            try:
                row = UserProfileCustomField.objects.get(key_name=custom_field, user=user)
                # print(row.value_str)
                mylist.append(row.value_str)
            except ObjectDoesNotExist:
                row = None
                mylist.append(row)
                # print(row)
        writer.writerow(mylist)

    return response



@staff_member_required
def list_users(request):
    ordering, users = get_paginated_users(request)
    return render(request, 'profile/users-paginated-list.html',
                  {'page': users,
                   'page_ordering': ordering,
                   'users_list_template': 'select',
                   'ajax_url': request.path})


def delete_user_data(delete_user):
    # delete points
    Points.objects.filter(user=delete_user).delete()

    # delete badges
    Award.objects.filter(user=delete_user).delete()

    # delete trackers
    Tracker.objects.filter(user=delete_user).delete()

    # delete quiz attempts
    QuizAttemptResponse.objects \
        .filter(quizattempt__user=delete_user).delete()
    QuizAttempt.objects.filter(user=delete_user).delete()

    # delete profile
    UserProfile.objects.filter(user=delete_user).delete()

    # delete api key
    ApiKey.objects.filter(user=delete_user).delete()

    # logout and delete user
    User.objects.get(pk=delete_user.id).delete()


def delete_account_view(request, user_id):
    if request.method == 'POST':  # if form submitted...
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            posted_user = User.objects.get(pk=user_id)

            if user.is_superuser or user.id == user_id:
                delete_user = posted_user
            else:
                raise PermissionDenied

            delete_user_data(delete_user)

            # redirect
            return HttpResponseRedirect(
                reverse('profile:delete_complete'))
    else:
        form = DeleteAccountForm(initial={'username': request.user.username})

    return render(request, 'profile/delete_account.html',
                  {'form': form})


class DeleteAccountComplete(TemplateView):
    template_name = 'profile/delete_account_complete.html'


class UploadUsers(AdminRequiredMixin, FormView):

    form_class = UploadProfileForm
    template_name = 'profile/upload.html'

    def form_valid(self, form):
        csv_file = csv.DictReader(
            chunk.decode() for chunk in self.request.FILES['upload_file'])
        required_fields = ['username', 'firstname', 'lastname']

        context = self.get_context_data(form=form)
        context['results'] = self.process_upload_user_file(csv_file,
                                                           required_fields)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_fields"] = CustomField.objects.all().order_by('order')
        return context
    
    def process_upload_user_file(self, csv_file, required_fields):
        results = []
        try:
            for row in csv_file:
                # check all required fields defined
                all_defined = True
                for rf in required_fields:
                    if rf not in row or row[rf].strip() == '':
                        result = {
                            'username': row.get('username', None),
                            'created': False,
                            'message': _(u'No %s set' % rf)
                        }
                        results.append(result)
                        all_defined = False

                if not all_defined:
                    continue

                results.append(self.process_upload_file_save_user(row))

        except Exception:
            result = {
                'username': None,
                'created': False,
                'message': _(u'Could not parse file')
            }
            results.append(result)

        return results

    def process_upload_file_save_user(self, row):
        user, user_created = User.objects.get_or_create(username=row['username'])
        user.first_name = row['firstname']
        user.last_name = row['lastname']

        if 'email' in row:
            user.email = row['email']

        auto_password = False
        if 'password' in row:
            password = row['password']
        else:
            password = User.objects.make_random_password()
            auto_password = True

        user.set_password(password)
        user.save()

        self.update_user_profile(user, row)

        # update CustomFields
        self.update_custom_fields(user, row)
        
        result = {
            'created': user_created,
            'username': row['username'],
        }
        if auto_password and user_created:
            result['message'] = _(u'User created with password: %s' % password)
        elif not auto_password and user_created:
            result['message'] = _(u'User created')
        elif auto_password and not user_created:
            result['message'] = _(u'User updated with password: %s' % password)
        else:
            result['message'] = _(u'User updated')
            
        return result
    
    def update_user_profile(self, user, row):
        up, created = UserProfile.objects.get_or_create(user=user)
        for col_name in row:
            setattr(up, col_name, row[col_name])
        up.save()
        
    def update_custom_fields(self, user, row):
        custom_fields = CustomField.objects.all()
        for cf in custom_fields:
            if cf.id in row:
                upcf, created = UserProfileCustomField.objects.get_or_create(user=user, key_name=cf)
                if cf.type == 'bool':
                    upcf.value_bool = row[cf.id]
                elif cf.type == 'int':
                    upcf.value_int = row[cf.id]
                else:
                    upcf.value_str = row[cf.id]
                upcf.save()
