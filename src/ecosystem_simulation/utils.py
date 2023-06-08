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
    header = ['tura', 'populacja', 'drapieżniki', 'ofiary', 'bobry']
    if not os.path.exists('csv'):
        os.makedirs('csv')
    with open(f'csv/{file_name}', "w", newline='', encoding='UTF8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)
        file.close()
    return file_name


def create_graph(file_name: str) -> None:
    """Tworzy wykres z podanego pliku csv"""
    with open(f'csv/{file_name}', newline='', encoding='UTF8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        data = list(reader)
        file.close()
    turns = []
    population = []
    predators = []
    prey = []
    beavers = []
    for row in data:
        turns.append(int(row[0]))
        population.append(int(row[1]))
        predators.append(int(row[2]))
        prey.append(int(row[3]))
        beavers.append(int(row[4]))
    plt.plot(turns, population, label="populacja", color='black')
    plt.plot(turns, predators, label="drapieżniki", color='red')
    plt.plot(turns, prey, label="ofiary", color='green')
    plt.plot(turns, beavers, label="bobry", color='brown')
    plt.xlabel('tura')
    plt.ylabel('liczebność')
    plt.title('populacje w czasie')
    plt.legend()
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    plt.savefig(f'graphs/{file_name}.png')
    plt.close()