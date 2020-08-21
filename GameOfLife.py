# fnagua project, 08/21/2020

"""
r 			: reset
spacebar 	: pause/play
+/-			: clock rate
right click : kill cell
left click	: revive cell
right arrow	: go to next state
"""
import pygame
import numpy as np
import time

def cleanScreen():
    screen.fill(bg)

def draw(state):

	cleanScreen()
	newState = np.zeros((nxCells, nyCells))

	for x in range(0, len(state)):
		for y in range(0, len(state[0])):
			poly = [( x     * dimCW, y     * dimCH ),
                        ( (x+1) * dimCW, y     * dimCH ),
                        ( (x+1) * dimCW, (y+1) * dimCH ),
                        ( x     * dimCW, (y+1) * dimCH )]

			# Draw the grid
			if state[x,y] == 0:
				pygame.draw.polygon(screen, GREY, poly, 1)
			else:
				pygame.draw.polygon(screen, WHITE, poly, 0)
				pygame.draw.polygon(screen, GREY, poly, 1)


	pygame.display.flip()

	# Update state
	return np.copy(newState)

def drawAndUpdate(state):

	cleanScreen()
	newState = np.zeros((nxCells, nyCells))

	for x in range(0, len(state)):
		for y in range(0, len(state[0])):
			poly = [( x     * dimCW, y     * dimCH ),
                        ( (x+1) * dimCW, y     * dimCH ),
                        ( (x+1) * dimCW, (y+1) * dimCH ),
                        ( x     * dimCW, (y+1) * dimCH )]

			# Draw the grid
			if state[x,y] == 0:
				pygame.draw.polygon(screen, GREY, poly, 1)
			else:
				pygame.draw.polygon(screen, WHITE, poly, 0)
				pygame.draw.polygon(screen, GREY, poly, 1)
	
			# Calculating neighbours
			n_neighbours = state[(x-1) % nxCells, (y-1) % nyCells] + \
							state[(x-1) % nxCells,   y   % nyCells] + \
							state[(x-1) % nxCells, (y+1) % nyCells] + \
							state[  x   % nxCells, (y-1) % nyCells] + \
							state[  x   % nxCells, (y+1) % nyCells] + \
							state[(x+1) % nxCells, (y-1) % nyCells] + \
							state[(x+1) % nxCells,   y   % nyCells] + \
							state[(x+1) % nxCells, (y+1) % nyCells]
			
			### RULES ###
			# 1. Any live cell with two or three live neighbours survives.
			if state[x,y] == 1 and (n_neighbours == 2 or n_neighbours == 3):
				newState[x,y] = 1

			# 2. Any dead cell with three live neighbours becomes a live cell.
			elif state[x,y] == 0 and n_neighbours == 3:
				newState[x,y] = 1
			
			# 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

			### END RULES ###


	pygame.display.flip()

	# Update state
	return np.copy(newState)

def wait():
	wait = input(" ")
  
# Screen resolution
height, width = 1000, 1000
res = height, width
  
# Opens up a window 
screen = pygame.display.set_mode(res) 

# Clock rate
cr = 0.01

# Colours
WHITE = 255,255,255
BLACK = 0, 0, 0
GREY  = 128, 128, 128

# Background colour
bg = BLACK
screen.fill(bg)

# Number of cells
nxCells, nyCells = 50, 50

# Dimension of each cell
dimCW = (width-1)  / nxCells
dimCH = (height-1) / nyCells

# Matrix init
state = np.zeros((nxCells, nyCells))
newState = np.copy(state)

# Pause/Play
pause = True

# Drawing initial state
draw(state)

# Exec
while True:

    # Events
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            quit()

        # Pause/Play
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pause = not pause
        
        # Right Arrows
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            newState = state
            state = drawAndUpdate(state)
            newState = drawAndUpdate(state)

        # Reset
        if pygame.key.get_pressed()[pygame.K_r]:
            newState = state
            state = np.zeros((nxCells, nyCells))
            draw(state)
            pause = True

        # Clock
        if pygame.key.get_pressed()[pygame.K_PLUS]:
            cr += 0.05
        if pygame.key.get_pressed()[pygame.K_MINUS]:
            cr -= 0.05
            if cr <= 0:
                cr = 0.01

        if pause:
            # Mouse
            mouseClick = pygame.mouse.get_pressed()
            if sum(mouseClick) > 0:
                newState = state
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                state[celX, celY] = mouseClick[0]
                draw(state)

    if not pause: 

        state = newState

        newState = drawAndUpdate(state)

        time.sleep(cr)