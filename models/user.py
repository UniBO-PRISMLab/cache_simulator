import random


class User:
    def __init__(self, user_id, start_position, end_position, speed, grid_size):
        self.user_id = user_id
        self.start_position = start_position
        self.end_position = end_position
        self.speed = speed
        self.grid_size = grid_size
        self.current_position = start_position
        self.time = 0
        self.reached_end_position = False

    def move(self, time):
        self.time = time
        distance = self.speed * time
        dx = self.end_position[0] - self.start_position[0]
        dy = self.end_position[1] - self.start_position[1]
        total_distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        if distance >= total_distance:
            self.current_position = self.end_position
            self.reached_end_position = True
        else:
            unit_x = dx / total_distance
            unit_y = dy / total_distance
            # Calculate grid-based position
            grid_x = int(self.start_position[0] + (unit_x * distance))
            grid_y = int(self.start_position[1] + (unit_y * distance))
            # Adjust position to fit within grid size
            grid_x = max(min(grid_x, self.grid_size), 0)
            grid_y = max(min(grid_y, self.grid_size), 0)
            self.current_position = (grid_x, grid_y)
            self.reached_end_position = False

    def get_position(self):
        return self.current_position

    def get_position_at_time(self, time):
        if time >= self.time:
            self.move(time - self.time)
        return self.current_position if self.current_position != self.end_position else self.end_position

    def has_reached_end_position(self):
        return self.reached_end_position

    def update_end_position(self):
        if self.reached_end_position:
            self.end_position = self.generate_random_end_position()

    def generate_random_end_position(self):
        x = random.randint(0, self.grid_size)
        y = random.randint(0, self.grid_size)
        return (x, y)

    def __str__(self):
        return f"User {self.user_id} - Current Position: {self.current_position} - Time: {self.time}"
