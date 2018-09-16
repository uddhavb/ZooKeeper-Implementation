def goOffline():
    # remove player from online players list
    data, stat = zk.get("/online_players")
    online_players = (data.decode("utf-8")).split('~')
    online_players.remove(name[1:])
    new_list =  bytes('~'.join(online_players))
    zk.set("/online_players", new_list)

def goOnline():
    # add player to online players list
    if(not zk.exists("/online_players")):
        zk.create("/online_players", name[1:])
    else:
        data, stat = zk.get("/online_players")
        online_players = (data.decode("utf-8")).split('~')
        if(name[1:] not in online_players):
            online_players.append(name[1:])
        new_list =  bytes('~'.join(online_players))
        zk.set("/online_players", new_list)

import sys
# first argument is the filename followed by the ip:property
# then comes the name, and optinally( count, delay and score)
#  default port 2181
ip_port = sys.argv[1]

# start the zookeeper client
from kazoo.client import KazooClient
zk = KazooClient(hosts=ip_port)
zk.start()

name = "/"+sys.argv[2]
# keep a list of online players
goOnline()

if(len(sys.argv) > 3):
    count = int(sys.argv[3])
    delay = int(sys.argv[4])
    score = int(sys.argv[5])

try:
    print(name[1:] + " is online")

    try:
        delay
    except:
           # if no delay and score specified continuously take input from user
        while(True):
            if(not zk.exists(name)):
                try:
                    score
                except NameError:
                    score = bytes(str(input('Enter your score: ')).encode("utf-8"))
                zk.ensure_path(name)
                zk.create(name+"/1", score)
            else:
                score = bytes(str(input('Enter your score: ')).encode("utf-8"))
                children = zk.get_children(name)
                children = list(map(int, children))
                children.sort()
                scoreVersion = str(children[-1] + 1)
                zk.create(name + '/' + scoreVersion, score)
            print("Score posted:  " + score)
    # if delay and score is given
    import numpy
    from time import sleep
    delays = abs(numpy.random.normal(delay, 0.01, count))
    scores = abs(numpy.random.normal(score, 10000, count))
    count -= 1 # To index lists
    while(count>=0):
        sleep(delays[count])
        if(not zk.exists(name)):
            score = bytes(str(int(scores[count])).encode("utf-8"))
            zk.ensure_path(name)
            zk.create(name+"/1", score)
        else:
            score = bytes(str(int(scores[count])).encode("utf-8"))
            children = zk.get_children(name)
            children = list(map(int, children))
            children.sort()
            scoreVersion = str(children[-1] + 1)
            print(scoreVersion)
            zk.create(name + '/' + scoreVersion, score)
        print("Score posted:  " + score)
        count -= 1
    goOffline()
except KeyboardInterrupt:
    goOffline()
    print("\nplayer exited")
    zk.stop()
