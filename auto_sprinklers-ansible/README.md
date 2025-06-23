# auto_sprinklers Ansible Deployment

This project provides an Ansible playbook to deploy the auto_sprinklers application on a remote Raspbian system. The playbook automates the installation of necessary packages, configuration of services, and deployment of the application.

## Project Structure

- **playbook.yml**: The main Ansible playbook that orchestrates the deployment.
- **inventory**: Contains the list of hosts for deployment.
- **roles**: Contains various roles for common tasks, Nginx setup, Gunicorn setup, and application deployment.
  - **common**: Tasks that are common to all deployments.
  - **nginx**: Tasks specific to the installation and configuration of Nginx.
  - **gunicorn**: Tasks specific to the installation and configuration of Gunicorn.
  - **app**: Tasks specific to deploying the auto_sprinklers application.
- **README.md**: Documentation for the project.

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

```
3. Run the playbook using the following command from this folder:
```
ansible-playbook -i inventory playbook.yml
```
