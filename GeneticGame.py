from tkinter import *
import math
import cmath
import random
import time

class Mutator:

    def __init__(self):
        self.Percentage = mutation * .01

    def CreateMutation(self, geneticCode):
        self.Percentage = mutation * .01
        MutatedCode = GeneticCode(len(geneticCode.Vertices))
        
        MutatedCode.Color = self.MutateColor(geneticCode.Color)
        MutatedCode.Vertices = self.MutateVertices(geneticCode.Vertices)
        MutatedCode.WeaponVertex = self.MutateWeaponVertex(len(geneticCode.Vertices), geneticCode.WeaponVertex)
        MutatedCode.WeaponAngle = self.MutateProperty(geneticCode.WeaponAngle)
        MutatedCode.RotSpeed = self.MutateProperty(geneticCode.RotSpeed)
        MutatedCode.TransSpeed = self.MutateProperty(geneticCode.TransSpeed)
        MutatedCode.Temperature = self.MutateProperty(geneticCode.Temperature)

        return MutatedCode

    def MutateColor(self, color):
        red = round(255.0/100.0 * self.MutateProperty(100.0/255.0 * color[0]))
        green = round(255.0/100.0 * self.MutateProperty(100.0/255.0 * color[1]))
        blue = round(255.0/100.0 * self.MutateProperty(100.0/255.0 * color[2]))
        if(red < 0):
            red = 0
        if(red > 255):
            red = 255
        if(green < 0):
            green = 0
        if(green > 255):
            green = 255
        if(blue < 0):
            blue = 0
        if(blue > 255):
            blue = 255
        return (red, green, blue)

    def MutateProperty(self, something):
        direction = random.randint(0,1)
        if direction == 0:
            something = something + random.random() * (100-something) * self.Percentage
        else:
            something = something - random.random() * something * self.Percentage
        return something

    def MutateVertices(self, VerticesList):
        MutatedList = []
        for x, y in VerticesList:
            MutatedList.append((self.MutateProperty(x), self.MutateProperty(y)))
        return MutatedList

    def MutateWeaponVertex(self, numVertices, weaponVertex):
        if random.random() < self.Percentage:
            return random.randint(0, numVertices - 1)
        else:
            return weaponVertex

    def MutateManyGenes(self, geneticCode, numGenes):
        allMutations = []
        allMutations.append(geneticCode)
        for i in range(0,numGenes - 1):
            allMutations.append(self.CreateMutation(geneticCode))
        return allMutations
            

class GeneticCode:
    def __init__(self, numVertices):
        self.Vertices = []
        self.Color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        self.WeaponVertex = random.randint(0,numVertices-1)
        self.WeaponAngle = random.random() * 100
        self.RotSpeed = random.random() * 100
        self.TransSpeed = random.random() * 100
        self.Temperature = random.random() * 100

        for i in range(0, numVertices):
            self.Vertices.append((random.random() * 100, random.random() * 100))

    def PrintCode(self):
        print(self.Vertices)
        print(self.WeaponVertex)
        print(self.WeaponAngle)
        print(self.RotSpeed)
        print(self.TransSpeed)
        print(self.Temperature)

    def CreateShip(self):
        totalAngle = 0
        totalArea = 0
        scaledAngles = []
        cumulAngles = [0]
        scaledLengths = []
        poly = []
        wep = []
        
        #Find sum of angles
        for item in self.Vertices:
            totalAngle += item[1]

        #Scale to 2pi
        previousAngle = 0
        for item in self.Vertices:
            currentAngle = item[1] * (2 * math.pi / totalAngle)
            cumulAngles.append(previousAngle + currentAngle)
            scaledAngles.append(currentAngle)
            previousAngle += currentAngle
        
        #Find total area
        for i in range(0, len(self.Vertices)):
            if(scaledAngles[i] < math.pi):
                totalArea += 0.5*self.Vertices[i][0]*self.Vertices[(i+1)%(len(self.Vertices)-1)][0]*math.sin(scaledAngles[i])

        #Scale Areas and Angles
        for (i,item) in enumerate(self.Vertices):
            scaledLengths.append(item[0] * math.sqrt(500/totalArea))
        
        #Make ship polygon
        for i in range(0, len(scaledLengths)):
            poly.append( (scaledLengths[i]*math.sin(cumulAngles[i]), scaledLengths[i]*math.cos(cumulAngles[i])) )
        
        #Make weapon polygon    
        wepVertex = poly[self.WeaponVertex]
        a = self.WeaponAngle * math.pi / 50
        d = math.atan(0.2)
        pt1 = (10*math.cos(a+d) + wepVertex[0], 10*math.sin(a+d) + wepVertex[1]) 
        pt2 = (10*math.cos(a-d) + wepVertex[0], 10*math.sin(a-d) + wepVertex[1]) 
        pt3 = (10*math.cos(a+d+math.pi) + wepVertex[0], 10*math.sin(a+d+math.pi) + wepVertex[1]) 
        pt4 = (10*math.cos(a-d+math.pi) + wepVertex[0], 10*math.sin(a-d+math.pi) + wepVertex[1])
        wep.append(pt1)
        wep.append(pt2)
        wep.append(pt3)
        wep.append(pt4)
        
        #Speeds
        rot = self.RotSpeed * 0.1 #0.02
        trans = self.TransSpeed * 0.1 #0.05
        temp = self.Temperature * 0.01
        
        #Color
        color = '#' + hex(256*256*256 + 256*256*self.Color[0] + 256*self.Color[1] + self.Color[2])[3:]
        
        return Ship( self, poly, wep, rot, trans, temp, color)
        
    def IntToHex(self, colorInt):
        color         

class Ship:
    
    def __init__(self, gene, poly, wep, avgrot, avgvel, temp, color):
        self.alive = True
        self.gene = gene
        self.poly = poly
        self.wep = wep
        self.avgrot = avgrot
        self.avgvel = avgvel
        self.temp = temp
        self.color = color
        self.health = 100
        self.angle = 0.0
        self.rot = avgrot
        self.dir = random.random()*2*math.pi
        self.velocity = [avgvel*math.cos(self.dir), avgvel*math.sin(self.dir)]
        self.center = [0.0, 0.0]
        self.isBouncing = False
        self.randomStart()

    def randomStart(self):
        self.center[0] = random.randrange(20, windowWidth - 20)
        self.center[1] = random.randrange(20, windowHeight - 20)
        pos = complex(self.center[0], self.center[1])
        rot = cmath.rect(1, self.angle*math.pi/180)
        newpoly = []
        for x, y in self.poly:
            v = rot * (complex(x, y)) + pos
            newpoly.append(v.real)
            newpoly.append(v.imag)
        self.realpoly = newpoly
        newwep = []
        for x, y in self.wep:
            v = rot * (complex(x, y)) + pos
            newwep.append(v.real)
            newwep.append(v.imag)
        self.realwep = newwep

    def move(self):
        self.center[0] += self.velocity[0] * (1 + 2*self.temp*(random.random() - 0.5))
        self.center[1] += self.velocity[1] * (1 + 2*self.temp*(random.random() - 0.5))
        self.angle += self.rot * (1 + self.temp*(random.random() - 0.5))

class MyCanvas(Canvas):

    def __init__(this,*args,**kwargs):
        super().__init__(*args,**kwargs)
        this.alltheships = []
        this.lastship = []
        this.bind("<KeyPress>",this.keyWasPressed)
        this.focus_set()

    def isColliding(this, ship):
        for oship in this.alltheships:
            if(ship != oship):
                if(checkCollisionShipShip(ship,oship)):
                   return True
        return False
        
    def moveStuff(this):
        for ship in this.alltheships:
            if(ship.alive):
                ship.move()
                            
                pos = complex(ship.center[0], ship.center[1])
                rot = cmath.rect(1, ship.angle*math.pi/180)
                newpoly = []
                for x, y in ship.poly:
                    v = rot * (complex(x, y)) + pos
                    newpoly.append(v.real)
                    newpoly.append(v.imag)
                if(graphicsOn):
                    this.coords(ship.cpoly, *newpoly)
                ship.realpoly = newpoly
                newwep = []
                for x, y in ship.wep:
                    v = rot * (complex(x, y)) + pos
                    newwep.append(v.real)
                    newwep.append(v.imag)
                if(graphicsOn):
                    this.coords(ship.cwep, *newwep)
                ship.realwep = newwep

                bounced = False
                flip0 = False
                flip1 = False
                for othership in this.alltheships:
                    if(othership.alive):
                        if(ship != othership):
                            if(checkCollisionWepShip(ship,othership)):
                                ship.rot *= -1
                                othership.health -= 20
                            if(checkCollisionShipShip(ship,othership)):
                                flip0 = True
                                flip1 = True
                                bounced = True
                if(outOfLeftRightBounds(ship)):
                    flip0 = True
                    bounced = True
                if(outOfUpDownBounds(ship)):
                    flip1 = True
                    bounced = True
                if(not(ship.isBouncing)):
                    if(flip0):
                        ship.velocity[0] *= -1
                    if(flip1):
                        ship.velocity[1] *= -1
                    if(bounced):
                        ship.isBouncing = True
                else:
                    if(not(bounced)):
                        ship.isBouncing = False
                if(ship.center[0] < 0):
                    ship.velocity[0] = ship.avgvel;
                if(ship.center[0] > windowWidth):
                    ship.velocity[0] = -ship.avgvel;
                if(ship.center[1] < 0):
                    ship.velocity[1] = ship.avgvel;
                if(ship.center[1] > windowHeight):
                    ship.velocity[1] = -ship.avgvel;

        totalships = 0      
        for ship in this.alltheships:
            if(ship.alive):
                this.lastship = ship
                if(ship.health > 0):
                    totalships += 1
                else:
                    ship.alive = False
                    if(graphicsOn):
                        this.delete(ship.cpoly)
                        this.delete(ship.cwep)
        if(totalships == 1):
            for ship in this.alltheships:
                if(ship.alive):
                    this.lastship = ship
        return (totalships > 1)

    def keyWasPressed(this, event=None):
        global delay,delayText,mutation,mutationText,genes,genesText,enableGraphics,graphicsOn,windowWidth,windowHeight,widthLine,heightLine
        key=event.keysym
        if(key=="Up"):
            delay -= 0.01
        if(key=="Down"):
            delay += 0.01
        if(key=="Left"):
            mutation -= 1
        if(key=="Right"):
            mutation += 1
        if(key=="Prior"):
            genes += 1
        if(key=="Next"):
            genes -= 1
        if(key=="Insert"):
            enableGraphics = True
        if(key=="Delete"):
            graphicsOn = False
        if(key=="F9"):
            windowWidth = max(windowWidth-50, 50)
        if(key=="F10"):
            windowWidth = min(windowWidth+50, 800)
        if(key=="F11"):
            windowHeight = max(windowHeight-50, 50)
        if(key=="F12"):
            windowHeight = min(windowHeight+50, 600)
        this.delete(heightLine)
        heightLine = canvas.create_line( (0,windowHeight), (windowWidth,windowHeight))
        this.delete(widthLine)
        widthLine = canvas.create_line( (windowWidth,0), (windowWidth,windowHeight))
        this.delete(delayText)
        delayText = this.create_text( (50,20), text="Delay: " + str(delay))
        this.delete(mutationText)
        mutationText = canvas.create_text( (50,30), text="Mutation: "+str(mutation))
        this.delete(genesText)
        genesText = canvas.create_text( (50,40), text="Genes: "+str(genes))

def checkCollisionWepShip(s,o):
    if(largeDistance(s.center[0],s.center[1],o.center[0],o.center[1])):
        return False
    return checkPolygonCollision(s.realwep, o.realpoly)

def checkCollisionShipShip(s,o):
    if(largeDistance(s.center[0],s.center[1],o.center[0],o.center[1])):
        return False
    return checkPolygonCollision(s.realpoly, o.realpoly)

def largeDistance(x1,y1,x2,y2):
    distsq = abs(x1-x2)*abs(x1-x2)+abs(y1-y2)*abs(y1-y2)
    return (distsq > 10000)

def checkPolygonCollision(p, q):
    plen = int(len(p)/2)
    qlen = int(len(q)/2)
    for i in range(0,plen):
        j = 0
        if(i < plen-1):
            j = i+1
        for k in range(0,qlen):
            l = 0
            if(k < qlen-1):
                l = k+1
            if(lineCollide(p[2*i], p[2*i+1], p[2*j], p[2*j+1], q[2*k], q[2*k+1], q[2*l], q[2*l+1])):
                return True
    return False

def lineCollide(x1,y1,x2,y2,x3,y3,x4,y4):
    try:
        ua = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/((y4-y3)*(x2-x1)-(x4-x3)*(y2-y1))
        x = x1 + ua*(x2-x1)
        y = y1 + ua*(y2-y1)
        if between(x,x1,x2) and between(x,x3,x4) and between(y,y1,y2) and between(y,y3,y4):
            return True
        else:
            return False
    except:
        return False

def between(n,first,second):
    return (first<=n<=second or first>=n>=second)

def outOfLeftRightBounds(ship):
    for i in range(0,len(ship.realpoly),2):
        if(ship.realpoly[i] < 0 or ship.realpoly[i] > windowWidth):
            return True
    for i in range(0,len(ship.realwep),2):
        if(ship.realwep[i] < 0 or ship.realwep[i] > windowWidth):
            return True
    return False
    
def outOfUpDownBounds(ship):
    for i in range(1,len(ship.realpoly),2):
        if(ship.realpoly[i] < 0 or ship.realpoly[i] > windowHeight):
            return True
    for i in range(1,len(ship.realwep),2):
        if(ship.realwep[i] < 0 or ship.realwep[i] > windowHeight):
            return True
    return False

class Logger():
    def __init__(this):
        this.frames = []
    def addFrame(this, alltheships):
        shipSteps = []
        for ship in alltheships:
            if(ship.alive):
                shipSteps.append( (ship.center[0], ship.center[1], ship.angle) )
        this.frames.append(shipSteps)
##################
# MAINNNNN #######
##################

root = Tk()

windowWidth = 800
windowHeight = 600

delay = 0.01
mutation = 20
genes = 20
enableGraphics = True
graphicsOn = True

canvas = MyCanvas( root, width=windowWidth+100, height=windowHeight )
canvas.pack()

logger = Logger()
mutator = Mutator()

beststreak = 0
streak = 1
bestEnabled = False
bestship = []
bestpoly = canvas.create_line( (0,0), (1,0) )
bestwep = canvas.create_line( (1,0), (2,0) )

currentGene = GeneticCode(5)

generation = 0
while(True):
    generation += 1
    if(enableGraphics):
        graphicsOn = True
        enableGraphics = False
    widthLine = canvas.create_line( (windowWidth,0), (windowWidth,windowHeight))
    heightLine = canvas.create_line( (0,windowHeight), (windowWidth,windowHeight))
    canvas.create_text( (50,10), text="Generation: "+str(generation))
    canvas.create_text( (windowWidth+50,20), text="Streak: "+str(beststreak))
    delayText = canvas.create_text( (50,20), text="Delay: "+str(delay))
    mutationText = canvas.create_text( (50,30), text="Mutation: "+str(mutation))
    genesText = canvas.create_text( (50,40), text="Genes: "+str(genes))
    if(bestEnabled):
        pnew = []
        for x,y in bestship.poly:
            pnew.append(windowWidth+50+x)
            pnew.append(50+y)
        wnew = []
        for x,y in bestship.wep:
            wnew.append(windowWidth+50+x)
            wnew.append(50+y)
        bestpoly = canvas.create_polygon(pnew, fill=bestship.color)
        bestwep = canvas.create_polygon(wnew)
    allGenes = mutator.MutateManyGenes(currentGene, genes)
    for gene in allGenes:
        canvas.alltheships.append(gene.CreateShip())
    for ship in canvas.alltheships:
        while(canvas.isColliding(ship)):
            ship.randomStart()
        if(graphicsOn):
            ship.cpoly = canvas.create_polygon(ship.poly, fill=ship.color)
            ship.cwep = canvas.create_polygon(ship.wep)
    x=0
    cont = True
    while(cont):
        x=x+1
        cont = canvas.moveStuff()
        #logger.addFrame(canvas.alltheships)
        root.update()
        if(delay > 0):
            time.sleep(delay)
    if(currentGene == canvas.lastship.gene):
        streak += 1
        if(streak > beststreak):
            beststreak = streak
            if(not(bestship == canvas.lastship)):
                bestship = canvas.lastship
                if(bestEnabled):
                    canvas.delete(bestpoly)
                    canvas.delete(bestwep)
                else:
                    bestEnabled = True
                pnew = []
                for x,y in bestship.poly:
                    pnew.append(windowWidth+50+x)
                    pnew.append(50+y)
                wnew = []
                for x,y in bestship.wep:
                    wnew.append(windowWidth+50+x)
                    wnew.append(50+y)
                bestpoly = canvas.create_polygon(pnew, fill=bestship.color)
                bestwep = canvas.create_polygon(wnew)
    else:
        streak = 1
        
    currentGene = canvas.lastship.gene
    canvas.alltheships = []
    canvas.delete(ALL)
