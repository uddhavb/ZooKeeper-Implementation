
def my_listener(state):
    if state == KazooState.LOST:
        raise Exception("Connection to Zookeeper server lost")
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        raise Exception("Connection to Zookeeper server suspended")
    else:
        # Handle being connected/reconnected to Zookeeper
        return


def addScore(name, score):
    if(not zk.exists(name)):
        # if the player does not exist, then create an entry for the player
        zk.ensure_path(name)
        zk.create(name+"/1", score)
    else:
        # create a new version(child node) for the player node to add the latest score
        children = zk.get_children(name)
        children = list(map(int, children))
        children.sort()
        scoreVersion = str(children[-1] + 1)
        print(scoreVersion)
        zk.create(name + '/' + scoreVersion, score)

def goOffline():
    # remove player from online players list
    data, stat = zk.get("/online_players")
    online_players = (data.decode("utf-8")).split('~')
    online_players.remove(name[1:])
    new_list =  bytes('~'.join(online_players))
    zk.set("/online_players", new_list)

def goOnline():
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
try:
    zk.start()
except:
    raise Exception("\n\nUnable to connect to IP:Port or zookeeper service is inactive\n\n")
try:
    name = "/"+sys.argv[2]
except:
    raise Exception("\n\nEnter name of player")
# keep a list of online players
# if player is already online then throw exception and exit
# add player to online players list
if(not zk.exists("/online_players")):
    zk.create("/online_players", "")

data, stat = zk.get("/online_players")
online_players = (data.decode("utf-8")).split('~')
if name[1:] in online_players:
    raise Exception("\n\n\nPlayer is already online\n\n")
try:
    # add player to the online players list
    goOnline()

    # get the automated testing test case inputs
    if(len(sys.argv) > 3):
        if len(sys.argv)<6:
            print "\n\nPlease enter count, delay and score"
            raise Exception("\n\nPlease enter count, delay and score")
        count = int(sys.argv[3])
        delay = int(sys.argv[4])
        score = int(sys.argv[5])

    try:
        print(name[1:] + " is online")
        try:
            delay
        except:
               # if delay and score are not specified, continuously take input from user
            while(True):
                try:
                    score = bytes(str(int(input('Enter your score: '))).encode("utf-8"))
                except ValueError:
                    print("Please enter Integer value for score")
                addScore(name,score)
                print("Score posted:  " + score)
        # if delay and score is given (for test automation)
        import numpy
        from time import sleep
        # get normally distributed values for delay and score. Ensure that they are positive
        delays = abs(numpy.random.normal(delay, 0.01, count))
        scores = abs(numpy.random.normal(score, 10000, count))
        count -= 1 # To index lists
        while(count>=0):
            sleep(delays[count])
            score = bytes(str(int(scores[count])).encode("utf-8"))
            addScore(name,score)
            print("Score posted:  " + score)
            count -= 1
        goOffline()
        # zk.stop()
    except KeyboardInterrupt:
        goOffline()
        print "\nplayer exited"
        zk.stop()
except Exception as ex:
    goOffline()
    zk.stop()
    print "\nplayer exited"
