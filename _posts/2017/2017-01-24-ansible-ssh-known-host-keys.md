---
  title: Ansible - SSH Known Host Keys
  categories:
    - Automation
  tags:
    - Ansible
  redirect_from:
    - /ansible-ssh-known-host-keys
excerpt: "I wanted to throw this together mainly for my own reference but maybe it will help someone else as well. I had a need to add every host's ssh keys to..."
---

> **Note**: This post was published over 5 years ago and may contain outdated information. Tool versions, syntax, and best practices may have changed. Please verify current documentation before implementing.
{: .notice--warning}


I wanted to throw this together mainly for my own reference but maybe it
will help someone else as well. I had a need to add every host's ssh
keys to every host so that every host knew what every other hosts ssh
keys were. After a bit of attempting many different things below is what
I came up with. And it works.

First create a simple playbook:

{% gist mrlesmithjr/71f0669dfb970b4904a7cbe8b8e46863 %}

Next create this simple template:

{% gist mrlesmithjr/10a0ad5ef831ca83e28f9b100e0f8ac6 %}

Then run

```bash
ansible-playbook -i yourinventoryfile ssh-keys.yml
```

and it will run through each host and capture their respective ssh key
and then create /etc/ssh/ssh_known_hosts on each host including all
other hosts ssh keys as well. Pretty simple after quite a bit of trial
and error but it does work.

Enjoy!

---

### Related Posts

- [2013-07-25-server-2012-ad-upgrade-notes](/server-2012-ad-upgrade-notes/)
- [2014-09-26-iptables-cluster-script](/iptables-cluster-script/)
- [Transforming IT Operations - The Rise of Infrastructure Automation Consulting](/transforming-it-operations-the-rise-of-infrastructure-automation-consulting/)
