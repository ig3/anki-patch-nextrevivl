# This Anki add-on fixes a couple of faults in calculation of next interval
# for review cards.
#
# If hardFactor > 1 then the minimum next interval for EASY is two days
# more than the current interval. Thus intervals tend to go 1, 3, 5, 7
# days, etc.
#
# If hardFactor < 1 then the minimum next interval for EASY is 2 and if the
# card factor is low (minimum is 1.3) the interval does not increase
# from 2: int(2 * 1.3) = 2, so, if one keeps clicking EASY, interval is
# stuck at 2 days.
#
# This monkey-patches _nextRevIvl so that clicking EASY always increases
# the interval by at least 1 day.
#
#

from anki.schedv2 import Scheduler as SchedulerV2
from anki.cards import Card

def myNextRevIvl(self, card: Card, ease: int, fuzz: bool) -> int:
    "Next review interval for CARD, given EASE."
    delay = self._daysLate(card)
    conf = self._revConf(card)
    fct = card.factor / 1000
    hardFactor = conf.get("hardFactor", 1.2)
    if hardFactor > 1:
        hardMin = card.ivl
    else:
        hardMin = 0
    ivl2 = self._constrainedIvl(card.ivl * hardFactor, conf, hardMin, fuzz)
    if ease == 2:
        # print("hard: ", card.ivl, " > ", ivl2)
        return ivl2

    ivl3 = self._constrainedIvl(
        (card.ivl + delay // 2) * fct,
        conf,
        card.ivl,
        fuzz
    )
    if ease == 3:
        # print("good: ", card.ivl, " > ", ivl3)
        return ivl3

    ivl4 = self._constrainedIvl(
        (card.ivl + delay) * fct * conf["ease4"],
        conf,
        card.ivl,
        fuzz
    )
    # print("easy: ", card.ivl, " > ", ivl4)
    return ivl4

origNextRevIvl = SchedulerV2._nextRevIvl
SchedulerV2._nextRevIvl = myNextRevIvl
