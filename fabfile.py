from datetime import datetime
from fabric.api import task, env, settings, cd, sudo, run, local, put, path, shell_env

stamp = datetime.now().strftime("v%Y%m%d%H%M%S")
stamptar = "r_tt-" + stamp + ".tar"
stampzip = stamptar + ".gz"

env.stamp = stamp
env.stamptar = stamptar
env.stampzip = stampzip

@task
def live():
    env.hosts = [
        "crow.endrun.org"
    ]

@task
def deploy():
    local('make clean')

    local('tar cf %(stamptar)s requirements/' % env)
    local('tar rf %(stamptar)s tagtrain/' % env)
    local('tar rf %(stamptar)s run.py' % env)
    local('tar rf %(stamptar)s run.sh' % env)
    local('gzip %(stamptar)s' % env)

    put(stampzip, '/tmp/%(stampzip)s' % env)

    local('rm %(stampzip)s' % env)

    with settings(sudo_user='reddit_tagtrain'):

        with cd('/home/reddit_tagtrain/run'):
            sudo('mkdir -p %(stamp)s/src' % env)
            sudo('mkdir -p %(stamp)s/venv' % env)

        with cd('/home/reddit_tagtrain/run/%(stamp)s' % env):
            sudo('tar xfz /tmp/%(stampzip)s -C ./src/' % env)

    sudo('rm /tmp/%(stampzip)s' % env)

    with settings(sudo_user='reddit_tagtrain'):

        with cd('/home/reddit_tagtrain/run/%(stamp)s' % env):
            with shell_env(PATH='/opt/pyenv/bin/:$PATH', PYENV_ROOT='/opt/pyenv'):
                sudo('virtualenv venv -p $(pyenv prefix 3.6.1)/bin/python' % env)

            with path('./venv/bin', behavior='prepend'):
                sudo('pip install --quiet --no-cache-dir -r ./src/requirements/prod.txt' % env)

        with cd('/home/reddit_tagtrain'):
            sudo('run/current/src/run.sh stop')

        with cd('/home/reddit_tagtrain/run'):
            sudo('ln -nsf $(basename $(readlink -f current)) previous' % env)
            sudo('ln -nsf %(stamp)s current' % env)

        with cd('/home/reddit_tagtrain'):
            sudo('run/current/src/run.sh start')


@task
def clean():
    with settings(sudo_user='reddit_tagtrain'):
        with cd('/home/reddit_tagtrain/run'):
            sudo('current=$(basename $(readlink -f current)) && previous=$(basename $(readlink -f previous)) && for dir in $(ls -dt */ | egrep -v "current|previous|$current|$previous"); do rm -r $dir; done')
