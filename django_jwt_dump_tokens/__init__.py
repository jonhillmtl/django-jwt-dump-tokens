from django.conf import settings
from itertools import chain
from jwcrypto import jwk
from optparse import OptionParser
from termcolor import colored
import django
import operator
import json
import os
import sys


parser = OptionParser()

parser.add_option(
    "--user_ids", 
    type=str, 
    dest="user_ids", 
    help="specify user ids, comma separated", 
    default=None)

parser.add_option(
    "--user_emails", 
    type=str, 
    dest="user_emails", 
    help="specify user emails, comma separated", 
    default=None)

parser.add_option(
    "--order_by", 
    type=str, 
    dest="order_by", 
    help="specify sort order [id, email, username]", 
    default='id')
    
parser.add_option(
    "--sort_direction", 
    type=str, 
    dest="sort_direction", 
    help="specify sort direction [asc, desc]",
    default='asc')
    
parser.add_option(
    "--as_json", 
    action="store_true",
    dest="as_json", 
    help="output as json"
)
    
(options, args) = parser.parse_args()

def get_settings_module():
    for root, dir, files in os.walk(os.getcwd()):
        if "settings.py" in files:
            return "{}.settings".format(root.rsplit("/")[-1])
    return None
    
def main():
    try:
        sys.path.append(os.getcwd())
        settings_module = get_settings_module()
        if settings_module is None:
            print(colored("settings.py file not found", "red"))
            quit()
            
        print(colored("Discovered settings module, setting DJANGO_SETTINGS_MODULE {}\n".format(settings_module), "green"))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
        try:
            django.setup()
        except NameError as e:
            print(colored("Your settings file has an error: {}".format(e), "red"))
            quit()
        
        try:
            settings.JWT_KEY
        except AttributeError as e:
            print(colored("Your settings file has an error: {}".format(e), "red"))
            quit()
            
        from django_jwt_utils import user_to_dictionary, user_dictionary_to_jwt
        from django.contrib.auth.models import User

        if options.user_ids is None and options.user_emails is None:
            users = User.objects.all()
        else:
            users_by_id = []
            if options.user_ids is not None:
                try:
                    users_by_id = [User.objects.get(pk=id) for id in options.user_ids.split(",")]
                except User.DoesNotExist as e:
                    message = "{}: user_id {}".format(str(e)[:-1], id)
                    print(colored(message, "red"))
                    quit()
            print(users_by_id)
            users_by_email = []
            if options.user_emails is not None:
                try:
                    users_by_email = [User.objects.get(email=email.lower()) for email in options.user_emails.split(",")]
                except User.DoesNotExist as e:
                    message = "{}: user_email {}".format(str(e)[:-1], email)
                    print(colored(message, "red"))
                    quit()

            users = list(chain(users_by_id, users_by_email))

        if options.order_by in ['id', 'username', 'email']:
            users = sorted(users, key=operator.attrgetter(options.order_by))
        else:
            print(colored("Using default sort order, order_by specified improperly: \"{}\"\n"
                          .format(options.order_by), "yellow"))
        
        if options.sort_direction.lower() in ['asc', 'desc']:
            if options.sort_direction.lower() == 'desc':
                users.reverse()
        else:
            print(colored("Using default sort direction, sort_direction specified improperly: \"{}\"\n"
                          .format(options.sort_direction), "yellow"))
            
        if options.as_json:
            json_data = []
            
        for user in users:
            ud = user_to_dictionary(user)
            jwt = user_dictionary_to_jwt(ud, settings.JWT_KEY)
            if options.as_json:
                json_data.append(dict(user=ud, jwtoken=jwt))
            else:
                print("user id: {}\nuser email: {}".format(user.id, user.email))
                print(colored(jwt, "cyan"))
                print("\n")
        
        if options.as_json:
            print(json.dumps(json_data))
            
    except django.core.exceptions.ImproperlyConfigured as e:
        print(colored(e, "red"))
