sudo chmod -R 777 *
sudo cp hacker_news.service /etc/systemd/system/
sudo systemctl start hacker_news.service
sudo systemctl enable hacker_news