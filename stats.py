import pygame


class stats(object):
    gold = 100
    castlehealth = 100
    miliseconds = 0
    lastmiliseconds = 0
    wave = 1
    timetowave = 5
    seconds = 0
    minutes = 0
    totalseconds = 0
    shitminutes = []
    # I don't know a better way of doing this but since python does not refresh fast enough
    # every milisecond I had to make a totalseconds, then I reset seconds if no remainder from 60.
    # The list is to see if it has already added it for that minute since it's not using decimals

    def gettime():
        change = int(stats.miliseconds / 1000) - stats.totalseconds
        stats.totalseconds += change
        stats.seconds += change
        if stats.timetowave != 0:
            stats.timetowave -= change
        if stats.totalseconds % 60 == 0 and stats.totalseconds >= 1 and stats.totalseconds not in stats.shitminutes:
            stats.shitminutes.append(stats.totalseconds)
            stats.minutes += 1
            stats.seconds = 0
        return str(stats.timetowave)


