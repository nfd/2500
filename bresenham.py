""" Line-drawing routine """

def bresenham(sx, sy, ex, ey):
	points = []

	rise = ey - sy
	run = ex - sx

	risemag = 1 if rise > 0 else -1
	runmag = 1 if run > 0 else -1

	if abs(run) > abs(rise):
		# The longer direction is vertical, so iterate over Y
		for x in range(0, run, runmag):
			y = (x * rise) / run
			points.append( (x + sx, y + sy) )
	else:
		# The longer direction is horizontal, so iterate over X
		for y in range(0, rise, risemag):
			x = (y * run) / rise
			points.append( (x + sx, y + sy) )

	points.append( (ex, ey) )

	return points

DEMO_WIDTH = 20
DEMO_HEIGHT = 20

def demo(segments):
	display = []
	for y in range(DEMO_HEIGHT):
		display.append(['.'] * DEMO_WIDTH)
	
	for sx, sy, ex, ey in segments:
		for x, y in bresenham(sx, sy, ex, ey):
			display[y][x] = 'X'

	for line in display:
		print ''.join(line)

if __name__ == '__main__':
	demo( [(10, 10, 0, 0), (10, 10, 19, 19), (10, 10, 0, 19), (10, 10, 19, 0)] )

