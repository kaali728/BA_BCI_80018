import mouse


def move(action):
    print("move mouse " + action)
    if mouse.is_pressed("right"):
        exit()
    if action == 'push' or action == "smile":
        mouse.move(0, -100, absolute=False, duration=0.2)
    elif action == 'right' or action == "winkR":
        mouse.move(100, 0, absolute=False, duration=0.2)
    elif action == 'left' or action == "winkL":
        mouse.move(-100, 0, absolute=False, duration=0.2)
    elif action == 'pull'or action == "blink":
        mouse.move(0, 100, absolute=False, duration=0.2)