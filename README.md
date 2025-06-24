# autohome
projects for a smart home using raspberry pi and python

## Running the Ansible Playbook

To deploy the Auto Sprinklers project using Ansible, follow these steps:

1. **Navigate to the Ansible playbook directory:**
   ```sh
   cd auto_sprinklers-ansible
   ```

2. **Run the playbook:**
   ```sh
   ansible-playbook playbook.yml -i inventory
   ```
   - Replace `inventory` with your inventory file if it has a different name or location.

3. **Requirements:**
   - Make sure you have Ansible installed (`pip install ansible`).
   - Ensure your Raspberry Pi is accessible via SSH and listed in your inventory file.

This will configure your Raspberry Pi for the Auto Sprinklers project as described in the playbook.
