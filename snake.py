import curses
from random import randint

def main(stdscr):
    # changing settings is terminal
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(150)

    HEADER = " Welcome to SNAKE!! "
    KEYS_OPPOSITE_DIRECTION = {curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP, curses.KEY_RIGHT: curses.KEY_LEFT, curses.KEY_LEFT: curses.KEY_RIGHT}
    key = curses.KEY_RIGHT    
    score = 0
    

    # getting the size of the terminal
    sh, sw = stdscr.getmaxyx()
    
    # creating boundary for the game
    stdscr.border()

    # create snake and set initial direction
    snake = [[5,9], [5,8], [5,7]]
    food = [sh//2, sw//2]

    # print header, score and food
    stdscr.addstr(0, sw//2 - len(HEADER)//2, HEADER)
    stdscr.addstr(0, 2, " Score: {} ".format(score))
    stdscr.addstr(food[0], food[1], 'O')

    while 1:
        # get input from user
        event = stdscr.getch()

        # check if the user entered any of the arrow keys, if yes then assign it to key
        if event in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP] and event != KEYS_OPPOSITE_DIRECTION[key]:
            key = event

        # get the next position based on the key
        if key == curses.KEY_RIGHT:
            snake.insert(0, [snake[0][0], snake[0][1]+1])
        elif key == curses.KEY_LEFT:
            snake.insert(0, [snake[0][0], snake[0][1]-1])
        elif key == curses.KEY_DOWN:
            snake.insert(0, [snake[0][0]+1, snake[0][1]])
        elif key == curses.KEY_UP:
            snake.insert(0, [snake[0][0]-1, snake[0][1]])

        # insert and print new head
        stdscr.addstr(snake[0][0], snake[0][1], '#')

        # check if snake is on food
        if snake[0] == food:
            # update the score
            score += 1
            stdscr.addstr(0, 2, " Score: {} ".format(score))

            # create new location for food and check it should not any of the snake's positions
            food = None
            while food is None:
                food = [randint(1, sh-2), randint(1, sw-2)]
                if food in snake:
                    food = None
            stdscr.addstr(food[0], food[1], 'O')

            # make the snake faster as it eats more
            stdscr.timeout(150 - (len(snake)//2) % 120)
        else:
            # remove the tail of the snake
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # conditions for game over
        if snake[0][0] in [0, sh-1] or snake[0][1] in [0, sw-1] or snake[0] in snake[1:]:
            msg_1 = "Game Over!"
            stdscr.addstr(sh//2, sw//2-len(msg_1)//2, msg_1)
            stdscr.nodelay(0)
            stdscr.getch()
            break

curses.wrapper(main)