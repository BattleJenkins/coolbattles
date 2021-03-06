"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def at_object_creation(self):
        "This is called when object is first created, only."
        for stat in ('ATM', 'DEF', 'VIT', 'ATR', 'MOB', 'SPE'):
            self.attributes.add(stat, 6)
        self.db.HP = 18
        self.db.SP = 12
        self.db.Special_Moves = {}
        self.db.Range_Messages = []
        self.db.Melee_Messages = []
        self.db.Allies = []
        self.db.shortdesc = "A fighter!"
    def at_before_move(self, destination):
        if self.db.Combat_TurnHandler:
            self.caller.msg("You can't exit a room while in combat!")
            return False
        if self.db.HP <= 0:
            self.caller.msg("You can't move, you've been defeated! Type 'return' to go back to the Institute and recover!")
            return False
        return True
    def at_after_move(self, source_location):
        """
        We make sure to look around after a move.

        """
        if self.location.access(self, "view"):
            self.msg(text=((self.at_look(self.location),), {"window":"room"}))
            self.msg("%s arrives at %s." % (self, self.location))
    pass

