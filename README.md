# anki-patch-nextrevivl

Fix/improve the calculation of next review interval in the V2 scheduler,
for Good and Easy cards.

## Installation

* Download patch-nextrevivl.ankiaddon
* Start Anki and open Tools -> Add-ons
* Drag the downloaded .ankiaddon file onto the add-ons list
* Restart Anki

## Changes

This add-on monkey patches _nextRevIvl in the V2 scheduler to change the
'current interval' parameter to _constrainedIvl to be the current interval,
for both Good and Easy. By default, for Good it is the new Hard interval
and for Easy it is the new Good interval.

With this change, the next interval for a review card is at least 1 day
longer than the current interval for all cases except Hard with Hard
Interval less than 1, in which case the minimum interval is 1 day. This
changes the interval for Good and Easy but the interval for Hard is
unchanged.

This fixes a fault with Good when Hard Interval is 1 or more, in which case
the new interval was at least 2 days greater than the current interval. At
larger intervals the difference is insignificant, but at shorter intervals
with a low card factor, this leads to intervals increasing in steps of two
days, which is quite noticable in the stats graph of intervals, and may be
too much for a just learned card.

This fixes a fault with Good when Hard Interval is less than 1, with a low
card factor and low current interval, in which case the interval becomes
stuck at 2 days. With the default scheduler, the only way out of this is to
select Easy until the interval and card factor increase sufficiently that
the next interval for Good is more than 1 day longer than the current
interval.

## Motivation

By default, Hard Interval is greater than 1 and the interval for Good
increases by at least 2 days. At short intervals (e.g. 1 or 2 days) the
increase really should be only 1 day. My memory is poor and the jump from 1
day (for a just learned card) to 3 days was too much.

More significant and the immediate motivation for me making this add-on is
when I changed Hard Interval to 90% so that the interval would gradually
decrease for persistently Hard cards. With this change, I ended up
accumulating cards at interval of 2 days. With interval 2 days, the new
interval for Good was also 2 days - no progress. The only way to progress
was Easy.

These problems arise because in the default scheduler, the minimum new
interval for Good is one day more than the new interval for Hard (i.e. the
new interval for Hard is calculated and this + 1 day is the minimum new
interval for Good. The minimum new interval for Hard is 1 day more than the
current interval if Hard Interval is set to 1 or more. If Hard Interval is
less than 1, then the minimum interval for Hard is 1 day. In this latter
case, the minimum interval for Good is 2 days and with a low card factor
(minimum is 130%) Good will not increase the interval from 2 days to 3
days, so it remains stuck at 2 days.

For me, this allows me to have Hard Interval a little less than 1 (I like
about 90%, so that I see cards that are persistently Hard at progressively
shorter intervals, rather than longer intervals). For decks with Hard
Interval greater than 1 (e.g. default configuration), then the increments
in interval are, initially, a little more gradual.

Alternatives to this are: set Hard Interval to 1 or more and configure
learning steps out to several days, so that increments of review intervals
of 2 days are reasonable; Set Hard Interval less than 1 and use the Easy
button to increase the interval when it is low.
