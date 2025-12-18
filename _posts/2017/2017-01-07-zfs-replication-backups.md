---
  title: ZFS - Replication Backups
  categories:
    - Storage
  tags:
    - ZFS
  redirect_from:
    - /zfs-replication-backups
excerpt: "I recently rebuilt my lab NAS hosts with Ubuntu 16.04 and used ZFS for the storage pools (once again). In doing it this time around I wanted to get a..."
---

> **Note**: This post was published over 5 years ago and may contain outdated information. Tool versions, syntax, and best practices may have changed. Please verify current documentation before implementing.
{: .notice--warning}


> **Version Notice**: This post references Ubuntu 16.04 which has reached end-of-life. Package names and commands may differ on Ubuntu 22.04/24.04 LTS.
{: .notice--info}

I recently rebuilt my lab NAS hosts with Ubuntu 16.04 and used ZFS for
the storage pools (once again). In doing it this time around I wanted to
get a good method of leveraging ZFS snapshots and replicating them for
my backups. I ended up coming up with the following script that has been
working out quite well so far. As usual, I figured it might be
worthwhile to share this for others to leverage as well.

{% gist mrlesmithjr/ef788f77b457df5ddfb7b223f2d39d6b %}

Enjoy!
