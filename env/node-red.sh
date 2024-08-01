sudo apt update
sudo snap install docker 
sudo docker run -it -p 1880:1880 -v node_red_data:/data --name nodered nodered/node-red 
