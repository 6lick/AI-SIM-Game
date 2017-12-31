import networkx as nx
import random
import matplotlib.pyplot as plt
import sys
import time
import itertools



board = nx.Graph()
playerBoard = nx.Graph()
cpuBoard = nx.Graph()

board.add_nodes_from(['A','B','C','D','E','F','G','H'])
playerBoard.add_nodes_from(['A','B','C','D','E','F','G','H'])
cpuBoard.add_nodes_from(['A','B','C','D','E','F','G','H'])

def addPlayerEdge():
    newEdge = input("Please enter the the two nodes you would like to draw a line between\n")
    nodes = list(newEdge)
    if not (board.has_edge(nodes[0], nodes[1])):
        board.add_edge(nodes[0],nodes[1],color='b')
        playerBoard.add_edge(nodes[0], nodes[1])
        
        return 0
    else:
        print("An edge already exists between those two nodes")
        addPlayerEdge(board)


def cpuNodeGen():
    letters = ['A','B','C','D','E','F','G','H']
    b = random.randint(0,7)
    a = random.randint(0,7)
    while (a == b):
        a = random.randint(0,7)
    node1 = letters[b]
    node2 = letters[a]
    return (node1, node2)


def removeduplicates(a):
  seen = set()
  dups = list()

  for i in a:
    if i not in seen:
      seen.add(i)
    else:
        dups.append(i)
  return dups 
    
def addCpuEdge():
    nodes = cpuNodeGen()
    ##todo minimize edges that would create second edge of triangle -check if either nodes match any node in current cpu edge list
    CPUedges = cpuBoard.edges()
    cpuEdges = list(itertools.chain(*CPUedges))

    playerEdges = playerBoard.edges()
    PlayerEdges = list(itertools.chain(*playerEdges))

    #maximize mixed trianlges
    dups = removeduplicates(playerEdges)

    #maximize partially mixed trianlges
    #avoid multiedges
    while cpuBoard.has_edge(nodes[0], nodes[1]) or cpuBoard.has_edge(nodes[1], nodes[0]) or playerBoard.has_edge(nodes[1],nodes[0]) or playerBoard.has_edge(nodes[0], nodes[1]):
        nodes = cpuNodeGen()

    #minimize loser edges
    if (nodes[0] in cpuEdges) or (nodes[1] in cpuEdges):
        nodes = cpuNodeGen()
    #maxi
    if (nodes[0] in playerEdges) and nodes[0] not in dups:
        cpuBoard.add_edge(nodes[0], nodes[1])
        board.add_edge(nodes[0], nodes[1], color='r')
        print("cpu added edge ",nodes[0], nodes[1])
        return
    #else:
        
    if (nodes[1] in playerEdges):
        cpuBoard.add_edge(nodes[0], nodes[1])
        board.add_edge(nodes[0], nodes[1], color='r')
        print("cpu added edge ",nodes[0], nodes[1])
        return

    cpuBoard.add_edge(nodes[0], nodes[1])
    board.add_edge(nodes[0], nodes[1], color='r')
    print("cpu added edge ",nodes[0], nodes[1])






##################game begins here
#player goes first, board will be shown after first move
playGame = True
while playGame:
    addPlayerEdge()
    addCpuEdge()
          
    edges = board.edges()
    colors = [board[u][v]['color'] for u,v in edges]   
    nx.draw_circular(board, with_labels=True, edge_color=colors)
    plt.ion()
    plt.show()
    userTri = nx.triangles(playerBoard)
    for i in userTri.values():
        if i > 0:
            print("CPU wins")
            playGame = False
            exit()
    cpuTri = nx.triangles(cpuBoard)
    for i in cpuTri.values():
        if i > 0:
            print("Player wins")
            time.sleep(60)
            playGame = False
            exit()
    
cpuBoard.add_edge('A','B')
cpuBoard.add_edge('B','C')
edges = list(cpuBoard.edges())
#b = list(map(lambda x: x[0], list(cpuBoard.edges())))


print(b)
