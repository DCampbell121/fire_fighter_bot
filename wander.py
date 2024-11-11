from pybricks.pupdevices import Motor,ColorSensor,UltrasonicSensor
from pybricks.parameters import Port,Direction,Color
from pybricks.robotics import DriveBase
from fire_fighter import goal_found
#from main_bot import colors
import umath

def wander(drive_base=DriveBase,c_sensor=ColorSensor,s_ultra=UltrasonicSensor,f_ultra=UltrasonicSensor, fan_motor=Motor):
    #wander until find wall
    drive_base.drive()
    goal = False
    while not goal:
        f_distance = f_ultra.distance
        if f_distance < 1000:
            drive_base.drive(turn_rate=f_distance)
        if c_sensor.color(surface=True) == Color.GREEN:
            goal = True
            break
    
    goal_found(fan_motor)

def wall_follow(drive_base=DriveBase,c_sensor=ColorSensor,s_ultra=UltrasonicSensor,f_ultra=UltrasonicSensor, fan_motor=Motor):
    #follow a wall on the robots left side
    drive_base.drive()
    goal = False
    next_to_wall = True
    
    #drive forward 250mm, if goal is found then end, if wall no longer there then wander
    #else get new distance to wall and try to calculate the angle to straighten along
    while not goal and next_to_wall:
        left_wall_dist = s_ultra.distance
        drive_base.straight(distance=250) #only goes in 250mm stretches, can increase
        new_wall_dist = s_ultra.distance
        if c_sensor.color(surface=True) == Color.GREEN:
            goal = True
        elif new_wall_dist > 100: #wall no longer found
            next_to_wall = False
        else:
            #adjust angle to try to drive parallel to the wall
            dist_difference = new_wall_dist - left_wall_dist
            adjust_angle = umath.atan(dist_difference / 250) #debated on acos here?
            drive_base.turn(adjust_angle)
        
    if goal:
        goal_found(fan_motor)
    else:
        wander(drive_base, c_sensor, s_ultra, f_ultra, fan_motor)