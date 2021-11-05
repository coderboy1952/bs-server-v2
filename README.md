This is Bombsquad Server Scripts

# To Run Server Run The Following Commands In Sequence

## [ONE TIME SETUP COMMANDS]
```
sudo apt-get update
```

For Ubuntu14.04
    
    sudo apt-get install python2.7 libsdl2-2.0
 
For Ubuntu16.04 or Up
    
    sudo apt-get install python libsdl2-2.0-0 libpython2.7

For Installing Scripts

    git clone https://github.com/coderboy1952/bs-server
    
Command For Installing Apache On Server

    sudo apt-get install apache2

Command For Giving Permission  If Access Denied
    
    sudo chown -R google /var/www/html/
    
NOTE: Username can be `root, ubuntu, google...etc`

    
## [TO START BOMBSQUAD SERVER]
```
cd bs-server
```
```
chmod 777 bs_headless
```
```
chmod 777 bombsquad_server
```
```
chmod 777 config.py
```
```
tmux
```
```
./bombsquad_server
```
## [TO CLOSE BOMBSQUAD SERVER]
```
pkill -f tmux
```
