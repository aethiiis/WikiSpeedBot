from math import floor
from queue import PriorityQueue
from request import get_wikipedia_links
from semantic_text_similarity.models import WebBertSimilarity

def heuristic(a, b):
    return 5 - web_model.predict([(getSubject(a),getSubject(b))])

def init():
    begin = input("Quel est le sujet de départ ? ")
    start = getUrl(begin)
    end = input("Quel est le sujet de fin ? ")
    arrival = getUrl(end)
    return start, arrival

def getUrl(word):
    url = "https://en.wikipedia.org/wiki/" + word.replace(" ", "_")
    return url

def getSubject(url):
    word = url[30:].replace("_", " ")
    return word

def astar(start, arrival):

    frontier = PriorityQueue()
    frontier.put((0, start))

    came_from = dict()
    cost_so_far = dict()
    
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current[1] == arrival:
            print("On a trouvé !")
            break

        links = get_wikipedia_links(current[1])
        
        for next in links:
            min_heuristic = 5
            print("\r", end="", flush=True)
            print("Current : ")
            print(current[1])
            print("Next : ")
            print(next)

            new_cost = cost_so_far[current[1]] + 1

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                similarity = heuristic(arrival, next)
                if similarity < min_heuristic:
                    min_heuristic = similarity
                    cost_so_far[next] = new_cost
                    frontier.put((floor((new_cost + similarity) * 100), next))
                    came_from[next] = current[1]
                if similarity < 1:
                    break

    avant = came_from[arrival]
    apres = arrival
    liste = [getSubject(arrival)]
    while avant != None:
        if came_from[apres] != None:
            liste.insert(0, getSubject(came_from[apres]))
        apres = came_from[apres]
        avant = apres
    
    print(liste)
    
if __name__ == "__main__":
    web_model = WebBertSimilarity(device='cpu', batch_size=100)
    start, arrival = init()
    astar(start, arrival)
