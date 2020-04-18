# auto_sprinklers
Main purpose is to make a website that control sprinklers (solenoid valves) with multiple types of control.
- manual control (on/off or completly disable)
- scheduled control
- motion detection control
## Requirements for raspberry pi 
```
sudo su
apt-get update
apt-get install git screen lsof tcpdump 
apt-get install python3 python3-pip python3-dev virtualenv
####change default python command to python3
python=`which python`;  [[ -L "$python" ]] && [[ `python --version |grep  "Python 3"` ]] ||  ln -sf /usr/bin/python3 $python
pip install --upgrade pip
pip install virtualenv Django Django-scheduled-tasks
```
## Building environment for project 
```
mkdir -p ~/.virtualenvs/
cd ~/.virtualenvs/
virtualenv django
source ~/.virtualenvs/django/bin/activate
###

python manage runserver 0.0.0.0:8000
```
