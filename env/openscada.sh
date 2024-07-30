sudo apt update -y
sudo apt install wget -y
echo "deb http://ftp.oscada.org/OpenSCADA/LTS/Ubuntu/22.04 ./" | sudo tee -a /etc/apt/sources.list
sudo wget -P /etc/apt/trusted.gpg.d http://ftp.oscada.org/Misc/openscada-archive-keyring.asc
sudo apt update -y
sudo apt install openscada-server -y
sudo service openscada-server start 
