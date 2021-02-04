'''
Detection theory

Detection is by means of SONAR.
The profile is computed as a reflected energy function of angle 0
for sensor location (room, room_x, room_y)

Simplifying design rules:
The profile function is computed with real numbers, and stored
as an integer function.

The profile function is limited to 63 angular sectors.

The profile values for an angular sector are positive integers
in the range [0,N), where N is (2**n)-1. n is integer and n <=8

Profile reflection values are:
    0 = no reflection
    N-1 = maximum (saturating) reflection energy


Navigation time convolutions of of live-sonar-scan against the
shape library, or sonar-scan-database use integer math,
since early robots floating point libraries will be slow,
and consume lots of power.


'''
