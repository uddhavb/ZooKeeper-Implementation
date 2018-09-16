def print_list():
    players = zk.get_children("/")
    scores = {}
    # print(players)
    for player in players:
        children = zk.get_children("/" + player)
        for child in children:
            data, stat = zk.get("/"+player+"/"+child)
            scores[player+"~"+child] = [data.decode("utf-8"),stat.ctime]
    # print(scores)
    # sort by creation time in reverse order(most recent first)

    most_recent = sorted(scores.items(), key=lambda e: e[1][1], reverse = True)
    print("\n\n\n\n\t\t\t\tMost recent scores\n\t\t\t--------------------------------")
    for i in range(lsize):
        name = most_recent[i][0].split('~')[0]
        online = ""
        data, stat = zk.get("/online_players")
        online_players = (data.decode("utf-8")).split('~')
        if name in online_players:
            online = "**"
        print("\t\t\t" + name + " "*(20 - len(name)) + most_recent[i][1][0] + "\t" + online)

    highest_scores = sorted(scores.items(), key=lambda e: e[1][0], reverse = True)
    print("\t\t\t\tHighest scores\n\t\t\t--------------------------------")
    for i in range(lsize):
        name = highest_scores[i][0].split('~')[0]
        online = ""
        data, stat = zk.get("/online_players")
        online_players = (data.decode("utf-8")).split('~')
        if name in online_players:
            online = "**"
        print("\t\t\t" + name + " "*(20 - len(name)) + highest_scores[i][1][0] + "\t" + online)



import sys
# first argument is the filename followed by the ip:property
#  default port 2181
ip_port = sys.argv[1]
#  then comes the list size that the watcher will print
lsize = int(sys.argv[2])

import logging
logger = logging.basicConfig()
print("-----Watcher Process-----")

# from zookeeper_watcher import ZookeeperWatcher
# watcher = ZookeeperWatcher(ip_port)
from kazoo.client import KazooClient
print(ip_port)
zk = KazooClient(hosts=ip_port)
from time import sleep
try:
    zk.start()
    # watch for changes to the online players list
    @zk.DataWatch("/online_players")
    def watch_online_players(data, stat):
        print_list()
    # list if existing players
    nodes = zk.get_children("/")
    # watch for addition of new players
    @zk.ChildrenWatch("/")
    def watch_children(children):
        for child in children:
            if child not in nodes:
                nodes.append(child)
                @zk.ChildrenWatch("/"+child)
                def watch_grand_children(grand_children):
                    print_list()
        # watch for activity of existing players
    for node in nodes:
        @zk.ChildrenWatch("/"+node)
        def watch_grand_children(grand_children):
            print_list()

    """
            Most recent scores
    ------------------
    Captain America      109569 **
    Thor                  99874
    Captain America      175010 **
    Smaug                  5015 **
    Thor                 111111
    Bob                  202014 **

            Highest scores
    --------------
    Prof Freeh        972430194
    Prof Freeh        883284030
    Prof Freeh        873920103
    Prof Freeh        859883839
    Prof Freeh        859893835
    Bob                  202014  **
    """
    while(True):
        sleep(5)
except KeyboardInterrupt:
    print("Watcher exited")
