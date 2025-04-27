.PHONY: help first-apply apply setup requirements lint install-ansible install-lint check-env $(ROLE_TARGETS) $(ROLE_CATEGORIES)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Variables
PYTHON		  		:= python3
PIP			 				:= pip3
ANSIBLE_PLAYBOOK:= ansible-playbook
ANSIBLE_LINT		:= ansible-lint
GALAXY		  		:= ansible-galaxy
PLAYBOOK				:= playbooks/all.yml
BECOME		  		:= --ask-become-pass
AS_ROOT		 			:= --extra-vars "ansible_user=root ansible_port=22"

# List of all "role" tags
ROLE_TARGETS = docker \
	timezone \
	users \
	ssh \
	hostname \
	firewall \
	fail2ban \
	dotfiles \
	monit \
	cockpit \
	borg \
	maldet \
	lynis

ROLE_CATEGORIES = essentials \
	configs \
	backups \
	access \
	services \
	security \
	monitoring

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
help:
		@echo "Usage:"
		@echo	"  make setup         # install pip deps, galaxy requirements, ansible-lint"
		@echo "  make requirements  # install ansible-galaxy roles from requirements.yml"
		@echo "  make lint          # run ansible-lint on your playbooks"
		@echo "  make first-apply   # Initial bootstrap (root-only, before any users exist)"
		@echo "  make apply         # run all roles"
		@echo "  make <role>        # run one tagged role"
		@echo "  make <category>    # run one tagged category"
		@echo
	@echo "Available categories: $(ROLE_CATEGORIES)"
	@echo "Available roles: $(ROLE_TARGETS)"

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Environment checks
check-env:
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
	  echo >&2 "Error: $(PYTHON) not found. Please install Python 3."; \
	  exit 1; \
	}
	@command -v $(PIP) >/dev/null 2>&1 || { \
	  echo >&2 "Error: $(PIP) not found. Please install pip for Python 3."; \
	  exit 1; \
	}

check-ansible:
	@command -v $(ANSIBLE_LINT) >/dev/null 2>&1 || { \
	  echo >&2 "Error: $(ANSIBLE_LINT) not found. Run `make install-lint`"; \
	  exit 1; \
	}
	@command -v $(ANSIBLE_PLAYBOOK) >/dev/null 2>&1 || { \
	  echo >&2 "Error: $(ANSIBLE_PLAYBOOK) not found. Run `make install-ansible`"; \
	  exit 1; \
	}

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# pip-based installs
install-ansible: check-env
	@echo "Installing Ansible via pip..."
	$(PIP) install --user ansible

install-lint: check-env
	@echo "Installing ansible-lint via pip..."
	$(PIP) install --user ansible-lint

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Galaxy roles
requirements: check-env check-ansible
	@echo "Installing Ansible Galaxy roles from requirements.yml..."
	$(GALAXY) install -r requirements.yml

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Combined setup
setup: check-env install-ansible install-lint requirements
	@echo "✔️  Environment is ready - Ansible, ansible-lint, and Galaxy roles installed."

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Linting
lint: check-ansible
	@echo "Running ansible-lint..."
	$(ANSIBLE_LINT) playbooks/

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Existing targets

first-apply first-run:
	$(ANSIBLE_PLAYBOOK) $(PLAYBOOK) $(AS_ROOT) --tags initial

apply run:
	$(ANSIBLE_PLAYBOOK) $(PLAYBOOK) $(BECOME)

# pattern rule: `make docker` → ansible-playbook ... --tags docker
$(ROLE_TARGETS):
	$(ANSIBLE_PLAYBOOK) $(PLAYBOOK) $(BECOME) --tags $@

$(ROLE_CATEGORIES):
	$(ANSIBLE_PLAYBOOK) $(PLAYBOOK) $(BECOME) --tags $@
