#Full Stack Nanodegree Project 4

##Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
2.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
3.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.

##Suggested API usage to play a game:
1. Create user
2. Creage new game for that user
3. Make moves until the game is finished.

##Game Description:
Tictactoe is a simple one player game played against the AI. Each game begins
with an empty 3 x 3 grid. players then take it in turns (user and AI) to place
either an 'x' or an 'o'. The winner is the player that gets three of their token
in a row. If no more moves can be made and there is no winner then the game is
considered a draw.
Many different Tic tac toe games can be played by many different Users at any
given time. Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

Games are scored as (3 + x) points for a win, 1 point for a draw and 0 points
for a loss, where x is the number of moves left when the game ends.

User rating is their win percentage multiplied by their average score.

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will
    raise a ConflictException if a User with that user_name already exists.

 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, game_state (optional)
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not.

 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, move
    - Returns: GameForm with new game state.
    - Description: Accepts a 'move' and returns the updated state of the game.
    Within this step the AIs turn will also be taken if the game isn't complete.
    If this causes a game to end, a corresponding Score entity will be created.

 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).

 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms.
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_user_games**
    - Path: 'games/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms.
    - Description: Returns all active Games recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_average_attempts**
    - Path: 'games/average_attempts'
    - Method: GET
    - Parameters: None
    - Returns: Message confirming action.
    - Description: Gets teh cached average moves remaining.

 - **cancel_game**
    - Path: 'games/{urlsafe_game_key}/cancel'
    - Method: DELETE
    - Parameters: urlsafe_game_key
    - Returns: Message confirming action taken.
    - Description: Deletes the specified game if it is active.
    Will not delete finished games.

 - **get_high_scores**
    - Path: 'high_scores'
    - Method: GET
    - Parameters: number_of_results (optional)
    - Returns: ScoreForms.
    - Description: Returns a list of high scores. Maximum size of results
    can be limited.

 - **get_user_rankings**
    - Path: 'user_rankings'
    - Method: GET
    - Parameters: None
    - Returns: UserRatingForms.
    - Description: Returns user ratings of all users.

 - **get_game_history**
    - Path: 'game/{urlsafe_game_key}/history'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: Message.
    - Description: Returns a message containing the game history.

##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.

 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.

 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.

##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, game_state, game_over,
    message, user_name, history).
 - **GameForms**
    - Multiple GameForm container.
 - **NewGameForm**
    - Used to create a new game (user_name, game_state)
 - **MakeMoveForm**
    - Inbound make move form (move).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, points).
 - **HighScoresForm**
    - Representation of a highscores request (number_of_results).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **UserRatingForm**
    - Representation of a user's Rating (user_name, rating).
 - **UserRatingForms**
    - Multiple UserRatingForm container.
 - **StringMessage**
    - General purpose String container.