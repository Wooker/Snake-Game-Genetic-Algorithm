import random
import random
import time
import math
from tqdm import tqdm
import numpy as np
import pygame


# Function to Display snake
def display_snake(snake_position, display):
    for position in snake_position:
        pygame.draw.rect(
            display, (0, 0, 0), pygame.Rect(position[0], position[1], 10, 10)
        )


# Function to Display apple
def display_apple(apple_position, display):
    pygame.draw.rect(
        display, (255, 0, 0),
        pygame.Rect(apple_position[0], apple_position[1], 10, 10)
    )


# Function for Initialising game with starting positions.
def starting_positions():
    snake_start = [100, 100]
    snake_position = [[100, 100], [90, 100], [80, 100]]
    apple_position = [
        random.randrange(1, 50) * 10, random.randrange(1, 50) * 10
    ]
    score = 0

    return snake_start, snake_position, apple_position, score

# Function to Calculate distance between apple and snake.
def apple_distance_from_snake(apple_position, snake_position):
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))

# Function to Generate snake based on its direction of movement.
def generate_snake(snake_start, snake_position, apple_position, button_direction, score, moves, count_loop):
    if len(moves) != 0 and snake_start == moves[count_loop] and snake_start in moves:
        count_loop += 1
    else:
        moves.append(list(snake_start))


    if button_direction == 1:
        snake_start[0] += 10
    elif button_direction == 0:
        snake_start[0] -= 10
    elif button_direction == 2:
        snake_start[1] += 10
    else:
        snake_start[1] -= 10

    if snake_start == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0, list(snake_start))
        if len(moves) != 0:
            moves = []
            count_loop = -1
            # print(f"{moves}, {count_loop}");
    else:
        snake_position.insert(0, list(snake_start))
        snake_position.pop()


    return snake_position, apple_position, score, moves, count_loop

# Function to check if snake has reached apple. 
def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score

# Function to check if snake has collided with a boundary. 
def collision_with_boundaries(snake_start):
    if snake_start[0] >= display_width or snake_start[0] < 0 or snake_start[1] >= display_height or snake_start[1] < 0:
        return 1
    else:
        return 0

# Function to check if snake has collided with itself. 
def collision_with_self(snake_start, snake_position):
    # snake_start = snake_position[0]
    if snake_start in snake_position[1:]:
        return 1
    else:
        return 0

# Function returns blocked directions for the snake based on its current position.
def blocked_directions(snake_position):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

# Function to check if a direction is blocked for the snake. 
def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector
    snake_start = snake_position[0]
    if collision_with_boundaries(next_step) == 1 or collision_with_self(next_step.tolist(), snake_position) == 1:
        return 1
    else:
        return 0

# Function returns direction. 
def generate_button_direction(new_direction):
    button_direction = 0
    if new_direction.tolist() == [10, 0]:
        button_direction = 1
    elif new_direction.tolist() == [-10, 0]:
        button_direction = 0
    elif new_direction.tolist() == [0, 10]:
        button_direction = 2
    else:
        button_direction = 3

    return button_direction

# Function to evaluate angle between apple and snake. 
def angle_with_apple(snake_position, apple_position):
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 10
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[0]) / math.pi
    return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized

# Function to play the game. 
def play_game(snake_start, snake_position, apple_position, button_direction, score, display, clock, moves, count_loop):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill((255, 255, 255))

        display_apple(apple_position, display)
        display_snake(snake_position, display)

        snake_position, apple_position, score, moves, count_loop = generate_snake(snake_start, snake_position, apple_position,
                                                               button_direction, score, moves, count_loop)

        pygame.display.set_caption("SCORE: " + str(score))
        font = pygame.font.Font('freesansbold.ttf', 32)
 
        # create a text surface object,
        # on which text is drawn on it.
        text = font.render("SCORE: " + str(score), True, (0, 255, 0), (0, 0, 255))
 
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
 
        # set the center of the rectangular object.
        textRect.center = (display_width // 2, 0 + textRect.height / 2)

        pygame.display.get_surface().blit(text, textRect)
        pygame.display.update()
        clock.tick(500)

        return snake_position, apple_position, score, moves, count_loop


'''
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN ->button_direction = 2
UP -> button_direction = 3
'''

display_width = 500
display_height = 500
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)

pygame.init()
display=pygame.display.set_mode((display_width,display_height))
clock=pygame.time.Clock()