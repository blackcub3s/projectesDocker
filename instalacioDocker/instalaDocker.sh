######################
#     INSTALACIÓ     #
######################

# netejar possibles versions anteriors
sudo apt remove docker docker-engine docker.io containerd runc

#actualitzar respositoris i instalar

sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$UBUNTU_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update


#ACTUALITZO I INSTALO docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


###########################
#     POST INSTALACIÓ     #
###########################
# CAL modificar els permisos de l'arxiu /var/run/docker.sock per al teu usuari.
# Si no, en fer docker version (entre altres comandes), petarà:
 sudo chmod ugo+rwx /var/run/docker.sock
