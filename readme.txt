
OBJECTIVE 🎯
-----------
After creating a fresh new VM/VPS/server (and adding a SSH key while doing so)
I should just be able to run one command on my PC, to have the new remote system
perfectly setup just how I like it.

Thanks to Ansible, everything is nice 'n easy, automated, repeatable and safe 😊
So all my fresh machines can be correctly configured, secured, backed up, and
actually usable and ready to go!

I've documented the playbooks, usage guide and some info about Ansible below...

================================================================================

JOBS 👔
-------
➡️ RECOMMENDED TASKS:
 ⚒️ Essentials:
  ├── ✅ Apt - Configures repositories and updates packages
  ├── ✅ Packages - Installs essential packages
  ├── ✅ User accounts - Creates user(s) and sets permissions
  ├── ✅ SSH - Configures and hardens SSH access
  ├── ✅ Timezone - Sets timezone and NTP server
  ├── ✅ Hostname - Sets hostname and configures hosts
  ├── ✅ Firewall - Sets UFW rules
  ├── ✅ Mail - Sets up Postfix (for notification sending)
  └── ✅ Updates - Enables unattended upgrades

➡️ OPTIONAL TASKS:
 ⚙️ Configs:
  ├── ☑️ Packages - Installs extra packages, for easier management
  └── ☑️ Dotfiles - Configures settings for CLI utils and apps

 💾 Backups
  └── ☑️ Backups - Sets up automated, encrypted, incremental Borg backups

 🔑 Access:
  ├── ☑️ VPN - Sets up and secures Wireguard VPN
  └── ☑️ Cockpit - Sets up Cockpit for easy management via UI

 🖥️ Apps and Services
  ├── ☑️ Docker - Installs and configures Docker (if needed)
  └── ☑️ Proxy - Sets up Caddy (only if not using Docker)

 🔒 Security:
  ├── ☑️ System hardening - Implements some DevSec security baselines
  ├── ☑️ AppArmor - Sets up profiles for process confinement
  ├── ☑️ Intrusion detection - Configures Fail2ban to block brute-force
  ├── ☑️ Integrity monitoring - Sets up and automates OSSEC
  ├── ☑️ Malware scanning - Sets up daily Maldet scans and reporting
  └── ☑️ Security audits - Enables daily Lynis audits and reporting

 📊 Monitoring:
  ├── ☑️ Log storage – Loki for ingesting and aggregating all logs
  ├── ☑️ Log shipping – Grafana Agent, pushes logs and metrics to Loki
  ├── ☑️ Metrics collection – Grafana Agent, pushing metrics into Prometheus
  ├── ☑️ Metrics storage – Prometheus for storing and querying metrics
  ├── ☑️ Visualization – Grafana for dashboards from Loki and Prometheus
  ├── ☑️ Alerting – Alertmanager for triggering critical notifications
  ├── ☑️ Log rotation - Sets up logrotate for all logs, so they don't get big
  └── ☑️ Monit - Monitors services and restarts them if they fail

Note about Docker:
On servers where Docker is used for deploying services, some of the apps above
can/will be skipped. Such as Caddy, Grafana and Alertmanager
Because it's better to run them in containers instead of directly on the host.
For the Docker stacks, see my compose in: https://github.com/Lissy93/dockyard

================================================================================

USAGE 🛠️
--------
STEP 0: PREREQUISITES
- Ensure Python (3.8+) and Ansible are installed (2.18+) on your local system
- Fetch external roles: `ansible-galaxy install -r requirements.yml`
- Create a new remote server (if u like). And ensure you have SSH access to it

STEP 1: SERVERS
- Add servers. Create `inventories/remote.yml`

STEP 2: CONFIGURATION
- Add variables to `inventories/group_vars/remote.yml` or `all.yml` (shared)
- Best to put secrete variables in an Ansible vault (see instructions below)

STEP 4: RUNNING
- Use the commands in the Makefile to execute the playbooks.
  - First run: `make first-run`
  - Subsequent runs: `make run`

================================================================================

COMMANDS 💲
-----------
Basics:
- `make` - View all available commands and our man page
- `make run` - Run all playbooks (as normal user with new SSH settings)
- `make <role>` - Run a specific role (e.g. `make ssh`)
- `make <playbook>` - Run a specific playbook (e.g. `make security`)

Setup:
- `make install-ansible` - Install Ansible (on host)
- `make requirements` - Downloads external roles from Ansible Galaxy
- `make scaffold-hosts` - Creates inventory template (for you to fill in)
- `make first-run` - First run on a fresh server (as root)

Other:
- `make lint` - Run Ansible-lint on all playbooks and roles
- `make docs` - Generates documentation for roles and playbooks
- `make test` - Runs all tests on playbooks and hosts

Native Ansible Commands:
- Run a playbook on specific servers:
  > ansible-playbook -i inventories/<hosts>.yml playbooks/<playbook>.yml
- Run only roles with a specific tag:
  > ansible-playbook -i inventories/<hosts>.yml playbooks/<play>.yml --tags <tag>
- Run a playbook on a specific server:
  > ansible-playbook -i inventories/<hosts>.yml playbooks/<play>.yml -l <servers>
- Do a dry-run, and preview what changes will be made before applying:
  > ansible-playbook -i inventories/<hosts>.yml playbooks/<play>.yml --check --diff
- Run an ad-hoc command on servers in an inventory:
  > ansible db -i inventories/<hosts>.yml -m shell -a "<shell command>"

================================================================================

ADDING SERVERS 🖥️
-----------------
Define your list of hosts (servers to manage) in the inventory file(s).
The path which ansible looks for hosts in, is specified in ./ansible.cfg
If it's your first time, you can run `make scaffold-hosts` to create a template
Then complete the values in .inventories/production/hosts.yml, like this:

all:
  hosts:
    my-server:
      ansible_host: 111.111.111.111
      ansible_user: bob
      ansible_python_interpreter: /usr/bin/python3
    my-other-server:
      ansible_host: 000.000.000.000
      ansible_user: alice
      ansible_port: 22
      ansible_python_interpreter: /usr/bin/python3

================================================================================

ADDING VARIABLES 🗂️
--------------------
- Defaults are defined per-role in: ./roles/<role_name>/defaults/main.yml
- But you can (and should) override in:  ./inventories/group_vars/all.yml
- Or, set host-specific vars, in:  ./inventories/host_vars/<hostname>.yml
- Secrets should be stored in a vault: ./inventories/group_vars/vault.yml
  1. Create a vault: `ansible-vault create ./inventories/group_vars/vault.yml`
  2. Edit the vault: `ansible-vault edit ./inventories/group_vars/vault.yml`
  3. Use the vault by adding the `--ask-vault-pass` flag when running a playbook

================================================================================

WHAT'S ANSIBLE, AND WHY USE IT? ❓
----------------------------------
Ansible is a simple, open source, agentless tool for automating anything.
Just describe how you want your system to look, and Ansible will ensure
the state is met.

10 Reasons why I love Ansible
Unlike Bash scripts or other alternatives...
1. Ansible is idempotent, so you can run it as many times as you like,
   and it will only make changes if the system is not in the desired state.
2. Ansible is agentless, there's nothing to install on any of your systems.
3. Ansible is declarative, you don't have to worry about the order of operations.
4. Ansible is reusable and x-platform. Write playbooks once, run them anywhere.
5. Ansible is scalable. Run it on a single host or thousands of servers at once.
6. Ansible is extensible. There's thousands of playbooks on Galaxy,
   or you can write your own modules in any language you want.
7. Ansible is simple. No finicky scripts, just self-documenting YAML declarations.
8. Ansible is powerful. Doing anything from simple tasks to complex orchestration.
9. Ansible is safe. Preview changes to be made (--diff), or do a dry-run (--check)
10. Ansible is configurable. Use built-in or custom 'facts' to customize playbooks.

Read the Ansible docs at:
https://docs.ansible.com/ansible/latest/getting_started/introduction.html

================================================================================

ANSIBLE BASICS 📚
-----------------
Terminology:
- Inventories = Who to configure (a list of hosts/servers)
- Playbooks = What to do (at a high level, collection of roles)
- Roles = Reusable collections of logic, made up of tasks
- Tasks = The actual code that Ansible runs (usually YAML)
- Plugins = Reusable code snippets (usually Python) that extend Ansible
- Vars = Variables used to specify values for each playbook/role/task
- ansible.cfg = The config file that tells Ansible where to find things

Structure:
Ansible projects follow a specific directory structure, as illustrated below:
The top-level directories are:
- inventories/ - Where you list the hosts/servers that changes will be applied to
- playbooks/ - The playbooks that run the roles, and define the order of execution
- roles/ - The individual roles, made up of tasks, handlers, and other files

This is the structure of my project:

.
├── ansible.cfg           # Config: inventory paths, plugin dirs, etc
├── callback_plugins/     # Custom Ansible callback plugins
│   └── pretty.py         # Emoji & color stdout formatting
├── inventories/          # Host/group definitions and vars
│   └── production/       # Remote production inventory
│       ├── hosts.yml     # Inventory host list
│       ├── group_vars/   # Variables applied by group
│       │   └── all.yml   # Variables to be shared by all servers in this group
│       └── host_vars/    # Per-host variables
│           └── serv1.yml # Example: Add a file for each of your servers
├── Makefile              # Shortcut targets for playbook runs
├── playbooks/            # Playbooks invoking roles by concern
│   ├── all.yml           # Main "run everything" playbook
│   ├── access.yml        # VPN & Cockpit setup
│   ├── backups.yml       # Borg backup tasks
│   ├── configs.yml       # General configuration tasks
│   ├── essentials.yml    # Core hardening, compliance, audits
│   ├── monitoring.yml    # Loki, Prometheus & Grafana setup
│   ├── security.yml      # Fail2ban, OSSEC, Maldet, Lynis, AppArmor
│   └── services.yml      # Docker, Caddy proxy, and other services
├── readme.txt            # Project overview & usage instructions
├── requirements.yml      # Galaxy roles/collections to install
└── roles/                # Reusable Ansible roles (one dir per role)
    ├── apparmor          # AppArmor profile deployment
    ├── blackbox_exporter # Prometheus Blackbox Exporter
    ├── borg              # Automated Borg backups
    ├── cockpit           # Cockpit management UI
    ├── directories       # Directory structure setup
    ├── docker            # Docker engine install & config
    ├── dotfiles          # User dotfiles deployment
    ├── fail2ban          # Intrusion-detection rules
    ├── firewall          # UFW firewall configuration
    ├── geerlingguy.docker# Docker setup, from geerlingguy
    ├── geerlingguy.pip   # Pip/Python setup, from geerlingguy
    ├── grafana           # Grafana install, config & provisioning
    ├── grafana-agent     # Grafana Agent setup & metrics checks
    ├── hostname          # Hostname & /etc/hosts management
    ├── installs          # Miscellaneous package installs
    ├── logrotate         # Logrotate config and templates
    ├── loki              # Loki log-aggregation setup
    ├── lynis             # Automated Lynis security audits
    ├── maldet            # Linux Malware Detect integration
    ├── monit             # Service monitoring with Monit
    ├── node_exporter     # Prometheus Node Exporter
    ├── prometheus        # Prometheus server setup & config
    ├── ssh               # SSH hardening & key management
    ├── tailscale         # Tailscale VPN installation
    ├── timezone          # Timezone & NTP configuration
    └── users             # User account & permission management

================================================================================

TROUBLESHOOTING 🫨
------------------
1. Ansible requires the locale encoding to be UTF-8; Detected None.
    - Fix: set `export LC_ALL=`
    - Or run `locale -a` to see your locales and set with `LC_ALL='en_US.UTF-8'`

2. Failed to connect to the host via ssh
    - Ensure you have run `make initial-apply` before running `make apply`
    - Check the ansible_user and ansible_host variables in your inventory file
    - Check SSH access to the server. Ensure you can SSH in manually.

3. The task includes an option with an undefined variable.. '___' is undefined
    - Define that variable in `./inventories/group_vars/all.yml` or elsewhere

4. Unable to encrypt nor hash, passlib must be installed
    - Install passlin, with: `pip install passlib`

5. YAML syntax or Jinja2 template errors
    - Check your YAML syntax with: `yamllint <file>.yml`
    - Check your Jinja2 with: `ansible-playbook --syntax-check <playbook>.yml`

6. The role 'foo' was not found
    - Install external roles with: `ansible-galaxy install -r requirements.yml`
    - And double check the `roles_path` and `collections_paths` in ansible.cfg

7. Help, my terminal is full of talking cows!
    - This happens because you have `cowsay` installed 🐮😉
    - Just set: `nocows=1` in your ansible.cfg file

================================================================================

WARNING ⚠️
----------
Should you use this? ...Probably not.
Because it's really easy to create your own Ansible playbooks,
and they will be better tailored to your specific needs.
(Also I don't much want to be responsible if something goes wrong! 🫣)

But feel free to use or copy-paste which ever parts you like into your setup 🫶

IMPORTANT: Read through the playbooks and roles before running them.
And make sure you understand what they do, to avoid any surprises!

================================================================================

LICENSE 📃
----------
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE  [Version 2, December 2004]
Copyright (C) 2025 Alicia Sykes <aliciasykes.com>

Everyone is permitted to copy and distribute verbatim or modified 
copies of this license document, and changing it is allowed as long 
as the name is changed. 

TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
0. You just do whatever the fuck you want to
