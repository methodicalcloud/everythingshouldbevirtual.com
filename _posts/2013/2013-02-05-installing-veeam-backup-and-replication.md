---
title: Installing Veeam Backup and Replication
date: 2013-02-05 16:48:11
toc: true
toc_label: "Installation Steps"
---

In this post we will be installing the Backup and Replication server
components. This is a fairly straight forward installation with very
minimal setup steps after installation to get started using it. Of
course there are many advanced setup scenarios that you can build which
would require much more setup time. I will go into those on another post
soon.

First off read the minimum requirements and FAQ
[here](http://www.veeam.com/veeam_backup_6_5_release_notes_rn.pdf).

Or just read below for the hardware requirements which were copied from
the above pdf.

## Hardware Requirements

**Veeam Backup & Replication Server**

- CPU: any x86/x64 processor.
- Memory: 4 GB RAM.
- Hard Disk Space: 2 GB for product installation. 10 GB per 100 VM for
guest file system catalog folder (persistent data). Sufficient free disk
space for Instant VM Recovery cache folder (non-persistent data, at
least 10 GB recommended).
- Network: 1 Gbps LAN for on-site backup and replication, 1 Mbps or faster
WAN for off-site backup and replication. High latency links are
supported, but TCP/IP connection must not drop.

**Backup Proxy Server**

- CPU: modern x86/x64 processor (minimum 2 cores). Using faster multi-core
processors improves data processing performance, and allows for more
concurrent jobs.
- Memory: 2 GB RAM per concurrent job. Using faster memory (DDR3) improves
data processing performance.
- Hard Disk Space: 300 MB.
- Network: 1 Gbps LAN for on-site backup and replication, 1 Mbps or faster
WAN for off-site backup and replication. High latency links are
supported, but TCP/IP connection must not drop.

**Backup Repository Server**

- CPU: any x86/x64 processor.
- Memory: 2 GB RAM per concurrent job.
- Network: 1 Gbps LAN for on-site backup and replication, 1 Mbps or faster
WAN for off-site backup and replication. Unreliable, high latency links
with packet loss are supported, but TCP/IP connection must not drop
completely.

## Installation

In this scenario we will be using a Windows 2008 R2 x64 server to
install on.

Let's get started.

Launch installation program:

![Veeam Installation Step 1](/assets/veeam-2013/veeam-install-01.png)

![Veeam Installation Step 2](/assets/veeam-2013/veeam-install-02.png)

![Veeam Installation Step 3](/assets/veeam-2013/veeam-install-03.png)

![Veeam Installation Step 4](/assets/veeam-2013/veeam-install-04.png)

![Veeam Installation Step 5](/assets/veeam-2013/veeam-install-05.png)

Download and browse to your trial license file.

![Veeam Installation Step 6](/assets/veeam-2013/veeam-install-06.png)

![Veeam Installation Step 7](/assets/veeam-2013/veeam-install-07.png)

![Veeam Installation Step 8](/assets/veeam-2013/veeam-install-08.png)

![Veeam Installation Step 9](/assets/veeam-2013/veeam-install-09.png)

![Veeam Installation Step 10](/assets/veeam-2013/veeam-install-10.png)

![Veeam Installation Step 11](/assets/veeam-2013/veeam-install-11.png)

![Veeam Installation Step 12](/assets/veeam-2013/veeam-install-12.png)

![Veeam Installation Step 13](/assets/veeam-2013/veeam-install-13.png)

![Veeam Installation Step 14](/assets/veeam-2013/veeam-install-14.png)

Now that the installation is complete launch the app.

![Veeam Installation Step 15](/assets/veeam-2013/veeam-install-15.png)

## Configuring Your First Backup Job

Now we will configure our first backup job to run.

![Veeam Installation Step 16](/assets/veeam-2013/veeam-install-16.png)

Click backup job.

![Veeam Installation Step 17](/assets/veeam-2013/veeam-install-17.png)

![Veeam Installation Step 18](/assets/veeam-2013/veeam-install-18.png)

Click on VMware vSphere:

![Veeam Installation Step 19](/assets/veeam-2013/veeam-install-19.png)

Enter IP or DNS name for host or enter your vCenter info.

![Veeam Installation Step 20](/assets/veeam-2013/veeam-install-20.png)

![Veeam Installation Step 21](/assets/veeam-2013/veeam-install-21.png)

![Veeam Installation Step 22](/assets/veeam-2013/veeam-install-22.png)

![Veeam Installation Step 23](/assets/veeam-2013/veeam-install-23.png)

![Veeam Installation Step 24](/assets/veeam-2013/veeam-install-24.png)

Click add to select which virtual machines you would like to backup.

![Veeam Installation Step 25](/assets/veeam-2013/veeam-install-25.png)

When adding objects to backup you can select data center, cluster,
hosts, folders, resource pools, datastores or individual virtual
machines. Make sure that you layout your different objects in vCenter to
whatever makes sense and makes this selection process the easiest and
cleanest as well as something that will capture the virtual machines
even if they move between any of these objects.

![Veeam Installation Step 26](/assets/veeam-2013/veeam-install-26.png)

![Veeam Installation Step 27](/assets/veeam-2013/veeam-install-27.png)

Select your backup repository you want to backup to. For information on
adding a Linux NFS backup repository read
[this](https://everythingshouldbevirtual.com/veeam-backup-and-replication-to-nexenta-nfs) article.

![Veeam Installation Step 28](/assets/veeam-2013/veeam-install-28.png)

Select Enable application-aware image processing for servers such as
Exchange or MS SQL and any other application that uses VSS technology.

![Veeam Installation Step 29](/assets/veeam-2013/veeam-install-29.png)

![Veeam Installation Step 30](/assets/veeam-2013/veeam-install-30.png)

![Veeam Installation Step 31](/assets/veeam-2013/veeam-install-31.png)

That's all there is to it. Now you are ready to start your backups.
More posts will follow going over file level restores, full vm restores
and etc. As well as on replication scenarios.

Feel free to leave comments as I look forward to any and all feedback.
