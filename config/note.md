buy rasberry pi to party

##config file directions

saved here, should move to cd ~/.config/systemd/user

## execute commands
**1. login to device**
ssh twenty@<PI_IP_ADDRESS>

**2. create file**
~/402-crawler && cd ~/402-crawler

**3. enable service**
systemctl --user enable 402-crawler.timer
systemctl --user start 402-crawler.timer
systemctl --user start 402-crawler.service
systemctl --user daemon-reload

**4. disable service**
systemctl --user stop 402-crawler.timer
systemctl --user disable 402-crawler.timer
systemctl --user stop 402-crawler.service
