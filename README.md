# COMP2001-REPORT
this repo contains my python code for the application of my COMP2001 REPORT, the changes for the schema CW2 are already in the database under ALEXANDER GOSLIN and all of the API is included in the word
document however i will add them here for clarities sake.
POST /trails – allows users to create a new trail by sending a JSON payload with information
GET /trails – retrieves a list of all trails in the database
PUT /trails/(TrailID) – updates the information of an existing trails specified by TrailID
DELETE /trails/(TrailID) – deleted a trail based on its TrailID
POST /trails/(TrailID)/waypoints – adds a new waypoint to trail with ID TrailID
GET /trails/(TrailID)/waypoints – gets a list of all waypoints to trail with ID TrailID
PUT /waypoints/(TrailID) – updates information to waypoint with ID WaypointID
DELETE /waypoints/(TrailID) -  deletes a waypoint with ID WaypointID
GET /trail_logs – retrieves all the logs
