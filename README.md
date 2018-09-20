# Zookeeper game   

### ZooKeeper version   
I have used the lastest stable release of zookeeper (version 12) to run and test my software.   

### basic requirements  

Python minimal and pip.   
pip libraries: kazoo, logging, numpy   

The scripts and zookeeper server are run and tested in Ubuntu Xenial   
Run `setup.sh`   

## To run the player and watcher programs   
### Watcher:   
`python watcher.py 12.34.45.87:6666 N`   
-- where N is an integer   

### Player:   
`python player.py 12.34.45.87:6666 name`  
`python player.py 12.34.45.87:6666 "first last"`   
`python player.py 12.34.45.87:6666 name count delay score`   
