import stats
import constants as c
import enemies

wave1 = [enemies.barbarian1, enemies.barbarian1]
wave2 = [enemies.barbarian1, enemies.barbarian2]
wave3 = [enemies.barbarian2, enemies.barbarian2]
wave4 = [enemies.barbarian2, enemies.barbarian3]
wave5 = [enemies.barbarian3, enemies.barbarian3]
wave6 = [enemies.barbarian3, enemies.barbarian4]
wave7 = [enemies.barbarian4, enemies.barbarian4]
wave8 = [enemies.barbarian8, enemies.barbarian4]
wave9 = [enemies.barbarian9, enemies.barbarian4]
wave10 = [enemies.barbarian10, enemies.barbarian4]
wave11 = [enemies.barbarian11, enemies.barbarian4]
wave12 = [enemies.barbarian12, enemies.barbarian4]
wave13 = [enemies.barbarian13, enemies.barbarian4]
wave14 = [enemies.barbarian14, enemies.barbarian4]
wave15 = [enemies.barbarian15, enemies.barbarian4]

allwaves = [wave1, wave2, wave3, wave4, wave5, wave6, wave7, wave8, wave9, wave10, wave11, wave12, wave13,
            wave14, wave15]

for wave in allwaves:
    for i in range(14):
        wave.append(wave[0])
    for i in range(9):
        wave.append(wave[1])

print (str(wave1))

class Wave(object):
    isgoing = False
    isspawning = False
    tospawn = None
    lastspawntime = -1 # Buffer the enemies
    spawncountdown = 0
    def __init__(self, enemies):
        enemies.self = enemies


def wavelistener():
    if Wave.isgoing:
        enemies.zenemies.update()
        enemies.zenemies.draw(c.gameDisplay)

    if len(enemies.zenemies) == 0 and Wave.isgoing and not Wave.isspawning: # Check for wave over
        print("Wave over!")
        stats.stats.timetowave = 10
        Wave.isgoing = False
        stats.stats.wave += 1

    if Wave.tospawn == []:
        if c.debugspawn:
            print ("Resetting list")
        Wave.tospawn = None
        Wave.isspawning = False

    if Wave.tospawn != None:
        spawnenemies()
    else:
        Wave.isspawning = False

    if stats.stats.timetowave == 0 and not Wave.isspawning and not Wave.isgoing:
        startwave()
        Wave.isspawning = True

def getwave():
    number = stats.stats.wave
    thewave = allwaves[number - 1]
    return thewave


def startwave():
    Wave.isgoing = True
    Wave.tospawn = list(getwave())
    #enemies.spawnenemies()
    spawnenemies()


def spawnenemies():
    if Wave.tospawn != None:
        if stats.stats.miliseconds - Wave.lastspawntime > 500:
            if c.debugspawn:
                print ("Can spawn!")
            Wave.spawncountdown = 0
            Wave.lastspawntime = stats.stats.miliseconds

        for enemy in Wave.tospawn:
            if Wave.spawncountdown == 0 and Wave.lastspawntime != stats.stats.totalseconds:
              #  print (wave.Wave.spawncountdown, wave.Wave.lastspawntime, stats.stats.totalseconds)
                if c.debugspawn:
                    print("Spawning " + str(enemy))
                enemies.zenemies.add(enemy())
                Wave.tospawn.remove(enemy)
                if c.debugspawn:
                    print("Not spawned: " + str(Wave.tospawn))
                Wave.spawncountdown = 1

