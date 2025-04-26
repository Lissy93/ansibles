
INTRO 👋
--------
This is how I setup and maintain my servers, with Ansible.
Everything is nice and easy, automated, repeatable and safe.

================================================================================

JOBS 👔
-------
The following tasks (roles) are performed on each server,
to take it from zero to full-configured, usable and secure.
Only the basics are required, the rest are optional.

➡️ ESSENTIAL TASKS:
 ⚒️ Basics:
  ├── ☑️ Apt - Configures repositories and updates packages
  ├── ☑️ Packages - Installs essential packages
  ├── ☑️ User accounts - Creates user(s) and sets permissions
  ├── ☑️ SSH - Configures and hardens SSH access
  ├── ☑️ Timezone - Sets timezone and NTP server
  ├── ☑️ Hostname - Sets hostname and configures hosts
  ├── ☑️ Firewall - Sets UFW rules
  ├── ☑️ Mail - Sets up Postfix (for notification sending)
  └── ☑️ Updates - Enables unattended upgrades

➡️ OPTIONAL TASKS:
 ⚙️ Extras:
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
  ├── ☑️ Visualization – Grafana for dashboards from Loki and Prometheus
  ├── ☑️ Alerting – Alertmanager for triggering critical notifications
  └── ☑️ Log rotation - Sets up logrotate for all logs, so they don't get big

Running:
- `make essentials` will only apply the basics (essential for all servers)
- `make apply` will run everything
- `make first-apply` should be used for the first run (logs in as root)
- `make [category]` or `make [role]` will run a specific category or role

Notes:
- Caddy, Grafana and Alertmanager can be skipped servers where Docker is used,
  as they can (and should) run within containers instead.

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
- Add variables to `inventories/group_vars/remote.yml`
- Best to put secrete variables in an Ansible vault
  1. Create a vault: ansible-vault create ./inventories/group_vars/vault.yml
  2. Edit the vault: ansible-vault edit ./inventories/group_vars/vault.yml
  3. Use the vault by adding the --ask-vault-pass flag when running a playbook

STEP 4: RUNNING
- Use the commands in the Makefile to execute the playbooks.
  - First run: `make first-apply`
  - Subsequent runs: `make apply`
  
- Alternatively, you can run ansible commands directly for more control. For example:
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
Specify the path to this file in the ansible config: ./ansible.cfg
By default, we've got ./inventories/remote.yml, which looks like this:

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

================================================================================

WHAT'S ANSIBLE, AND WHY USE IT? ❓
----------------------------------
Ansible is a simple (just YAML), open source (free) and agentless (nothing to install)
tool for automating pretty much anything, anywhere.
Just describe how you want your system to look, and Ansible will ensure the state is met.

10 Reasons why I love Ansible
Unlike Bash scripts or other alternatives...
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
9. Ansible is safe. Use --diff to see what changes will be made, and --check for a dry-run.
10. Ansible is configurable. Use built-in or custom 'facts' to customize playbooks.

Read the Ansible docs at:
https://docs.ansible.com/ansible/latest/getting_started/introduction.html

================================================================================

ANSIBLE BASICS 📚
-----------------
Terminology:
- Inventories = Who to configure (which hosts)
- Playbooks = What to do (at a high level, collection of roles)
- Roles = Reusable collections of logic, made up of tasks

Ansible projects follow a specific directory structure.
Warning: There's a lot of directories and main.yml files!
(This can be customized in ansible.cfg, but best to use standard layout)

ansible/                             # ── Top-level project directory
├── ansible.cfg                      # ── Config: inventory paths, roles path, default vars, plugins, etc.
├── requirements.yml                 # ── List of external Galaxy/Ansible-lint roles to install
├── .vault_pass.txt                  # ── (Optional) file containing your vault password; keep out of Git
├── inventories/                     # ── Define which hosts to manage
│   ├── production.yml               # ── Production inventory (hostnames/IPs, groups)
│   ├── staging.yml                  # ── Staging/testing inventory
│   ├── group_vars/                  # ── Variables applied to whole groups
│   │   ├── all.yml                  #     ── Vars for every host in any inventory
│   │   └── webservers.yml           #     ── Vars for the “webservers” group only
│   └── host_vars/                   # ── Variables applied to individual hosts
│       └── db01.example.com.yml     #     ── Overrides for a single host
├── playbooks/                       # ── Entry-point playbooks invoking roles/tasks
│   ├── site.yml                     # ── “Umbrella” playbook: runs everything in correct order
│   ├── webservers.yml               # ── Web-tier specific playbook
│   └── dbservers.yml                # ── Database playbook
├── roles/                           # ── Reusable components (can be shared via Galaxy)
│   ├── common/                      # ── “Bootstrap” tasks for all hosts
│   │   ├── tasks/                   #     ── Main list of steps to run
│   │   │   └── main.yml             #       ── Entry point for this role’s tasks
│   │   ├── handlers/                #     ── Handlers triggered by tasks (e.g. restart service)
│   │   │   └── main.yml
│   │   ├── defaults/                #     ── Lowest-priority default variables
│   │   │   └── main.yml
│   │   ├── vars/                    #     ── Higher-priority role variables
│   │   │   └── main.yml
│   │   ├── files/                   #     ── Static files to copy (e.g. configs, binaries)
│   │   ├── templates/               #     ── Jinja2 templates (e.g. nginx.conf.j2)
│   │   └── meta/                    #     ── Role metadata and dependencies
│   │       └── main.yml
│   ├── webserver/                   # ── Role to install & configure your web server
│   │   └── (same sub-dirs as above)
│   └── database/                    # ── Role for DB setup (Postgres/MySQL/etc.)
│       └── (…)
├── scripts/                         # ── Helper scripts (e.g. inventory generators)
│   └── dynamic_inventory.py         #     ── Python script for a dynamic inventory source
├── group_vars/                      # ── Legacy/global group-vars (if not under inventories/)
│   └── all.yml
└── host_vars/                       # ── Legacy/global host-vars (if not under inventories/)
    └── example.com.yml

================================================================================

TROUBLESHOOTING 🫨
------------------
1. Ansible requires the locale encoding to be UTF-8; Detected None.
    - Fix: set `export LC_ALL=`
    - Or run `locale -a` to see available locales, and set one, like `LC_ALL='C.utf8`

2. Failed to connect to the host via ssh
    - Ensure you have run `make initial-apply` before running `make apply`
    - Check SSH access to the server. Ensure you can SSH in manually.
    - Check the ansible_user and ansible_host variables in your inventory file

3. The task includes an option with an undefined variable.. '___' is undefined
    - Fix: Define that variable in `./inventories/group_vars/all.yml` or elsewhere

4. Unable to encrypt nor hash, passlib must be installed
    - Install passlin, with: `pip install passlib`

5. YAML syntax or Jinja2 template errors
    - Check your YAML syntax with: `yamllint <file>.yml`
    - Check your Jinja2 templates with: `ansible-playbook --syntax-check <playbook>.yml`

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
