import random

GRID_WIDTH = 50
GRID_HEIGHT = 50
MAX_ROOM_SIZE = 10
MIN_ROOM_SIZE = 5
NUM_ROOMS = 20

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def generate_room():
    width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
    height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
    x = random.randint(0, GRID_WIDTH - width - 1)
    y = random.randint(0, GRID_HEIGHT - height - 1)
    return x, y, width, height

def place_room(room):
    x, y, width, height = room
    for i in range(x, x + width):
        for j in range(y, y + height):
            grid[i][j] = 1

def create_corridor(room1, room2):
    x1, y1 = room1[0] + room1[2] // 2, room1[1] + room1[3] // 2
    x2, y2 = room2[0] + room2[2] // 2, room2[1] + room2[3] // 2

    if random.choice([True, False]):
        create_h_corridor(x1, x2, y1)
        create_v_corridor(y1, y2, x2)
    else:
        create_v_corridor(y1, y2, x1)
        create_h_corridor(x1, x2, y2)

def create_h_corridor(x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        grid[x][y] = 1

def create_v_corridor(y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        grid[x][y] = 1

rooms = []
for _ in range(NUM_ROOMS):
    room = generate_room()
    rooms.append(room)
    place_room(room)

for i in range(1, len(rooms)):
    create_corridor(rooms[i-1], rooms[i])

# Print the grid
for row in grid:
    print("".join(["#" if cell == 0 else "." if cell == 1 else "E" for cell in row]))
