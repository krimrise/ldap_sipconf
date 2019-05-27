# -*- coding: utf-8 -*-

import os
import ldap


class BaseConfig(object):
    """Base configuration."""
    
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    OLD_CONF_DIR = 'old_sip_conf'
    ASTER_SIP_CONF_DIR = BASE_PATH
    USER_FILENAME = 'sip_ldap.conf'
    TEMPLATE_FILENAME = 'sip_template.conf'
    EMPTY_NUMBER_FILENAME = 'sip_empty_number.conf'
    
    SIP_USER_FILENAME = os.path.join(ASTER_SIP_CONF_DIR, USER_FILENAME)
    SIP_TEMPLATE_FILENAME = os.path.join(ASTER_SIP_CONF_DIR, TEMPLATE_FILENAME)
    SIP_EMPTY_NUMBER_FILENAME = os.path.join(ASTER_SIP_CONF_DIR, EMPTY_NUMBER_FILENAME)
    
    BASE_ALL_NUMBER = 'base_number.json'
    LDAP_SERVER = 'ldaps://example.com'
    LDAP_BASEDN = 'dc=example,dc=com'
    LDAP_USER = 'cn=admin,dc=example,dc=com'
    LDAP_PASS = 'pass'
    SCOPE = ldap.SCOPE_SUBTREE
    ACCOUNT_FILTER = 'objectClass=AsteriskSIPUser'
    ACCOUNT_ATTR = ('telephoneNumber',
                    'AstAccountRegistrationContext',
                    'AstAccountName',
                    'AstAccountMailbox',
                    'AstAccountFullContact',
                    'AstAccountSecret',
                    'uid',
                    'astextension',
                    'astaccounttype',
                    'astaccountfromuser',
                    'astaccountdefaultuser',
                    'astaccounthost',
                    'astaccountdisallowedcodec',
                    'astaccountallowedcodec',
                    'astaccountcallgroup',
                    'astaccountpickupgroup',
                    'astaccountnat',
                    'astaccountdtmfmode',
                    'astaccountcallerid',
                    'astaccountcanreinvite',
                    'astaccountipaddress',
                    'astaccountcontext',
                    'astaccountinsecure',
                    'astaccountqualify',
                    'astaccountpermit',
                    "astaccountsetvar"
                   )
    ACCOUNT_GROUP = 'cn=sip_accounts'
    TEMPLATE_GROUP = 'cn=sip_templates'
    GROUP_ATTR = ('memberUid',)
    LIST_ATTR_SIPCONF =  (
        ('AstAccountRegistrationContext', 'templates'),
        ('telephoneNumber', 'telephonenumber'),
        ('AstExtension', 'extension'),
        ('AstAccountType', 'type'),
        ('AstAccountFullContact', 'fullname'),
        ('AstAccountName', 'username'),
        ('AstAccountFromUser', 'fromuser'),
        ('AstAccountDefaultUser', 'defaultuser'),
        ('AstAccountSecret', 'secret'),    
        ('AstAccountHost', 'host'),
        ('AstAccountMailbox', 'mailbox'),
        ('AstAccountDisallowedCodec', 'disallow'),
        ('AstAccountAllowedCodec', 'allow'),
        ('AstAccountCallGroup', 'callgroup'),
        ('AstAccountPickupGroup', 'pickupgroup'),
        ('AstAccountNAT', 'nat'),
        ('AstAccountDTMFMode', 'dtmfmode'),
        ('AstAccountCallerID', 'callerid'),
        ('AstAccountCanReinvite', 'canreinvite'),
        ('AstAccountIPAddress', 'externaddr'),
        ('AstAccountContext', 'context'),
        ('AstAccountRegistrationExten', 'regext'),
        ('AstAccountInsecure', 'insecure'),
        ('AstAccountQualify', 'qualify'),
        ('AstAccountPermit', 'permit'),
        ('AstAccountSetVar', 'vars'),
    )
