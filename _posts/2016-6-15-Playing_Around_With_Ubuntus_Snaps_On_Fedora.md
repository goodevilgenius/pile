---
date: 2016-06-15 16:16:45-05:00
layout: post
link_url: https://www.phoronix.com/scan.php?page=article&item=ubuntu-snaps-fedora&num=1
tags:
- programming
- linux
- applications
timestamp: 1466025405
title: Playing Around With Ubuntu's Snaps, On Fedora
type: link

---
> Executing `snap find *` returned a... less than impressive list. In total there were 7 snaps available from the store for install-- 2 of which were example applications provided by Ubuntu.
>
> Now, to be fair to Canonical and Snapper... The idea behind Snapper is that of OS X (now MacOS) bundles. You don't download them from a central repository, you download them from the application authors directly.
>
> When one issues "sudo snap install" on an application, part of the downloading output is the total size of the snap. Since snap uses bundled libraries, I was rather curious to see how big these relatively simple applications would be:
>
> Ubuntu Clock App: 120.11 MB – admittedly, this is written in QML, so it has to pull in Qt. Ubuntu Calc App: 120.01 MB – same as above. LibreOffice*... 1.1 GB
>
> he Document Foundation's download page lists the sizes of all the various installers, broken down by operating system.
Windows x64? 238 MB. Mac OS X? 201 MB. Linux x64 RPM? 229 MB Linux x64 Deb? 229 MB
>
> So, even if you took all the installers for every OS and added them together, you would still come out at less used space than the single LibreOffice 5.2 Beta .snap package. To snap's credit, it did function. Less to snap's credit...the binary appeared to be Ubuntu-specific.

This seems incredibly wasteful of space. Every package includes all of its dependencies. What's the point in even having a package manager, then?

However, there was a very good point made on [Reddit](https://www.reddit.com/r/linux/comments/4o7d8y/playing_around_with_ubuntus_snaps_on_fedora/):

> Reading the comments I feel like people are missing the point of snaps. They aren't intended to replace your distro's package manager. I'm not even sure why some packages are in the snap repo, except perhaps to test it with certain large packages? (ie libreoffice?). What distro doesn't have Libreoffice?
>
> In my mind, snaps are best for applications that aren't in your distro already. Yes, they become inefficient on disk space (although space is cheap) but that one packages works on every distro that supports snaps.