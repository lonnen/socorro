# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Makes a user into a superuser/staff. This is helpful for local development
environment.
"""

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError


def get_input(text):
    """Get user input, or mock it for tests."""
    return input(text).strip()


class Command(BaseCommand):
    help = "Makes a user a superuser/staff for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            "emailaddress",
            nargs="+",
            type=str,
            help="email address of user account to promote",
        )

    def handle(self, **options):
        emails = options["emailaddress"]
        if not emails:
            emails = [get_input("Email address: ").strip()]
        if not [x for x in emails if x.strip()]:
            raise CommandError("Must supply at least one email address")
        for email in emails:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = User.objects.create(username=email, email=email)
                user.set_unusable_password()

            # Set superuser and staff flags on user
            if user.is_superuser and user.is_staff:
                self.stdout.write("{} was already a superuser/staff".format(user.email))
            else:
                user.is_superuser = True
                user.is_staff = True
                self.stdout.write("{} is now a superuser/staff".format(user.email))
                user.save()

            # Add user to Hackers group
            try:
                hackers_group = Group.objects.get(name="Hackers")
                if user in hackers_group.user_set.all():
                    self.stdout.write(
                        "{} is already in Hackers group.".format(user.email)
                    )
                else:
                    hackers_group.user_set.add(user)
                    self.stdout.write("{} added to Hackers group.".format(user.email))
                    user.save()
            except Group.DoesNotExist:
                self.stdout.write('"Hackers" group does not exist.')
