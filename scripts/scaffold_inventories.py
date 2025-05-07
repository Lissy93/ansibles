
# 1. If inventories/ already exists, and so does ./production, then exit with info
# 2. If it does not exist, create it
# 3. Then create the file structure:
  # inventories
  # └── production
  #    ├── group_vars
  #    │  └── all.yml
  #    ├── host_vars
  #    │  └── my-server.yml
  #    └── hosts.yml

# 4. Write content to group_vars/all.yml
# 5. Write content to host_vars/my-server.yml
# 6. Write content to hosts.yml
# 7. Print a message indicating that the inventory structure has been created
# And tell them what each file is, and what they should edit in it.
# Finally, tell them how they can add new servers to the inventory.
