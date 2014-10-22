lb clean --binary
unlink chroot/sbin/true
cp backup/start-stop-daemon chroot/sbin/
rm chroot/var/lib/apt/lists/ftp*
lb binary iso
