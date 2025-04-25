INTRO
-----

This is how I setup and maintain my servers, with Ansible.
Everything is nice and easy, automated, repeatable and safe.

Basics:
- ☑️ Apt - Updates packages, configures repositories and upgrades
- ☑️ Packages - Installs common packages
- ☑️ User accounts - Creates user(s) and sets permissions
- ☑️ SSH - Hardens SSH
- ☑️ Timezone - Sets timezone and NTP server
- ☑️ Hostname - Sets hostname and configures hosts
- ☑️ Mail - Sets up Postfix and Dovecot

Maintenance:
- ☑️ Firewall - Sets UFW rules
- ☑️ Backups - Sets up automated Borg backups
- ☑️ Updates - Sets up unattended upgrades
- ☑️ Monitoring - Sets up monitoring and alerting
- ☑️ Logs - Sets up log rotation and monitoring
- ☑️ Fail2ban - Sets up fail2ban
- ☑️ VPN - Sets up Wireguard VPN

Apps:
- ☑️ Docker - Installs and configures Docker
- ☑️ Cockpit - Sets up Cockpit and management UI
- ☑️ Proxy - Sets up Caddy (if not already using in docker) 

USAGE
-----

STEP 0: PREREQUISITES
- Ensure Python (3.8+) and Ansible are installed (2.18+) on your local system
- Fetch external roles: `ansible-galaxy install -r requirements.yml`
- Ensure you have SSH access to the remote servers

STEP 1: SERVERS
- Add servers. Create `inventories/remote.yml`

STEP 2: CONFIGURATION
- Add variables to `inventories/group_vars/remote.yml`
- Best to put secrete variables in an Ansible vault
  1. Create a vault: ansible-vault create ./inventories/group_vars/vault.yml
  2. Edit the vault: ansible-vault edit ./inventories/group_vars/vault.yml
  3. Use the vault by adding the --ask-vault-pass flag when running a playbook

STEP 4: RUNNING
- First run: `make first-apply`
- Subsequent runs: `make apply`


WHAT'S ANSIBLE, AND WHY USE IT?
-------------------------------
Ansible is a simple (just YAML), open source (free) and agentless (nothing to install)
tool for automating pretty much anything, anywhere.
Just describe how you want your system to look, and Ansible will ensure the state is met.

Unlike a bash script, and most other automation tools:
1. Ansible is idempotent, so you can run it as many times as you like,
   and it will only make changes if the system is not in the desired state.
2. Ansible is agentless, meaning there's nothing to install on any of your systems.
3. Ansible is declarative, so you don't have to worry about the order of operations.
4. Ansible is reusable and x-platform. Write your playbooks once, and run them anywhere.
5. Ansible is scalable. You can run it on a single host or thousands of servers at once.
6. Ansible is extensible. There's thousands of playbooks on Galaxy,
   or you can write your own modules in any language you want.
7. Ansible is simple. No finicky scripts, just self-documenting YAML declarations.
8. Ansible is powerful. You can do anything from simple tasks to complex orchestration.


Read the Ansible docs at:
https://docs.ansible.com/ansible/latest/getting_started/introduction.html


Terminology:
- Inventories = Who to configure (which hosts)
- Playbooks = What to do (at a high level, collection of roles)
- Roles = Reusable collections of logic, made up of tasks

Structure:

ansible/
├── ansible.cfg                 # Config file (inventory, roles path, etc)
├── playbooks/
│   ├── bootstrap.yml           # Main setup playbook
│   └── docker.yml              # Optional specific setup
├── inventories/                # Collections of hosts
│   ├── remote.yml              # Remote production servers
│   └── local.yml               # Local testing
├── roles/
│   ├── users/
│   │   ├── tasks/main.yml
│   │   └── defaults/main.yml
│   ├── ssh/
│   │   └── tasks/main.yml
│   └── ...
├── group_vars/
│   └── all.yml
└── secrets/
    └── vault.yml


Role Structure:

(this is th only thing I don't like about Ansible. Too many nested main.yml files.)
🏅 You have earned the "main.yml Master" achievement!

roles/
├── users/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   ├── vars/
│   │   └── main.yml
│   └── defaults/
│       └── main.yml


