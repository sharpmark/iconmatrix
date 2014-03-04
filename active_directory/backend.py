import ldap
import os
import re
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.backends import ModelBackend #Need to include this as it has been disabled

#Need to have this class inherit from ModelBackend to have permissions inherit to groups.
class ActiveDirectoryAuthenticationBackend(ModelBackend):

    """
    This authentication backend authenticates against Active directory.
    It updates the user objects according to the settings in the AD and is
    able to map specific groups to give users admin rights.
    """

    def __init__(self):
        """ initialise a debuging if enabled """
        self.debug = settings.AD_DEBUG
        if len(settings.AD_DEBUG_FILE) > 0 and self.debug:
            self.debugFile = settings.AD_DEBUG_FILE
            # is the debug file accessible?
            if not os.path.exists(self.debugFile):
                open(self.debugFile,'w').close()
            elif not os.access(self.debugFile, os.W_OK):
                raise IOError("Debug File is not writable")
        else:
            self.debugFile = None

    def authenticate(self,username=None,password=None):
        try:
            if len(password) == 0:
                return None            
            l = ldap.initialize(settings.AD_LDAP_URL)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            binddn = "%s@%s" % (username,settings.AD_NT4_DOMAIN)
            l.simple_bind_s(binddn,password)
            l.unbind_s()
            return self.get_or_create_user(username,password)

        except ImportError:
            self.debug_write('import error in authenticate')
        except ldap.INVALID_CREDENTIALS:
            self.debug_write('%s: Invalid Credentials' % username)

    def get_or_create_user(self, username, password):
        """ create or update the User object """
        # get user info from AD
        userInfo = self.get_user_info(username, password)

        # is there already a user?
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if userInfo is not None:
                user = User(username=username, password=password)
                self.debug_write('create new user %s' % username)
                user.save() #Creates initial user so groups can be manipulated
            else:
                return None

        ## update the user objects
        # group mapping for the access rights
        user.groups.clear() #Clears user groups in case of changes
        for group in userInfo['idGroup']:  #Adds all groups user is member of
            try:
                g=Group.objects.get(name=group)
                user.groups.add(g)
            except:
                pass
        if userInfo['isAdmin']:
            user.is_staff = True
            user.is_superuser = True
        elif userInfo:
            user.is_staff = False
            user.is_superuser = False
        else:
            user.is_active = False

        # personal data
        user.first_name = userInfo['first_name']
        user.last_name = userInfo['last_name']
        user.email = userInfo['mail']

        # cache the AD password
        user.set_password('ldap authenticated') #puts in a dummy PW doesn't matter but use this to put a hash in

        user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def debug_write(self,message):
        """ handle debug messages """
        if self.debugFile is not None:
            fObj = open(self.debugFile, 'a')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            fObj.write("%s\t%s\n" % (now,message))
            fObj.close()

    def check_group(self,membership):
        """ evaluate ADS group memberships """
        self.debug_write("Evaluating group membership")
        isValid = False
        isAdmin = False
        idGroup = []
        pattern = re.compile(r'^CN=(?P<groupName>[\w|\d|\s]+),')  #Our AD groups were mirrored with the Django groups but prefaced with "ID " (notice the space)
        for group in membership:
            groupMatch = pattern.match(group)
            print groupMatch
            if groupMatch:
                thisGroup = groupMatch.group('groupName')
                idGroup.append(thisGroup)
                print thisGroup
                print settings.AD_MEMBERSHIP_REQ
                if thisGroup in settings.AD_MEMBERSHIP_REQ:
                    isValid = True
                if thisGroup in settings.AD_MEMBERSHIP_ADMIN:
                    isAdmin = True

        if isAdmin:
            self.debug_write('is admin user')
        elif isValid:
            self.debug_write('is normal user')
        else:
            self.debug_write('does not have the AD group membership needed')

        return isAdmin, isValid, idGroup

    def get_user_info(self, username, password):
        """ get user info from ADS to a dictionary """
        try:
            userInfo = {
                'username' : username,
                'password' : password,
            }
            # prepare LDAP connection
            # ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,settings.AD_CERT_FILE)
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,ldap.OPT_X_TLS_NEVER) #This required to avoid CN mismatches
            ldap.set_option(ldap.OPT_REFERRALS,0) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!

            # initialize
            self.debug_write('ldap.initialize...')
            l = ldap.initialize(settings.AD_LDAP_URL)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)

            # bind
            binddn = "%s@%s" % (username,settings.AD_NT4_DOMAIN)
            self.debug_write('ldap.bind %s' % binddn)
            l.bind_s(binddn,password)

            # search
            self.debug_write('search...')
            result = l.search_ext_s(settings.AD_SEARCH_DN,ldap.SCOPE_SUBTREE,"sAMAccountName=%s" % username,settings.AD_SEARCH_FIELDS)[0][1]
            self.debug_write("results in %s" % result)

            # Validate that they are a member of review board group
            if result.has_key('memberOf'):
                membership = result['memberOf']
            else:
                self.debug_write('AD user has no group memberships')
                return None

            # user ADS Groups
            isAdmin, isValid, idGroup = self.check_group(membership)

            if not isValid:
                return None

            userInfo['isAdmin'] = isAdmin
            userInfo['idGroup'] = idGroup
            self.debug_write(idGroup)

            # get user info from ADS
            # get email
            if result.has_key('mail'):
                mail = result['mail'][0]
            else:
                mail = ""

            userInfo['mail'] = mail
            self.debug_write("mail=%s" % mail)

            # get surname
            if result.has_key('sn'):
                last_name = result['sn'][0]
            else:
                last_name = None

            userInfo['last_name'] = last_name
            self.debug_write("last_name=%s" % last_name)

            # get display name
            if result.has_key('givenName'):
                first_name = result['givenName'][0]
            else:
                first_name = None

            userInfo['first_name'] = first_name
            self.debug_write("first_name=%s" % first_name)

            # LDAP unbind
            l.unbind_s()
            return userInfo

        except Exception, e:
            self.debug_write("exception caught!")
            self.debug_write(e)
            return None