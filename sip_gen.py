#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import ldap
from settings import BaseConfig
import logging
import shutil
from datetime import datetime
import os

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -10s %(funcName) '
                '-10s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

cfg = BaseConfig()


def ldap_to_list(attrs_dic, ATTR_SIPCONF):

    sip_list = []

    if not attrs_dic.get('telephoneNumber', ''):
        attrs_dic['telephoneNumber'] = attrs_dic['AstExtension']
    for ldap_attr,sip_var in ATTR_SIPCONF:
        if attrs_dic.get(ldap_attr, ''):
            sip_list.append((sip_var, attrs_dic.get(ldap_attr)))
                
    return sip_list


def acc_to_sipconf(list_accounts):

    print(list_accounts)

    sip_conf = ''

    for acc in list_accounts:
        templ = ''
        for var, value in acc:
            if var == 'templates':
                templ = '(' + ','.join(value) + ')'
            elif var == 'telephonenumber':
                sip_conf += '\r\n[%s]%s\r\n' % (','.join(value), templ)
            elif var == 'allow':
                for v in value:
                    sip_conf += 'allow=%s\r\n' % v
            elif var == 'vars':
                sip_conf += '%s\r\n' % '\r\n'.join(value)
            else:
                sip_conf += '%s=%s\r\n' % (var, ','.join(value))
            
    return sip_conf
    

def free_number(use_numbers_list, file_name):
    sip_list = []
    f = open(file_name, 'r')
    number_list = json.load(f)
    f.close()
    for number in number_list:
        if not number[0] in use_numbers_list:
            sip_list.append(number[1])
    return sip_list


def save_file(data, filename):
    date = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    shutil.copyfile(os.path.join(cfg.ASTER_SIP_CONF_DIR, filename),
                    os.path.join(cfg.BASE_PATH,cfg.OLD_CONF_DIR, '_'.join((filename,date))))
    f = open(os.path.join(cfg.ASTER_SIP_CONF_DIR,filename), 'w')
    f.write(u';== файл сгенерирован автоматически ==\r\n'.encode('utf-8'))
    f.write(data.encode('utf-8'))
    f.close()


def main():

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    accounts_list = []
    templates_list = []
    nmb_list = []
    nmb_lists = []

    l = ldap.initialize(cfg.LDAP_SERVER)
    l.simple_bind_s(cfg.LDAP_USER, cfg.LDAP_PASS)
    results = l.search_s(cfg.LDAP_BASEDN,
                         cfg.SCOPE,
                         cfg.ACCOUNT_FILTER,
                         cfg.ACCOUNT_ATTR)
    memeberuid_list = l.search_s(cfg.LDAP_BASEDN,
                                 cfg.SCOPE,
                                 cfg.ACCOUNT_GROUP,
                                 cfg.GROUP_ATTR)
    template_group_list = l.search_s(cfg.LDAP_BASEDN,
                                     cfg.SCOPE,
                                     cfg.TEMPLATE_GROUP,
                                     cfg.GROUP_ATTR)
    
    for account in results:
        if account[1]['uid'][0] in memeberuid_list[0][1]['memberUid']:
            try:
                nmb_list.append(account[1]['telephoneNumber'][0])
            except:
                pass
            accounts_list.append(ldap_to_list(account[1], cfg.LIST_ATTR_SIPCONF))
        if account[1]['uid'][0] in template_group_list[0][1]['memberUid']:
            templates_list.append(ldap_to_list(account[1], cfg.LIST_ATTR_SIPCONF))

    for value in free_number(nmb_list, cfg.BASE_ALL_NUMBER):
        nmb_lists.append(ldap_to_list(value, cfg.LIST_ATTR_SIPCONF))

    sip_cfg = acc_to_sipconf(accounts_list)
    sip_empty_cfg = acc_to_sipconf(nmb_lists)
    sip_template_cfg = acc_to_sipconf(templates_list)
    
    LOGGER.info('Количество обработанных номеров:  %s' % len(accounts_list))
    LOGGER.info('Количество номеров в группе:      %s' % len(memeberuid_list[0][1]['memberUid']))
    LOGGER.info('Количество обработанных шаблонов: %s' % len(templates_list))
    LOGGER.info('Количество шаблонов в группе:     %s' % len(template_group_list[0][1]['memberUid']))
    LOGGER.info('Количество шаблонов в группе:     %s' % len(nmb_list))
   
    save_file(sip_cfg, cfg.USER_FILENAME) 
    save_file(sip_empty_cfg, cfg.EMPTY_NUMBER_FILENAME)
    save_file(sip_template_cfg, cfg.TEMPLATE_FILENAME)


if __name__ == '__main__':
    main()
