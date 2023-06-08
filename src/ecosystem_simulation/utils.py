import csv
import os
import matplotlib.pyplot as plt



def move_towards_point(x: int, y: int, x2: int, y2: int, distance: int) -> tuple:
        """Przesuwa się w kierunku punktu"""
        if x2 == x and y2 == y:
            return (x, y)
        if x2 == x:
            if y2 > y:
                return (x, y + distance)
            else:
                return (x, y - distance)
        if y2 == y:
            if x2 > x:
                return (x + distance, y)
            else:
                return (x - distance, y)
        if x2 > x:
            if y2 > y:
                return (x + distance, y + distance)
            else:
                return (x + distance, y - distance)
        else:
            if y2 > y:
                return (x - distance, y + distance)
            else:
                return (x - distance, y - distance)
            
def move_away_from_point(x: int, y: int, x2: int, y2: int, distance: int) -> tuple:
    """Przesuwa się zdala od punktu"""
    if x2 == x and y2 == y:
        return (x, y)
    if x2 == x:
        if y2 > y:
            return (x, y - distance)
        else:
            return (x, y + distance)
    if y2 == y:
        if x2 > x:
            return (x - distance, y)
        else:
            return (x + distance, y)
    if x2 > x:
        if y2 > y:
            return (x - distance, y - distance)
        else:
            return (x - distance, y + distance)
    else:
        if y2 > y:
            return (x + distance, y - distance)
        else:
            return (x + distance, y + distance)
        

def name_to_emoji(name: str) -> str:
    """Zamienia nazwę obiektu na emoji"""
    emojis = {
        "Beaver": "🦫",
        "Wolf": "🐺",
        "Eagle": "🦅",
        "Mouse": "🐭",
        "Deer": "🦌",
        "Tree": "🌲",
        "Plant": "🌱",
        "Water": "💧",
        "Dirt": "🟫", 
        "Rock": "🪨",
    }

    return emojis.get(name, "❓")

def create_csv_file(file_name: str, data: list) -> str:
    """Tworzy plik csv z podanymi danymi"""
    header = ['tura', 'populacja', 'drapieżniki', 'ofiary', 'bobry', 'rośliny', 'drzewa', 'woda']
    if not os.path.exists('csv'):
        os.makedirs('csv')
    with open(f'csv/{file_name}', "w", newline='', encoding='UTF8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)
        file.close()
    return file_name


def create_single_graph(folder_name: str, file_name: str, title: str, data: [], turns: []) -> None:
    colors = ['red', 'blue', 'green', 'brown', 'orange', 'purple', 'pink', 'black']
    for series in data:
        plt.plot(turns[0], series[0], label=series[1], color=colors.pop(0))
    plt.xlabel('tura')
    plt.ylabel('liczebność')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'graphs/{folder_name}/{file_name}.png')
    plt.close()

def create_graphs(file_name: str) -> None:
    """Tworzy wykres z podanego pliku csv"""
    with open(f'csv/{file_name}.csv', newline='', encoding='UTF8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        data = list(reader)
        file.close()
    turns = [[], 'tury']
    population = [[], 'populacja']
    predators = [[], 'drapieżniki']
    prey = [[], 'ofiary']
    beavers = [[], 'bobry']
    plants = [[], 'rośliny']
    trees = [[], 'drzewa']
    water = [[], 'woda']
    for row in data:
        turns[0].append(int(row[0]))
        population[0].append(int(row[1]))
        predators[0].append(int(row[2]))
        prey[0].append(int(row[3]))
        beavers[0].append(int(row[4]))
        plants[0].append(int(row[5]))
        trees[0].append(int(row[6]))
        water[0].append(int(row[7]))
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    os.makedirs(f'graphs/{file_name}')
    create_single_graph(file_name, 'population', 'Populacja', [population, predators, prey, beavers], turns)
    create_single_graph(file_name, 'predatorAndPrey', 'Drapieżniki i ofiary', [predators, prey], turns)
    create_single_graph(file_name, 'beaversAndTrees', 'Bobry i drzewa', [beavers, trees], turns)
    create_single_graph(file_name, 'preysAndPlants', 'Ofiary i rośliny', [prey, plants], turns)
    create_single_graph(file_name, 'populationAndWater', 'Woda i populacja', [water, population], turns)
