.PHONY: first-apply apply docker users ssh timezone hostname firewall dotfiles monit

ANSIBLE_CMD = ansible-playbook playbooks/bootstrap.yml
BECOME = --ask-become-pass
AS_ROOT = --extra-vars "ansible_user=root ansible_port=22"

# Before server is setup, login as root, create user, setup SSH
first-apply:
	$(ANSIBLE_CMD) $(AS_ROOT) --tags initial

# Then after setup, just make apply
apply:
	$(ANSIBLE_CMD) $(BECOME)

# Or, to run just one specific role
docker:
	$(ANSIBLE_CMD) $(BECOME) --tags docker
users:
	$(ANSIBLE_CMD) $(BECOME) --tags users
ssh:
	$(ANSIBLE_CMD) $(BECOME) --tags ssh
timezone:
	$(ANSIBLE_CMD) $(BECOME) --tags timezone
hostname:
	$(ANSIBLE_CMD) $(BECOME) --tags hostname
firewall:
	$(ANSIBLE_CMD) $(BECOME) --tags firewall
dotfiles:
	$(ANSIBLE_CMD) $(BECOME) --tags dotfiles
monit:
	$(ANSIBLE_CMD) $(BECOME) --tags monit
cockpit:
	$(ANSIBLE_CMD) $(BECOME) --tags cockpit
borg:
	$(ANSIBLE_CMD) $(BECOME) --tags borg

