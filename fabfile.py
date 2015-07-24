import datetime
import os
import subprocess
import zipfile

from fabric.api import task, run, require, put, local, env, cd, sudo


env.hosts = env.hosts or ['www@lananh.love']
env.use_ssh_config = True


def push():
    """push current git branch to server"""
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    run('mkdir -p /var/www/release/')

    local('git archive --format zip --output ./deploy.zip HEAD')
    zf = zipfile.ZipFile('deploy.zip', mode='a')
    zf.write('.config/env.sh', '.config/env.sh', zipfile.ZIP_DEFLATED)
    zf.close()

    with cd('/var/www/release/'):
        put('./deploy.zip', '%s.zip' % now)
        run('unzip {name}.zip -d {name}'.format(name=now))
        os.unlink('./deploy.zip')
        run('rm {name}.zip'.format(name=now))

        with cd(now):
            sudo("apt-get install -y libjpeg-dev libpng-dev supervisor")
            run('fab deploy')

            print("Copy nginx settings")
            sudo("rm -f /etc/nginx/sites-enabled/www.conf")
            sudo("cp etc/nginx.conf /etc/nginx/sites-enabled/www.conf")
            sudo('service nginx restart')


def deploy():
    """Deploy command run on server"""
    if '/var/www/' not in __file__:
        print("This command run only on remote server")
        return

    if not Run.exec_with_env_wrapper('lsvirtualenv | grep env', output=False):
        print("Create new virtual env")
        Run.exec_with_env_wrapper('mkvirtualenv env -p `which python3.4`')

    print("Init directories")
    Run.execute('mkdir -p /var/www/run/')

    print("Link current deployment to a static path")
    Run.execute("rm ../../on")
    Run.execute("ln -sn `pwd` ../../on")

    print("Install requirement")
    Run.exec_env('pip install -r requirements.txt')

    print("Migrate django")
    Run.exec_env('python manage.py migrate')

    print("Install bower component")
    Run.execute('bower install')

    print("Create static folder if not exists")
    Run.execute('mkdir -p /var/www/static')

    print("Link static folder to current dir")
    Run.execute('ln -sn /var/www/static static')

    print("Collect static")
    Run.exec_env('python manage.py collectstatic --noinput')

    print("Compile django message")
    Run.exec_env('python manage.py compilemessages')

    print("Shutdown web server")
    Run.exec_env('supervisorctl -c/var/www/current/etc/supervisord.conf shutdown')

    print("Like to current")
    Run.execute("rm ../../current")
    Run.execute("ln -sn `pwd` ../../current")

    print("Restart webserver")
    Run.execute("chmod 777 etc/*.sh")
    Run.exec_env('supervisord -c/var/www/current/etc/supervisord.conf')


class Run(object):
    @staticmethod
    def execute(command, output=True):
        print(command)
        result = subprocess.Popen(command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE).communicate()[0]
        if not output:
            return result
        print(result)

    @staticmethod
    def exec_with_env_wrapper(command, output=True):
        Run.execute('source /usr/local/bin/virtualenvwrapper_lazy.sh;%s' % command, output=output)

    @staticmethod
    def exec_env(command, output=True):
        Run.exec_with_env_wrapper('workon env; source .config/env.sh; %s' % command, output=output)
