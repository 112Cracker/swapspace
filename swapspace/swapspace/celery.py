from __future__ import absolute_import, unicode_literals

import os
from celery import Celery, shared_task
from django.conf import settings
from celery.schedules import crontab

#获取当前文件夹名，即为该Django的项目名
project_name = os.path.split(os.path.abspath('.'))[-1]
project_settings = '%s.settings' % project_name

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

#实例化Celery
app = Celery(project_name)

#使用django的settings文件配置celery
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update-every-30-seconds': {
        'task': 'automatch',
        'schedule': 30.0,
        #'schedule': crontab(minute=1),
    },
    'update-every-5-seconds': {
        'task': 'updatestatus',
        'schedule': 5.0,
        #'schedule': crontab(minute=1),
    },
}