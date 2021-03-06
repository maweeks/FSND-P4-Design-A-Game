"""models.py - This file contains the class definitions for the Datastore
entities used by the Tictactoe game. Because these classes are also regular
Python classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    @classmethod
    def getUserRating(self, scores):
        count = 0
        points = 0
        wins = 0
        user_name = ""
        userRating = 0.0
        for score in scores:
            if user_name == "":
                user_name = score.user.get().name
            count += 1
            points += score.points
            if score.points >= 3:
                wins += 1

        form = UserRatingForm()
        # average points per game * win percentage
        if count > 0:
            userRating = (1.0 * points * wins / count / count)
        form.user_name = user_name
        form.rating = userRating
        return form


class Game(ndb.Model):
    """Game object"""
    game_state = ndb.StringProperty(required=True, default=".........")
    game_over = ndb.BooleanProperty(required=True, default=False)
    history = ndb.StringProperty(default="")
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, user):
        """Creates and returns a new game"""
        game = Game(user=user,
                    game_state=".........",
                    game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.game_state = self.game_state
        form.game_over = self.game_over
        form.history = self.history
        form.message = message
        return form

    def checkEndGame(self):
        possible_wins = [[0, 1, 2], # top row
                        [3, 4, 5], # middle row
                        [6, 7, 8], # bottom row
                        [0, 3, 6], # left column
                        [1, 4, 7], # middle column
                        [2, 5, 8], # right column
                        [0, 4, 8], # top left to bottom right
                        [2, 4, 6]] # top right to bottom left
        # check for wins
        gs = self.game_state
        remaining = self.game_state.count(".")
        for p_win in possible_wins:
            if ((gs[p_win[0]] == gs[p_win[1]]) and (gs[p_win[0]] == gs[p_win[2]])):
                if gs[p_win[0]] == "x":
                    self.end_game(3 + remaining)
                elif gs[p_win[0]] == "o":
                    self.end_game(0)
        # check for draw
        if (("." not in self.game_state) and (not self.game_over)):
            self.end_game(1)

    def end_game(self, points=0):
        """Ends the game."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), points=points)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    points = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, points=self.points,
            date=str(self.date))


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    game_state = messages.StringField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    history = messages.StringField(6, required=True)


class GameForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    game_state = messages.StringField(2, default=".........")


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    move = messages.IntegerField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    points = messages.IntegerField(3, required=True)


class HighScoresForm(messages.Message):
    """ScoreForm for outbound Score information"""
    number_of_results = messages.IntegerField(1, required=False, default=10)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class UserRatingForm(messages.Message):
    """UserRatingForm for outbound Rating information"""
    user_name = messages.StringField(1, required=True)
    rating = messages.FloatField(2, required=True)


class UserRatingForms(messages.Message):
    """Return multiple UserRatingForms"""
    items = messages.MessageField(UserRatingForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
