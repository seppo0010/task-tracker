# Task Tracker

Simple CLI task tracker to handle task dependencies and start/end dates.

## Example

```
$ python index.py sample.csv available
Write a task tracker

$ python index.py sample.csv deadlines
Have dinner (until 2017-01-17)
  Cook (since 2017-01-17)
    Buy ingredients (since 2017-01-14)

  Invite people to have dinner (2017-01-10 to 2017-01-14)

  Write a task tracker
```
