# coding=utf-8


"""
This file is divided into 3 segments:

1. Sample output of the pyspecs framework when executing this module.
2. Production code for a bowling game score card (the system under test).
3. The test code that relies on and is run by the pyspecs framework to verify
   that the Production Code is correct.

########### 1. Sample Output ###########


# run_pyspecs.py

-------------------------------------- 1 --------------------------------------

  | • given a game with all gutter balls
  |   • when the score is calculated
  |     • then the score should be zero


  | • given a game with all ones
  |   • when the score is calculated
  |     • then the score should be twenty


  | • given a game with one spare
  |   • when the score is calculated
  |     • then the score should include the next roll as bonus


  | • given a game with one strike
  |   • when the score is calculated
  |     • then the score should include the next frame as a bonus


  | • given a perfect game
  |   • when the score is calculated
  |     • then the score should equal 300


15 steps, 5 scenarios in 0.0002 seconds

ok

"""

########## Production Code ###########


ALL_PINS = 10
FULL_GAME_IN_FRAMES = 10


class BowlingGame(object):
    def __init__(self):
        self._rolls = []

    def roll(self, pins):
        self._rolls.append(pins)

    def score(self):
        total = 0
        roll = 0
        for frame in range(FULL_GAME_IN_FRAMES):
            if self._is_strike(frame):
                total += self._strike_bonus(frame)
                roll += 1
            elif self._is_spare(frame):
                total += self._spare_bonus(frame)
                roll += 2
            else:
                total += self._current_frame(roll)
                roll += 2

        return total

    def _is_strike(self, frame):
        return self._rolls[frame] == ALL_PINS

    def _is_spare(self, frame):
        return self._current_frame(frame) == ALL_PINS

    def _strike_bonus(self, frame):
        return ALL_PINS + self._rolls[frame + 1] + self._rolls[frame + 2]

    def _spare_bonus(self, frame):
        return ALL_PINS + self._rolls[frame + 2]

    def _current_frame(self, roll):
        return self._rolls[roll] + self._rolls[roll + 1]


############## Test Code ###############


def roll_game(rolls):
    game = BowlingGame()

    for pins in rolls:
        game.roll(pins)

    return game


from pyspecs import given, when, then, the, finish


with given.a_game_with_all_gutter_balls:
    game = roll_game([0] * 20)

    with when.the_score_is_calculated:
        score = game.score()

        with then.the_score_should_be_zero:
            the(score).should.equal(0)


with given.a_game_with_all_ones:
    game = roll_game([1] * 20)

    with when.the_score_is_calculated:
        score = game.score()

        with then.the_score_should_be_twenty:
            the(score).should.equal(20)


with given.a_game_with_one_spare:
    game = roll_game([4, 6, 3] + [0] * 17)

    with when.the_score_is_calculated:
        score = game.score()

        with then.the_score_should_include_the_next_roll_as_bonus:
            the(score).should.equal(4 + 6 + 3 + 3)  # 17


with given.a_game_with_one_strike:
    game = roll_game([10, 3, 4] + [0] * 16)

    with when.the_score_is_calculated:
        score = game.score()

        with then.the_score_should_include_the_next_frame_as_a_bonus:
            the(score).should.equal(10 + 3 + 4 + 3 + 4)  # 24


with given.a_perfect_game:
    game = roll_game([10] * 12)

    with when.the_score_is_calculated:
        score = game.score()

        with then.the_score_should_equal_300:
            the(score).should.equal(300)


if __name__ == '__main__':
    finish()