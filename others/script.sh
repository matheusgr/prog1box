# Reboot?
#reboot

# Pagina inicial:
echo 'http://tst-online.appspot.com/l' > /tmp/pagina

echo "nameserver 8.8.8.8
nameserver 8.8.4.4" > /etc/resolv.conf

unset http_proxy
unset https_proxy

# Configurando TST:
wget https://dl.dropboxusercontent.com/u/9427789/tst/tst.zip
unzip -o tst.zip -d /usr/local/bin
chmod a+x /usr/local/bin/*.py
rm tst.zip

# Se a URL comecar igual a uma dessas linhas, libere o acesso
echo "https://docs.python.org
http://docs.python.org
https://www.google.com/a/ccc.ufcg.edu.br/ServiceLogin?
https://dl.dropboxusercontent.com/u/12935044
https://dl.dropboxusercontent.com/u/12935044/
https://dl.dropboxusercontent.com/u/12935044/quadradoinscrito1.jpg
https://dl.dropboxusercontent.com/u/74287933/2013.2/ranking.txt
https://dl.dropboxusercontent.com/u/74287933/2013.2/lr.html
https://dl.dropboxusercontent.com/u/74287933/2013.2/last-results.dat
http://dl.dropboxusercontent.com/u/74287933/2013.2/last-results.dat
http://bit.ly/resultadostst
http://upload.wikimedia.org/
https://dl.dropboxusercontent.com/u/9427789/images/fahrenheit_celsius.gif
http://dl.dropboxusercontent.com/u/9427789/images/fahrenheit_celsius.gif
http://dl.dropboxusercontent.com/u/37343177/pedagio.jpg
http://dl.dropbox.com/u/9427789/
http://dl.dropbox.com/u/9427789
http://dl.dropbox.com/u/9427789/images/matriz_interna.png
https://bigsnarf.files.wordpress.com/2012/03/distance.jpg
http://upload.wikimedia.org/math/4/1/f/41f3936d7053336f97dd59dee9d5df7b.png
http://upload.wikimedia.org/math/b/7/b/b7b326b6c8394786f8c373de98ceb161.png
http://upload.wikimedia.org/math/e/6/7/e678db0137d57dddf5d66f02a6fdf4ef.png
http://db.tt/bZsBY456
http://dl.dropboxusercontent.com/u/37343177/relogio.jpg
http://dl.dropboxusercontent.com/u/37343177/pedagio.jpg
http://dl.dropboxusercontent.com/u/37343177/cardshuffler.jpg
http://www.121mobility.co.uk/shop/wp-content/uploads/2013/12/Automatic-Card-Shuffler-500x380.jpg
http://upload.wikimedia.org/math/d/8/5/d858202192abadd0bb8a60fa9dd9b013.png
https://dl.dropboxusercontent.com/u/9427789/2012.2/figura.jpg
http://www.brasilescola.com/upload/e/Untitled-13(7).jpg
http://dl.dropboxusercontent.com/u/9427789/images/matriz_interna.png
http://dl.dropboxusercontent.com/u/37343177/planocartesiano.jpg
http://dl.dropboxusercontent.com/u/37343177/decimal_BCD.jpg
https://dl.dropboxusercontent.com/u/37343177/distribui_aluno.png
https://dl.dropboxusercontent.com/u/37343177/zenit.png
https://dl.dropboxusercontent.com/u/37343177/planocartesiano-distancia.jpg
https://dl.dropboxusercontent.com/u/37343177/alvo.jpeg
https://www.google.com/accounts/
https://www.google.com.br/accounts/
https://ssl.gstatic.com/
https://gg.google.com/
https://accounts.google.com/
https://accounts.youtube.com/
https://appengine.google.com/_ah/
https://accounts.google.com.br/
https://www.google.com/accounts/ClientLogin
http://tst-online.appspot.com
http://www.google.com/gen_204" > /tmp/sites

# Proibindo pendrives
echo "blacklist usb-storage" > /etc/modprobe.d/blacklist.conf
rmmod usb-storage

# Desativando o acesso ao CD
chmod 700 /media

# Desativando lock screen e log-out
sleep 1
su aluno -c 'DISPLAY=:0 dconf write /org/gnome/desktop/lockdown/disable-lock-screen true'
sleep 1
su aluno -c 'DISPLAY=:0 dconf write /org/gnome/desktop/lockdown/disable-log-out false'
sleep 1
su aluno -c 'DISPLAY=:0 dconf write /org/gnome/desktop/lockdown/disable-user-switching true'
sleep 1

# Desativando o screensaver
su aluno -c 'DISPLAY=:0 dconf write /org/gnome/desktop/screensaver/lock-enabled false'
sleep 1

# Configurando proxy para o aluno
su aluno -c 'DISPLAY=:0 dconf write /system/proxy/http/host \"localhost\"'
sleep 1
su aluno -c 'DISPLAY=:0 dconf write /system/proxy/mode \"manual\"'
sleep 1

# Setting ssh-auth-keys
mkdir /root/.ssh

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDqEnq1r5OEa7Qm7whja0QtoQJTOT8PxZXlzY4UNRlaiHS8PANknPNqqHiULT0EyOhmH4dxyWKWTfx+o1j3MxcVnRGazeIafnCuQzfK/WSO42kkSFiqRZRYHDsuuYL8cVceX2+sQbYvF2cYNkQGMeiMiDkolZ7NucfYQYU0CGltWLRjCONy5hk0hi3jMya5ZHAiENcmkPSTuIyUp/hglnJ7F7ZL/IICkyEuW03dMMGtz3lx6cSkqWEcvxY/pwfmENN0RTC+sNLguFgiNP+CQEGiFYbVhdbrwlTJyLJlKhsgfEb2en3ywPrlBz3GkVc9IcN/t3RJoI0aS5jL8FIVm2Fr root@borr
ssh-dss AAAAB3NzaC1kc3MAAACBAPd1jhQafokHcyH5IGEL2gENo9EoAhl4IX5dtP/3Ds3RJPqB0S8H4wcv2MI13QYVIsKH1T4zWwgWd2PzD2s/FsajReSstk2OnisPCgDpf2sJrasiVzZmw1QvOsQsvkNnpACPy4QURd3Ncs9f4l6gO5UjGrLeJJm64kBW4tV0q5z9AAAAFQDdiy2tFEftGHa2bJOj6L0dlvadAwAAAIA2QOoDa/JZDYWdAnugZzhO5WlrKjv5yCiiydHCCGusDmZjziV0h0ccem6VA9M3b7pzvC5cA2c7ujIYKMzfdNe7tLHA2043BT1hTKxd72MCEkSr0PSnGfD4HaYIw2b4W1wCD+Xcu3Kkadp6xb90q/hsK8p74IJHRMbrh9vwdy17IwAAAIEAuAp0QGjR8x0PVxD9Paov/OfJhofq7lfX4pv2lb975Apzto+jGXYpqkm2GGQohkAw5tNyGh1KF6GGnblEbRUwYy4kWFCdARa+/M9lSwPXHvX8LFl4nTvLUY4sDaVL77f1zCtWPt8r09AuhEgEJCgySEi+6p/+TyRepqlcMO+z0Ak= root@homer
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAkpLFWb25MihdQ/sX6jNcp/dcbTWfv02/ivy/sP8PVPKKgWASeAVaApOjqDzvrCArA/2txGMFi0mmW0czrkzzRIUF925qM3R1pqXZN1+sV2gK9WiuuiacGlzkzy5ixZWcXcSXDxqdzKxOxaaGfYJiwDnM58c7ET0zp7pR/eQVZFXET9bAUyeT5n3ZfFXEuHiuWoSH59SlCDNBg7oqhQzQFA6cPNqYTCs1llhZfpaDEnnlp0vfomlX4nZ3SNfXRJT3V7MQLICKa8F7T5plh3X8FdrDEkumOifKVl1wdsfHCrF4mVXG8PTco9kShcK5XzuVIhjSt7FQSNbpGNX4KJi/4Q== root@coisafofa" > /root/.ssh/authorized_keys

chmod -R go-rwx /root/.ssh