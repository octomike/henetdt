Tunnelbroker.net (he.net) automated daily test
---

Simple script for the *IPv6 Certification* daily tests:

+ traceroute
+ dig AAAA/PTR
+ ping
+ whois


Requirements
---

Python 3.3+, Linux, Commands listed above.

User/Password in **auth_data**.

Systemd
---
```
sudo install -m0755 henet.py /usr/local/bin/henet.py
sudo cp henet.service henet.timer /etc/systemd/system
sudo systemctl enable henet.timer
sudo systemctl start henet.timer
```

Caution
---

Untested, I just got my tunnel some hours ago ..
