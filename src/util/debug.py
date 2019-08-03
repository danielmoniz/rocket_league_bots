import math

from src.util.vec import Vec3
from src import pathing

def draw_debug(player, renderer, car, action_display, planned_curve=None):
    car_location = player.game_info['car_location']
    ball_location = player.game_info['ball_location']
    car_direction = player.game_info['car_direction']
    renderer.begin_rendering()

    # print the action that the bot is taking
    renderer.draw_string_3d(car_location, 2, 2, action_display, renderer.white())

    # output the intended curve of the bot
    if planned_curve is not None:
        segments = get_segments(planned_curve)
        final_vector = segments[-1]
        previous_distance = (car_location - final_vector).length()
        previous_vector = car_location
        for vector in segments:
            colour = renderer.white()
            new_distance = (vector - final_vector).length()
            if new_distance > previous_distance:
                colour = renderer.red()
            renderer.draw_line_3d(previous_vector, vector, colour)
            previous_vector = vector
            previous_distance = new_distance

    # draw line vertically from car's various points
    car_length = 125
    car_width = 60
    line_length = 20
    renderer.draw_line_3d(car_location, car_location + Vec3(0, 0, line_length), renderer.white())
    front_of_car = car_location + 75 * car_direction
    renderer.draw_line_3d(front_of_car, front_of_car + Vec3(0, 0, line_length), renderer.white())
    back_of_car = car_location - 50 * car_direction
    renderer.draw_line_3d(back_of_car, back_of_car + Vec3(0, 0, line_length), renderer.white())

    left = Vec3(-car_direction.y * math.sin(-math.pi/2), car_direction.x * math.sin(-math.pi/2))
    left_of_car = car_location + (car_width / 2) * left
    renderer.draw_line_3d(left_of_car, left_of_car + Vec3(0, 0, line_length), renderer.white())
    right_of_car = car_location - (car_width / 2) * left
    renderer.draw_line_3d(right_of_car, right_of_car + Vec3(0, 0, line_length), renderer.white())

    # draw line vertically from ball
    renderer.draw_line_3d(ball_location, ball_location + Vec3(0, 0, line_length), renderer.white())

    # @TEST: draw line out of the right side of the car
    car_right = player.game_info['car_orientation'].right
    renderer.draw_line_3d(car_location, car_location + car_right * line_length, renderer.blue())

    # experiment: draw lines along goal -------------------------
    # Horizontal line along center of goal:
    middle_left = Vec3(player.opposing_goal.location) + Vec3(-player.goal_width / 2, 0, 0)
    middle_right = middle_left + Vec3(player.goal_width, 0, 0)

    # Vertical line along left of goal:
    bottom_left = middle_left + Vec3(0, 0, -player.goal_height / 2)
    top_left = middle_left + Vec3(0, 0, player.goal_height / 2)

    # Vertical line along right of goal:
    top_right = top_left + Vec3(player.goal_width, 0, 0)
    bottom_right = bottom_left + Vec3(player.goal_width, 0, 0)

    renderer.draw_line_3d(middle_left, middle_right, renderer.white())
    renderer.draw_line_3d(bottom_left, top_left, renderer.white())
    renderer.draw_line_3d(bottom_right, top_right, renderer.white())

    renderer.end_rendering()


def get_segments(curve):
    segments = []
    num_items = 100
    for i in range(num_items + 1):
        fraction = i / num_items
        coord = curve.evaluate(fraction).tolist()
        vector = convert_coordinate_to_vector(coord)
        segments.append(vector)
    return segments


def convert_coordinate_to_vector(coord):
    return Vec3(
        coord[0][0],
        coord[1][0],
        max(coord[2][0], 25),
    )