"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    game_state = ndb.StringProperty(required=True, default=".........")
    game_over = ndb.BooleanProperty(required=True, default=False)
    points =  ndb.IntegerProperty(required=True, default=0)
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, user):
        """Creates and returns a new game"""
        game = Game(user=user,
                    game_state=".........",
                    game_over=False,
                    points=0)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.game_state = self.game_state
        form.game_over = self.game_over
        form.points = self.points
        form.message = message
        return form

    def checkEndGame(self):
        draw = False
        # check for draw
        if "." not in self.game_state:
            draw = True
        # check for wins
        gs = self.game_state
        if (((gs[0] == gs[1]) and (gs[0] == gs[2])) or
            ((gs[0] == gs[3]) and (gs[0] == gs[6])) or
            ((gs[0] == gs[4]) and (gs[0] == gs[8]))):
            if gs[0] == "x":
                self.end_game(3)
            elif gs[0] == "o":
                self.end_game(0)
        elif (((gs[4] == gs[3]) and (gs[4] == gs[5])) or
            ((gs[4] == gs[2]) and (gs[4] == gs[6])) or
            ((gs[4] == gs[1]) and (gs[4] == gs[7]))):
            if gs[4] == "x":
                self.end_game(3)
            elif gs[4] == "o":
                self.end_game(0)
        elif (((gs[8] == gs[2]) and (gs[8] == gs[5])) or
            ((gs[8] == gs[6]) and (gs[8] == gs[7]))):
            if gs[8] == "x":
                self.end_game(3)
            elif gs[8] == "o":
                self.end_game(0)
        elif draw:
            self.end_game(1)



    def end_game(self, points=0):
        """Ends the game."""
        self.game_over = True
        self.points = points
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
    points = messages.IntegerField(6, required=True)


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


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
