# PySplash changelog

## 0.3.1, 0.3.2, 0.3.3, 0.3.4, 0.3.5

2017-12-24
- temporarily replace javascript literal for backwards compatibility
- replace lua literals with single quote strings
- remove user_agent
- update static.py
- Update README.md, add new example
- Bug fix: xpath condition can now be in single quote string
- When custom javascript is in condition anonymous self calling function is called
- Hotfix: use lua literals instead double quote strings

# 0.3

2017-11-08

### Add support for adding proxy

- Add new param backup_wait
- Minor fixes

## 0.2.1, 0.2.2

2017-11-03

- Update README.md and splash_url fix
- Bug fix: escape char for lua literal in POST body

# 0.2

2017-10-29

### Add missing functionality

- Add static parts of lua script
- Add support for POST requests
- Add support for setting up cookies and headers
- Add option to set user-agent
- Prepare repo for PYPI

# 0.1

2017-10-21

### Initial commit

Just basic support for GET requests.