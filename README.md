Prog1Box is a live image created to be used at a programming classroom.

It's a live CD that can be also booted through grub using the squashfs file or by a VirtualMachine using the ISO file.

Building your Image
===================

You will need the **live-images** package (4.0 - http://live.debian.net/)

You may test now how the live-images works. It will do almost all things automatically (run lb build as root).

```
$ mkdir live-default && cd live-default
$ lb config
# lb build
```

You need to change some configuration files to lookdown your image. See those files on *live-image_config/* compare them with the files created on *live-default/config/*.

You also need to install some packages. You can do this by chroot to *chroot* dir. You can see the full list of installed packages at *others/debian_packages* file.

Also, additional files must be added to the image. Those files are at *image_chroot*.

After change those files, running **lb binary** will recreate your image.

You may need to copy isolinux files to live-image\_config/bootloaders/ to make the image bootable.

Google App Engine
=================

The application that controls a Prog1Box runs at Google App Engine and has its source at the *gae* directory. You can configure which server a image will contact by change the Prog1Box client application (*/root/client.py*).

Other Files
===========

You also have access to files that may help you to deploy your application:

   * *others/grub* - Grub file to boot a squashfs (copy *live-default/binary/live* to */boot/labp1/live*)
   * *script.sh* - An example of script to be used at Prog1Box server
   * *compile.sh* - Script to do an iso after any change on chroot
