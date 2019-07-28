from util.vec import Vec3

def draw_debug(player, renderer, car, target, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the target
    renderer.draw_line_3d(car.physics.location, target, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())

    # experiment: draw lines along goal
    renderer.draw_line_3d(player.opposing_goal.location, Vec3(player.opposing_goal.location) + Vec3(800, 0, 0), renderer.white())
    renderer.draw_line_3d(player.opposing_goal.location, Vec3(player.opposing_goal.location) + Vec3(-800, 0, 0), renderer.white())


    renderer.end_rendering()