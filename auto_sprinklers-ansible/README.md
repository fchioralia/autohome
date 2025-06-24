# auto_sprinklers Ansible Deployment

This project provides an Ansible playbook to deploy the auto_sprinklers application on a remote Raspbian system. The playbook automates the installation of necessary packages, configuration of services and deployment of the application.

## Project Structure

- **playbook.yml**: The main Ansible playbook that orchestrates the deployment.
- **roles**: Contains various roles for common tasks, Nginx setup, Gunicorn setup and application deployment.
  - **common**: Tasks that are common to all deployments.
  - **webserver**: Tasks specific to the installation and configuration of the http service.
  - **oauth2-proxy**: Tasks specific to the installation and configuration of oauth2-proxy.
  - **app**: Tasks specific to deploying the auto_sprinklers application.
- **README.md**: Documentation for the project.
- **group_vars/raspberry.yml**: The file used for keeping variables. To be modified!
- **inventory**: Contains the list of hosts for deployment. To be modified!

## Requirements

- Ansible and git installed on your local machine.
- Access to a remote Raspbian system with SSH enabled with ssh key at ~/.ssh/id_rsa.

## Usage
Deploy 

1. Create `inventory` file in this directory with the details of your remote Raspbian system, like:
```
[remote]
raspberry_pi ansible_host=192.168.1.1 ansible_user=pi ansible_ssh_private_key_file=~/.ssh/id_rsa
```
2. Create `group_var/raspberry.yml` file in this directory with the details of your remote Raspbian system, like:
```
server_hostname: example.com
account_email: youremail@example.com
web_username: pi_username
web_password: pi_passwd
web_auth_file: "/etc/nginx/.htpasswd"
web_root: /var/www/html
app_folder: "{{ web_root }}/auto_sprinklers"
app_environment: "/root/.virtualenvs/django"
app_name: "autohome"
app_repo_destination: "/opt/{{ app_name }}"
app_gunicorn_socket: "{{ web_root }}/auto_sprinklers.sock"


oauth2_enable: false # change to true if you want to use this
oauth2_cpu_version: "armv6"  # for older raspberry pi
oauth2_provider: "google"
oauth2_client_id: "create a client id at google"
oauth2_client_secret:  "set secret for client id"
# Generate a random cookie secret (32 bytes, base64)
# python3 -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'
oauth2_cookie_secret: "RSZWYxzcVl_Kl8eTHwFJUBsONqnz-Fuf3Zp6F5SYJV4"
oauth2_allowed_emails:
  - email1@example.com
  - email2@example.com

```
3. Run the playbook using the following command from this folder:
```
ansible-playbook -i inventory playbook.yml
```
