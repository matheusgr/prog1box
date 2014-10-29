lb clean --binary
# usually you want link start-stop-daemon to /bin/true before changing chroot
unlink chroot/sbin/start-stop-daemon
cp backup/start-stop-daemon chroot/sbin/
# clean some space
rm chroot/var/lib/apt/lists/ftp*
lb binary iso
chmod a+r live-image-amd64.hybrid.iso
