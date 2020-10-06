"""
A BARD DAY'S NIGHT
a.k.a. BARD ROCK CAFE
a.k.a. A GOOD MAN IS BARD TO FIND
a.k.a. THE SCHOOL OF BARD KNOCKS
a.k.a. A BARD RAIN'S A-GONNA FALL
"""

# Imports

from __future__ import annotations  # Non-string-escaped annotations
from typing import Optional, Set, List, Dict, TextIO  # Specific annotations

# Constants

# Minimum number of songs for a villager to be promoted to a bard
BARD_THRESHOLD = 10

# Number of songs for the billboard_top statistic
BILLBOARD_N = 10


class Villager:
    """
    A named inhabitant of the village. Knows songs. Can be a bard,
    in which case they know every song.

    Attributes:
        name: a string representing the Villager's name
        is_bard: True iff the Villager is a bard, otherwise False
        songs: a set of the Songs the Villager knows
    """

    name: str
    is_bard: bool
    songs: Set[Song]

    def __init__(self: Villager, name: str, is_bard: bool) -> None:
        """Initialize a villager who begins knowing no songs."""

        self.name = name
        self.is_bard = is_bard
        self.songs = set()

    def __repr__(self: Villager) -> str:
        """Return a string representing this Villager by its name."""

        return self.name

    def __hash__(self: Villager) -> int:
        """Return a hash for this Villager using its name."""
        return hash(self.name)


class Song:
    """
    A titled song that maintains a record of who has sung it.

    Attributes:
        title: a string representing the song's title
        known_by: a set of Villagers who know the song
    """

    title: str
    known_by: Set[Villager]

    def __init__(self: Song, title: str) -> None:
        """Initialize a song not yet sung by anybody."""

        self.title = title
        self.known_by = set()

    def __repr__(self: Song) -> str:
        """Return a string representing this Song by its title."""

        return self.title

    def __hash__(self: Song) -> int:
        """Return a hash for this Song using its title."""
        return hash(self.title)


class Village:
    """
    A collection of villagers who hold parties where they sing songs.

    Attributes:
        villagers: a set of Villagers
        songs: a set of Songs
        parties: a list of Parties

    Representation invariants:
        Every villager in a party is in <villagers>
    """

    villagers: Set[Villager]
    songs: Set[Song]
    parties: List[Party]

    def __init__(self: Village) -> None:
        """Initialize a village without villagers, songs, or parties."""

        self.villagers = set()
        self.songs = set()
        self.parties = []

    # Input

    def read_input(self: Village, file: TextIO) -> None:
        """
        Read the given file and populate the villagers, songs, and parties.

        file is an open file containing VILLAGERS, SONGS, and PARTIES,
        in that order, with those headings. One villager per line;
        one song per line; one party per line, consisting of attendees
        separated by commas. The parties are given in the order they're held.
        """

        t = file.readlines()      # read the files line by line
        lst = []
        for element in t:
            lst.append(element.strip())     # remove /n

        lst_of_villagers = lst[1:lst.index('SONGS') - 1]
        lst_of_songs = lst[lst.index('SONGS') + 1: lst.index("PARTIES") - 1]
        lst_of_parties = lst[lst.index("PARTIES") + 1:]

        for v in lst_of_villagers:
            if "*" in v:
                v = v[:len(v) - 1]
                new = Villager(v, True)
            else:
                new = Villager(v, False)
            self.villagers.add(new)

        for s in lst_of_songs:
            new = Song(s)
            for b in self.villagers:
                if b.is_bard is True:
                    new.known_by.add(b)
            self.songs.add(new)

        for p in lst_of_parties:
            new = p.split(",")
            new_party = Party()
            for new_villager in new:
                for v in self.villagers:
                    if v.name == new_villager:
                        new_villager = v
                new_party.attendees.add(new_villager)
            self.parties.append(new_party)

    # Stats

    def unheard_songs(self: Village) -> Set[Song]:
        """
        Return a set of songs that have never been heard by non-bards.
        (This means that only the bards know it.)
        """

        unheard_songs = set()
        bards = set()

        for villager in self.villagers:
            if villager.is_bard is True:
                bards.add(villager)

        for s in self.songs:
            if s.known_by == bards:
                unheard_songs.add(s)

        return unheard_songs

    def billboard_top(self: Village) -> List[Song]:
        """
        Return a list of the BILLBOARD_N most popular songs by number of people
        who know them, in descending order. Break ties alphabetically.
        """

        d = {}
        for s in self.songs:
            d[s] = len(s.known_by)

        return sorted(d, key=d.get, reverse=True)[:BILLBOARD_N]

    def bards(self: Village) -> Set[Villager]:
        """Return the set of the village's bards."""

        bards = set()
        for villager in self.villagers:
            if villager.is_bard is True:
                bards.add(villager)

        return bards

    def average_attendees(self: Village) -> int:
        """
        Return the average number of attendees at parties in the village.
        Round up to the nearest integer.
        """

        num_of_attendees = 0
        for party in self.parties:
            num_of_attendees = num_of_attendees + len(party.attendees)

        return round(num_of_attendees / len(self.parties))


class Party:
    """
    A record of attendees and procedures for singing and updating bards.

    Attributes:
        attendees: a Set of the Villagers attending this party
    """

    attendees: Set[Villager]

    def __init__(self: Party) -> None:
        """Initialize a party with no attendees."""

        self.attendees = set()

    def sing(self: Party) -> None:
        """A bard sings if present, otherwise the villagers sing."""
        #
        # d_set
        # for v in self.attendees:
        #     d_set = d_set.symmetric_difference(v.songs)
        #
        # list(d_set)
        #
        # for song in d_set:
        #     if song.title > song_to_sing.title:
        #         song_to_sing = item
        #
        # for v in self.attendees:
        #     v.songs.add(song_to_sing)
        #     song_to_sing.known_by.add(v)

    def update_bards(self: Party) -> None:
        """
        Promote attendees who have learned enough songs to bards,
        iff there is another bard present at the party.
        """

        state = 0
        for v in self.attendees:
            if v.is_bard is True:
                state = 1

        for v in self.attendees:
            if state == 1:
                if len(v.songs) >= BARD_THRESHOLD:
                    v.is_bard = True


# Main process

def run(filename: str) -> Dict[str, object]:
    """
    Run the program: Create a village, read the input, host the parties,
    and return a dictionary of resulting statistics keyed by name:
    {unheard_songs, billboard_top, bards, average_attendees}

    filename is the name of an input file.
    """
    new_village = Village()
    new_village.read_input(filename)

    return {'unheard_songs': new_village.unheard_songs,
            'billboard_top': new_village.billboard_top,
            'bards': new_village.bards,
            'average_attendees': new_village.average_attendees}


if __name__ == '__main__':

    # import python_ta
    # python_ta.check_all(
    #     config={
    #         'allowed-io':
    #             ['Village.read_input', 'run'],
    #
    #         'extra-imports':  # allowed imports that shouldn't cause a warning
    #             ['typing', 'math']})
    #
    # # Sample input from the handout -- you can tweak this if you like
    # stats_short = run('handout_example.txt')
    # print('Results of handout sample input')
    # for key, value in stats_short.items():
    #     print(f'{key}: {value}')
    #
    # print()
    #
    # # Sample bigger input -- you can tweak this if you like
    # stats_long = run('bigger_example.txt')
    # print('Results of bigger sample input')
    # for key, value in stats_long.items():
    #     print(f'{key}: {value}')

    # villagers = ["Luke Sawczak", "Dan Zingaro*", "Sadia Rain Sharmin",
    #             "Arnold Rosenbloom"]
    #
    # b = set()
    #
    # for v in villagers:
    #     if "*" in v:
    #         v = v[:len(v) - 1]
    #         new = Villager(v, True)
    #     else:
    #         new = Villager(v, False)
    #     b.add(new)
    #
    # unheard_songs = set()
    # bards = set()
    #
    # for villager in self.villagers:
    #     if villager.is_bard is True:
    #         bards.add(villager)
    #
    # for s in self.songs:
    #     if s.known_by == bards:
    #         unheard_songs.add(s)
    #
    # print(unheard_songs)



