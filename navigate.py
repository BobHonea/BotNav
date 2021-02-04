'''
Navigation theory

navigation activities are:
  scanning : do a live sonar scan from position
  scan-lookup : identify static position based on sonar scan and database
  qualify : scan a "novel" object, add to database as "novel"
  pathing : journey from location A to location B.
  auditing: journey on a predefined pattern, to verify the database.
  signaling: express in light or sound a data pattern that identifies
             the present activity or status.

  idling: remaining in place
  following: pathing towards a "novel" "non-static" shape

  note: non-static "novel" shape

the travel journies are:
    pathing : moving on runtime computed path from position A to B

    pathright : moving in forward in for path_quantum length, then
                moving at angle
the robot must calibrate orientation and position before it can
travel on paths to an objective point.


'''
