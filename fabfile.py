#import wingdbstub
import time
import os, sys
from fabric.api import local, cd, run, env, sudo, require
import settings

db = settings.DATABASES['default']
fab = settings.FABRIC['live']


env.hosts = fab['HOSTS']
env.user = fab['ADMIN_USER']
env.admin_user = fab['ADMIN_USER']
env.dbname = db['NAME']
env.dbuser = db['USER']
env.dbpass = db['PASSWORD']

def hello():
    print("Hello world!")
    
def r():
    # symlink convenience
    # ln -s /home/flt/django/projects/flt/ /home/flt/dj
    run('cd C:\Users\Larry\__prjs\flt; ls')


#from fabric.decorators import runs_once 

from fabric.contrib.console import confirm

## try to implement this
#def reload(first=False):
    #""" Reload webserver/webapp """
    #if hasattr(env, 'use_nginx'):
        #if first==True:
            #run("bash /home/%(user)s/%(project_name)s/bin/django_gunicorn start" % env)
        #else:
            #sudo("kill -QUIT `cat %(nginx_pidfile)s`" % env)
            #run("bash /home/%(user)s/%(project_name)s/bin/django_gunicorn restart" % env)
        #sudo("%(nginx_bin)s" % env)
    #else:
        #"Reload Apache to pick up new code changes."
        #sudo("invoke-rc.d apache2 reload")



#@run_once 
def commit(msg): 
    with cd(os.path.abspath(os.path.dirname(__file__))): 
        local('git add .')
        local('git commit -am"%s"' % msg)
        local('git push origin master') # push local to repository 
         
def update_remote():
    env.user = fab['WEB_USER']
    
    with cd(fab['PROJECT_ROOT']): 
        run('git pull origin master') # pull from repository to remote 
        run('python manage.py collectstatic -v0 --noinput')
         
def restart(): 
    sudo('supervisorctl restart flt')
    sudo('/etc/init.d/nginx restart')
         
# def deploy(push_code=False): 
def deploy(msg="No Msg"):
    #if push_code: 
        #commit_code() 
    commit(msg)
    update_remote() 
    #restart()     
   
         
def pushpull():
    local('git push') # runs the command on the local environment
    run('cd /path/to/project/; git pull') # runs the command on the remote environment
   
def backup():
    require('hosts', provided_by=[hg])
    require('dbname')
    require('dbuser')
    require('dbpass')

    date = time.strftime('%Y%m%d%H%M%S')
    fname = '/tmp/%(database)s-backup-%(date)s.xml.gz' % {
        'database': env.dbname,
        'date': date,
    }

    if os.path.exists(fname):
        run('rm "%s"' % fname)

    run('mysqldump -u %(username)s -p%(password)s %(database)s --xml | '
        'gzip > %(fname)s' % {'username': env.dbuser,
                              'password': env.dbpass,
                              'database': env.dbname,
                              'fname': fname})

    get('_bu/' + fname, os.path.basename(fname))
    run('rm "%s"' % fname)
    