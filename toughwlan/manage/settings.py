#!/usr/bin/env python
#coding=utf-8

import os


param_cache_key = 'toughwlan.cache.param.{0}'.format
nas_cache_ipkey = 'toughwlan.cache.nas.ip.{0}'.format
domain_cache_key = 'toughwlan.cache.domain.{0}.{1}'.format
template_cache_key = 'toughwlan.cache.template.{0}.{1}'.format
chkos_cache_key = 'toughwlan.cache.checkos'


def redis_conf(config):
    eredis_url = os.environ.get("REDIS_URL")
    eredis_port = os.environ.get("REDIS_PORT")
    eredis_pwd = os.environ.get("REDIS_PWD")
    eredis_db = os.environ.get("REDIS_DB")

    is_update = any([eredis_url,eredis_port,eredis_pwd,eredis_db])

    if eredis_url:
        config['redis']['host'] = eredis_url
    if eredis_port:
        config['redis']['port'] = int(eredis_port)
    if eredis_pwd:
        config['redis']['passwd'] = eredis_pwd 
    if eredis_db:
        config['redis']['db'] = int(eredis_db)
    if is_update:
        config.save()

    return config['redis']

