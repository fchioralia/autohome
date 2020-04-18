# auto_sprinklers
Main purpose is to make a website that control sprinklers (solenoid valves) with multiple types of control.
- manual control (on/off or completly disable)
- scheduled control
- motion detection control
## Requirements for raspberry pi 
```
sudo su
apt-get update
apt-get install git subversion screen lsof tcpdump nginx
apt-get install python3 python3-pip python3-dev virtualenv
####change default python command to python3
python=`which python`;  [[ -L "$python" ]] && [[ `python --version |grep  "Python 3"` ]] ||  ln -sf /usr/bin/python3 $python
pip install --upgrade pip
pip install virtualenv Django Django-scheduled-tasks
```
## Building environment for project 
```
mkdir -p /root/.virtualenvs/
cd /root/.virtualenvs/
virtualenv django
source /root/.virtualenvs/django/bin/activate
###
pip install django gunicorn 
### choose a folder where will you download the project
project_folder=/var/www/html
mkdir -p $project_folder
cd $project_folder
svn export https://github.com/fchioralia/autohome.git/trunk/auto_sprinklers

## configure nginx and gunicorn
cd $project_folder/auto_sprinklers
###optional test `python manage runserver 0.0.0.0:8000`
###optional test `gunicorn --bind 0.0.0.0:8000 home.wsgi`

cd /etc/systemd/system
svn export --force  https://github.com/fchioralia/autohome.git/trunk/config_files/gunicorn.service
systemctl daemon-reload
systemctl enable gunicorn
systemctl restart gunicorn

cd /etc/nginx/sites-available/
svn export --force  https://github.com/fchioralia/autohome.git/trunk/config_files/default
systemctl enable nginx
systemctl restart nginx



```
