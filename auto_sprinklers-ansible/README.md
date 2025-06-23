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
2. Run the playbook using the following command:
```
ansible-playbook -i inventory playbook.yml
```
3. Follow any additional instructions provided in the roles for specific configurations.
