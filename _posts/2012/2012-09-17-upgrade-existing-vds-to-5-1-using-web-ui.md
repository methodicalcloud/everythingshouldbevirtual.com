---
  title: Upgrade existing VDS to 5.1 using web ui
  date: 2012-09-17 22:11:07
excerpt: "Here is a quick walk through on upgrading an existing VDS (Distributed Switch) to version 5.1 from an older version. Upgrading to this new version will..."
---

> **Note**: This post was published over 5 years ago and may contain outdated information. Tool versions, syntax, and best practices may have changed. Please verify current documentation before implementing.
{: .notice--warning}


Here is a quick walk through on upgrading an existing VDS (Distributed
Switch) to version 5.1 from an older version. Upgrading to this new
version will give you the following new features. Network health check,
rollback and recovery, LACP and [more](http://www.vmware.com/files/pdf/products/vsphere/vmware-what-is-new-vsphere51.pdf "https\://www.vmware.com/files/pdf/products/vsphere/vmware-what-is-new-vsphere51.pdf").
I would highly recommend upgrading to this latest version. And as you
will see below it is very quick and easy.

Log into new web interface and get started.

Once you are logged in here is what you will see.

![2012-09-17_20-53-22](../../assets/2012-09-17_20-53-22-300x149.png )

Click on networking

![2012-09-17_20-54-02](../../assets/2012-09-17_20-54-02-300x189.png )

Right click on dvswitch (Your's may be named differently) and select
"Upgrade Distributed Switch"

![2012-09-17_20-54-51](../../assets/2012-09-17_20-54-51-300x182.png )

Now just click through the next few screens and verify that it says
compatible. And Click finish. And make sure it is reports as completed
successful over on the right side pane.

![2012-09-17_20-56-03](../../assets/2012-09-17_20-56-03-300x175.png )

![2012-09-17_20-56-21](../../assets/2012-09-17_20-56-21-300x175.png )

![2012-09-17_20-56-42](../../assets/2012-09-17_20-56-42-300x96.png )

And that's it. Very simple. Now go migrate your management console
ports into your VDS and have the comfort of rollback functionality if
something goes wrong in the process.
