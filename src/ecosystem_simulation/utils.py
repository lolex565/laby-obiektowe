import csv
import os


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

def create_csv_file(file_name: str, data: list) -> None:
    """Tworzy plik csv z podanymi danymi"""
    header = ['tura', 'populacja', 'drapieżniki', 'ofiary', 'bobry']
    if not os.path.exists('csv'):
        os.makedirs('csv')
    with open(f'csv/{file_name}', "w", newline='', encoding='UTF8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)
        file.close()