# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab
import matplotlib.lines as mlines # for creating legends on plots
# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[(x,y)] = False
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = pos.getX()
        y = pos.getY()
        tile = (int(x), int(y))
        self.tiles[tile] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m, n)]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return self.tiles.values().count(True)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = round(random.random() * self.width, 1)
        y = round(random.random() * self.height, 1)
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        if (0 <= x < self.width) and (0 <= y < self.height):
            return True
        else:
            return False		


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.randrange(360)
        self.position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)		

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError
 
# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_position  = self.position.getNewPosition(self.direction, self.speed)
        # if robot not within the room change direction at random and move to new position in da'house
        while not self.room.isPositionInRoom(new_position):
            self.direction = random.randrange(360)
            new_position  = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(new_position)
        self.room.cleanTileAtPosition(self.position)

		
# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    visualize = False
    total_time_steps = 0.0
    for trial in range(num_trials):
        if visualize:
            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        robotCollection = []
        for i in range(num_robots):
            robotCollection.append(robot_type(room, speed))
        if visualize:
            anim.update(room, robotCollection)
        while (room.getNumCleanedTiles()/float(room.getNumTiles())) < min_coverage:
            for robot in robotCollection:
                robot.updatePositionAndClean()
            total_time_steps += 1
            if visualize:
                anim.update(room, robotCollection)
        if visualize:
            anim.done()
    return total_time_steps / num_trials

# === Problem 4

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    times = []
    num_robots = [1, 10, 20, 50, 100]
    for x in num_robots:
        test = runSimulation(x, 1, 20, 20, 1, 10, StandardRobot)
        times.append(test)
    pylab.figure()
    pylab.title('Dependence of cleaning time on number of robots')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Time / Steps')
    pylab.plot(num_robots, times)
    pylab.show()	

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    times = []
    room_width = [10, 20, 25, 50]
    shapes = []	
    for x in room_width:
        room_height = 300/x
        test = runSimulation(1, 1, x, room_height, 1, 10, StandardRobot)
        times.append(test)
        shapes.append(float(x) / room_height) 
    pylab.figure()
    pylab.title('Dependence of cleaning time on room shape')
    pylab.xlabel('Room shape')
    pylab.ylabel('Time / Steps')
    pylab.plot(shapes, times)
    pylab.show() 

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_position  = self.position.getNewPosition(random.randrange(360), self.speed)
        # if robot not within the room change direction at random and move to new position in da'house
        while not self.room.isPositionInRoom(new_position):
            self.direction = random.randrange(360)
            new_position  = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(new_position)
        self.room.cleanTileAtPosition(self.position)

# print runSimulation(1, 1, 20, 20, 0.8, 10, StandardRobot)
# print runSimulation(1, 1, 20, 20, 0.8, 10, RandomWalkRobot)

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    times_std = []
    times_rnd = []
    num_robots_range  = range(1, 11)
    for x in num_robots_range:
        times_std.append(runSimulation(x, 1, 20, 20, 0.8, 10, StandardRobot))
        times_rnd.append(runSimulation(x, 1, 20, 20, 0.8, 10, RandomWalkRobot))
    pylab.title('Time of cleaning 80% of a 20x20 sq room')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Time / Steps')
    # create legend
    blue_line = mlines.Line2D(num_robots_range, times_std, color='blue', label='StandardRobot')
    orange_line = mlines.Line2D(num_robots_range, times_rnd, color='orange', label='RandomWalkRobot')
    pylab.legend(handles=[blue_line, orange_line])

    pylab.plot(num_robots_range, times_std, color='blue')
    pylab.plot(num_robots_range, times_rnd, color='orange')
    pylab.show()

	
if __name__ == '__main__':
    showPlot1()
    showPlot2()
    showPlot3()

	
	
	
	
	