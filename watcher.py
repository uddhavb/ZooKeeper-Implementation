#
# def changeMade():
#     players = zk.get_children("/")
#     scores = {}
#     # print(players)
#     for player in players:
#         @zk.ChildrenWatch("/" + player)
#         def watch_children(children):
#             # print("Children are now: %s" % children)
#             for child in children:
#                 @zk.DataWatch("/"+player+"/"+child)
#                 def watch_node(data, stat):
#                     # print("Version: %s, data: %s" % (stat, data.decode("utf-8")))
#                     scores[player+"~"+child] = [data.decode("utf-8"),stat.ctime]
#     # print(scores)
#     # sort by creation time in revers order(most recent first)
#     most_recent = sorted(scores.items(), key=lambda e: e[1][1], reverse = True)
#     print(most_recent[0:lsize])
#     highest_scores = sorted(scores.items(), key=lambda e: e[1][0], reverse = True)
#     print(highest_scores)

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
    while(True):
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
        # do only if any update has been made
        if True:
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
            print("\t\t\t\tMost recent scores\n\t\t\t--------------------------------")
            for i in range(lsize):
                name = most_recent[i][0].split('~')[0]
                online = ""
                data, stat = zk.get("/online_players")
                online_players = (data.decode("utf-8")).split('~')
                if name in online_players:
                    online = "**"
                print(name + "\t\t\t" + most_recent[i][1][0] + "\t" + online)

            highest_scores = sorted(scores.items(), key=lambda e: e[1][0], reverse = True)
            print("\t\t\t\tHighest scores\n\t\t\t--------------------------------")
            for i in range(lsize):
                name = highest_scores[i][0].split('~')[0]
                online = ""
                data, stat = zk.get("/online_players")
                online_players = (data.decode("utf-8")).split('~')
                if name in online_players:
                    online = "**"
                print(name + "\t\t\t" + highest_scores[i][1][0] + "\t" + online)

        sleep(5)
except KeyboardInterrupt:
    print("Watcher exited")
