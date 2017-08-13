# TagTrain Bot

A reddit bot for dealing with the fact that reddit only allows you to mention 3 users per post.  Any more than that
and NOBODY won't get the notification about being mentioned.

## How does it work

1. Redditor creates a Group and adds redditors as Members `u/TagTrain add internetmallcop to reddit-mods`
1. Owner adds as many others as they want `u/TagTrain add kethryvis to reddit-mods`
1. etc `u/TagTrain add Chtorrr to reddit-mods`
1. etc `u/TagTrain add toasties to reddit-mods`
1. etc `u/TagTrain add br0000d to reddit-mods`
1. etc `u/TagTrain add MyNameIzKhan to reddit-mods`
1. etc `u/TagTrain add bigapplered to reddit-mods`
1. And then, should they need to mention all those users at once, `u/TagTrain use reddit-mods` and the bot will create, in this case, 3 Messages.

## Why?

A redditor on `r/TheAdventureZone/` was posting write ups of their "Retrospective Relistens" to all the past episodes.
People wanted to be mentioned so they didn't miss a bit.  Unfortunately, the "tag train" become a little unweildy for a
person to manage manually.  I thought the idea was neat and offered up solution.


## Priority TODO
- [ ] Handle sending important messages to owner (i.e. me)
- [ ] Convert `use` command from "username pings" to direct messages since Reddit has temporarily suspended the bot for "username ping spam"

## TODO
- [ ] Finish tests
