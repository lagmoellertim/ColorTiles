from math import sqrt, pow, sin, cos
from math import pi as M_PI
M_PI_2 = M_PI * 2

"""
Based on code of:
https://gist.github.com/zeffii/c1e14dd6620ad855d81ec2e89a859719
original c code:
https://raw.githubusercontent.com/warrenm/AHEasing/master/AHEasing/easing.c
Copyright (c) 2011, Auerhaus Development, LLC
http://sam.zoy.org/wtfpl/COPYING for more details.
"""


def QuadraticEaseIn(percentage):
    return percentage * percentage


def QuadraticEaseOut(percentage):
    return -(percentage * (percentage - 2))


def QuadraticEaseInOut(percentage):
    if (percentage < 0.5):
        return 2 * percentage * percentage
    return (-2 * percentage * percentage) + (4 * percentage) - 1


def CubicEaseIn(percentage):
    return percentage * percentage * percentage


def CubicEaseOut(percentage):
    f = (percentage - 1)
    return f * f * f + 1


def CubicEaseInOut(percentage):
    if (percentage < 0.5):
        return 4 * percentage * percentage * percentage
    else:
        f = ((2 * percentage) - 2)
        return 0.5 * f * f * f + 1


def QuarticEaseIn(percentage):
    return percentage * percentage * percentage * percentage


def QuarticEaseOut(percentage):
    f = (percentage - 1)
    return f * f * f * (1 - percentage) + 1


def QuarticEaseInOut(percentage):
    if (percentage < 0.5):
        return 8 * percentage * percentage * percentage * percentage
    else:
        f = (percentage - 1)
        return -8 * f * f * f * f + 1


def QuinticEaseIn(percentage):
    return percentage * percentage * percentage * percentage * percentage


def QuinticEaseOut(percentage):
    f = (percentage - 1)
    return f * f * f * f * f + 1


def QuinticEaseInOut(percentage):
    if (percentage < 0.5):
        return 16 * percentage * percentage * percentage * percentage * percentage
    else:
        f = ((2 * percentage) - 2)
        return 0.5 * f * f * f * f * f + 1


def SineEaseIn(percentage):
    return sin((percentage - 1) * M_PI_2) + 1


def SineEaseOut(percentage):
    return sin(percentage * M_PI_2)


def SineEaseInOut(percentage):
    return 0.5 * (1 - cos(percentage * M_PI))


def CircularEaseIn(percentage):
    return 1 - sqrt(1 - (percentage * percentage))


def CircularEaseOut(percentage):
    return sqrt((2 - percentage) * percentage)


def CircularEaseInOut(percentage):
    if(percentage < 0.5):
        return 0.5 * (1 - sqrt(1 - 4 * (percentage * percentage)))
    else:
        return 0.5 * (sqrt(-((2 * percentage) - 3) * ((2 * percentage) - 1)) + 1)


def ExponentialEaseIn(percentage):
    return percentage if (percentage == 0.0) else pow(2, 10 * (percentage - 1))


def ExponentialEaseOut(percentage):
    return percentage if (percentage == 1.0) else 1 - pow(2, -10 * percentage)


def ExponentialEaseInOut(percentage):
    if(percentage == 0.0 or percentage == 1.0):
        return percentage

    if(percentage < 0.5):
        return 0.5 * pow(2, (20 * percentage) - 10)
    else:
        return -0.5 * pow(2, (-20 * percentage) + 10) + 1


def ElasticEaseIn(percentage):
    return sin(13 * M_PI_2 * percentage) * pow(2, 10 * (percentage - 1))


def ElasticEaseOut(percentage):
    return sin(-13 * M_PI_2 * (percentage + 1)) * pow(2, -10 * percentage) + 1


def ElasticEaseInOut(percentage):
    if (percentage < 0.5):
        return 0.5 * sin(13 * M_PI_2 * (2 * percentage)) * pow(2, 10 * ((2 * percentage) - 1))
    else:
        return 0.5 * (sin(-13 * M_PI_2 * ((2 * percentage - 1) + 1)) * pow(2, -10 * (2 * percentage - 1)) + 2)


def BackEaseIn(percentage):
    return percentage * percentage * percentage - percentage * sin(percentage * M_PI)


def BackEaseOut(percentage):
    f = (1 - percentage)
    return 1 - (f * f * f - f * sin(f * M_PI))


def BackEaseInOut(percentage):
    if (percentage < 0.5):
        f = 2 * percentage
        return 0.5 * (f * f * f - f * sin(f * M_PI))
    else:
        f = (1 - (2*percentage - 1))
        return 0.5 * (1 - (f * f * f - f * sin(f * M_PI))) + 0.5


def BounceEaseIn(percentage):
    return 1 - BounceEaseOut(1 - percentage)


def BounceEaseOut(percentage):
    if(percentage < 4/11.0):
        return (121 * percentage * percentage)/16.0

    elif(percentage < 8/11.0):
        return (363/40.0 * percentage * percentage) - (99/10.0 * percentage) + 17/5.0

    elif(percentage < 9/10.0):
        return (4356/361.0 * percentage * percentage) - (35442/1805.0 * percentage) + 16061/1805.0

    else:
        return (54/5.0 * percentage * percentage) - (513/25.0 * percentage) + 268/25.0


def BounceEaseInOut(percentage):
    if(percentage < 0.5):
        return 0.5 * BounceEaseIn(percentage*2)
    else:
        return 0.5 * BounceEaseOut(percentage * 2 - 1) + 0.5
