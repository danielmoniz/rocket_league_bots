from src.util.vec import Vec3

def draw_debug(player, renderer, car, target, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the target
    renderer.draw_line_3d(car.physics.location, target, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())

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