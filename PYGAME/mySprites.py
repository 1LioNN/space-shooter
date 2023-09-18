'''
Author: Lion Su
Date: 24/05/2019
Description: Sprites for the main game
'''
import pygame 
import random
class Space(pygame.sprite.Sprite):
    '''Our Space background class inherits from the Sprite class'''
    def __init__(self, screen):
        '''Initializer to set the image, position, and direction.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define a space image
        self.image = pygame.image.load("images/background.png")

          
        # Define the position and direction of the background
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width() / 2
        self.rect.bottom = screen.get_height()
        self.dy = 8
    

    def update(self):
        '''Scrolls the background down 2/3 then resets'''
        self.rect.bottom += self.dy
        if self.rect.centery >= 1230:
            self.rect.bottom = self.window.get_height()
class Player(pygame.sprite.Sprite):
    '''Our Player class inherits from the Sprite class'''
    def __init__(self, screen):
        '''Initializer to set the image, position, and direction'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define a plane image
        self.image = pygame.image.load("images/player.png")
        # Define a mask for our player for better collison
        self.mask = pygame.mask.from_surface(self.image)
        # Define the position, and bullet levels/damage
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width() / 2
        self.rect.centery = screen.get_height() - 150
        #Define direction, damage, hit indicator, and bullet level
        self.dy = 0
        self.dx = 0
        self.damage = 50
        self.hit = 1
        self.bulletLvl = 1

    def moveUp(self):
        '''This mutator method changes the planes y direction to 11'''
        self.dy = 11
        
    def moveLeft(self):
        '''This mutator method changes the planes x direction to -11'''
        self.dx = -11
    
    def moveDown(self):
        '''This mutator method changes the planes y direction to -11'''
        self.dy = -11
    
    def moveRight(self):
        '''This mutator method changes the planes x direction to 11'''
        self.dx = 11
    
    def stopMoving(self):
        '''This mutator method stops the planes movement'''
        self.dx = 0
        self.dy = 0
        
    def returnDmg(self):
        '''This accessor method returns the planes bullet damage'''
        return self.damage
    
    def bulletLvlUp(self):
        '''This mutator method levels up the plane bullets and increases damage by 50, and reduces damage by 50 for lvl 4 bullets
        for balancing reasons'''
        
        self.bulletLvl += 1
        if self.bulletLvl == 4:
            self.damage -=50
        else:
            self.damage+= 50        
        
    def getBulletLvl(self):
        '''This accessor method returns the bullet level'''
        return self.bulletLvl 
    def playerHit(self):
        '''This mutator method sets player hit indicator to 1'''
        self.hit = 1

    def update(self):
        '''Automatically called in the Refresh section to update our Plane Sprite's position.'''
        self.image = pygame.image.load("images/player.png")
        #If plane is hit change image
        if self.hit:  
            self.image = pygame.image.load("images/playeroof.png")
            self.hit = 0  
        #If plane hits top or bottom of screen then prevent it from going further
        if ((self.rect.top > 0) and (self.dy > 0)) or\
           ((self.rect.bottom < self.window.get_height()) and (self.dy < 0)):
            self.rect.top -= self.dy
        #If plane hits left or right of screen then prevent it from going further
        if ((self.rect.left > 0) and (self.dx < 0)) or\
            ((self.rect.right< self.window.get_width()) and (self.dx > 0)):
            self.rect.left += self.dx
      
            
class EnemyPlane1(pygame.sprite.Sprite):
    '''Our enemy plane class inherits from the Sprite class'''
    def __init__(self, screen):
        '''Initializer to set the image, position, and direction.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define an enemy plane image
        self.image = pygame.image.load("images/enemy1.png")
          
        # Define the position of our enemy using it's rect, randomly generated
        self.rect = self.image.get_rect()
        self.rect.bottom = -75
        self.rect.centerx = random.randint(25, 535)
        self.dy = random.randint(10,12)
        self.dx = random.randint(-4,4)

        
    def reset(self):
        '''This mutator method resets all of the plane's instance variables'''
        self.rect.bottom = -75
        self.rect.centerx= random.randint(25,self.window.get_width()-25)
        self.dy = random.randint(10,12)
        self.dx = random.randint(-4,4) 
        
    def update(self):
        '''Automatically called in the Refresh section to update plane's position.'''
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        #If it updates 20 times, have 33% chance to change x direction
        if self.rect.bottom == (self.dy * 20) - 75 and not random.randint(0,2):
            self.dx = -self.dx
        #If it flies past the bottom then call the reset method
        if ((self.rect.top > self.window.get_height()) and (self.dy > 0)):
            self.reset()
        #If it flies past the left or right of the screen then call the reset method
        if ((self.rect.right < 0) and (self.dx < 0)) or\
            ((self.rect.left> self.window.get_width()) and (self.dx > 0)):
            self.reset()
class EnemyPlane2(pygame.sprite.Sprite):
    '''Our Big Planbe class inherits from the Sprite class'''
    def __init__(self, screen,planeNum):
        '''Initializer to set the image, position, and direction, accepts an extra parameter for plane number.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define a plane image
        self.image = pygame.image.load("images/enemy2.png")
        #Hit indicator
        self.hit = 0
        self.rect = self.image.get_rect()
        #Create mask for better collision
        self.mask = pygame.mask.from_surface(self.image)
        # Define the position depending the the plane number
        self.planeNum = planeNum
        if planeNum == 1:
            self.rect.centerx = 140
            self.dx = -1
        elif planeNum ==2:
            self.rect.centerx = screen.get_width() - 140
            self.dx = 1
        #Define direction and health
        self.dy = 5
        self.rect.bottom = -1500
        self.health = 750
    def loseHealth(self,bulletDmg):
        '''This mutator method sets the hit indicator to 1 and makes the plane lose health depending on bullet damage'''
        self.health -= bulletDmg
        self.hit = 1
    def getHealth(self):
        '''This accessor method returns the current health of the plane'''
        return self.health
    def reset(self):
        '''This mutator method resets all of the plane's instance variables'''
        self.rect.bottom = -1500
        self.health = 500
        if self.planeNum == 1:
            self.rect.centerx = 140
        elif self.planeNum ==2:
            self.rect.centerx = self.window.get_width() - 140
        self.dy = 5
            
    def update(self):
        '''Automatically called in the Refresh section to update our plane's position.'''
        self.rect.centery += self.dy 
        #Resets image after being hit
        self.image = pygame.image.load("images/enemy2.png")
        #If the center of the plane reaches 201 pixels then change y direction to 0, and start moving left to right
        if self.rect.centery > 250:
            self.dy = 0
            self.rect.centerx += self.dx
        #If plane is hit change image
        if self.hit:
            self.image = pygame.image.load("images/enemy2oof.png")
            self.hit = 0
        #Reset if health goes 0 or lower
        if self.health <= 0:
            self.reset()
        #Prevent planes from going through eachother and going off screen depending on plane number
        if self.planeNum ==1:
            if ((self.rect.left < 0) and (self.dx < 0)) or\
               ((self.rect.right> self.window.get_width()/2) and (self.dx > 0)):
                self.dx = -self.dx 
        if self.planeNum ==2:
            if ((self.rect.left < 280) and (self.dx < 0)) or\
                ((self.rect.right> self.window.get_width()) and (self.dx > 0)):
                self.dx = -self.dx             
class PlayerBullets(pygame.sprite.Sprite):
    '''Our bullet class inherits from the Sprite class'''
    def __init__(self,screen,playerX,playerTop,bulletLvl,dx,number):
        '''Initializer to set the image, position, and direction for player bullets, accepts player x and player top rect and bullet level as parameters, also
        accepts x direction value and bullet number for lvl 4 bullets'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define a bullet image depending on level of the bullet
        if bulletLvl < 4:
            self.image = pygame.image.load("images/bullet"+str(bulletLvl)+".png")
        elif bulletLvl == 4:
            self.image = pygame.image.load("images/bullet4"+str(number)+".png")
        
        # Define the position of our Bullet using it's rect, set start position to the top center of the plane
        self.rect = self.image.get_rect()
        self.rect.centerx = playerX
        self.rect.centery = playerTop
        self.dy = -30
        self.dx = dx

 
    def update(self):
        '''Automatically called in the Refresh section to update our Bullet Sprite's position.'''
        self.rect.bottom += self.dy
        self.rect.centerx += self.dx
        #If bullets goes out of screen then kill it
        if self.rect.bottom < 0:
            self.kill()
class EnemyBullets(pygame.sprite.Sprite):
    '''Our enemy bullets class inherits from the Sprite class'''
    def __init__(self,screen,dx,dy,enemyX,enemyBottom):
        '''Initializer to set the image, position, and direction, accepts x direction, y direction, enemy x position, and enemy bottom position as parameters.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define a round bullet for our Sprite
        self.image = pygame.image.load("images/enemybullet.png")
    
        # Define the position of our bullet depending on x and y direction and enemy bottom center position
        self.rect = self.image.get_rect()
        self.rect.centerx = enemyX
        self.rect.bottom = enemyBottom
        self.dy = dy
        self.dx = dx
    

    def update(self):
        '''Automatically called in the Refresh section to update our Bullet Sprite's position.'''
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        #If bullet flies out of screen then kill it
        if ((self.rect.top > self.window.get_height()) and (self.dy > 0)):
            self.kill()
        if ((self.rect.right < 0) and (self.dx < 0)) or\
            ((self.rect.left> self.window.get_width()) and (self.dx > 0)):
            self.kill()
class PowerUp(pygame.sprite.Sprite):
    '''Our power up class inherits from the Sprite class'''
    def __init__(self, screen,powerType):
        '''Initializer to set the image, position, and direction, accepts type of power up (in int) as parameter'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen                   
        #Define image depending on Power type
        self.powType = powerType
        if powerType == 1:
            self.image = pygame.image.load("images/pow1.png")
        elif powerType ==2:
            self.image = pygame.image.load("images/pow2.png")
        #Define position and direction of power up randomly
        self.rect = self.image.get_rect()
        self.rect.bottom = -75             
        self.rect.centerx = random.randint(25, 535)
        self.dx = 0
        self.dy = 0
    def appear(self):
        '''This mutator method causes the sprite to move toward the screen'''
        self.dy = random.randint(3,7)
        self.dx = random.randint(-7,7)
    def reset(self):
        '''This mutator method resets the sprite's instance variables'''
        self.rect.bottom = -75
        self.rect.centerx = random.randint(25, 535)
        self.dy = 0
        self.dx = 0       
            
    def update(self):
        '''Automatically called in the Refresh section to update our power up Sprite's position.'''
        self.rect.centery += self.dy 
        self.rect.centerx += self.dx
        #If sprite hits left or right wall then reverse x direction
        if ((self.rect.left > 0) and (self.dx < 0)) or\
           ((self.rect.right < self.window.get_width()) and (self.dx > 0)):
            self.rect.left += self.dx
        else:
            self.dx = -self.dx
        #If the goes off screen reset position
        if self.rect.top > self.window.get_height():
            self.reset()
             
class Explosion(pygame.sprite.Sprite):
    '''Our Explosion class inherits from the Sprite class'''
    def __init__(self, screen,planeCenter):
        '''Initializer to set the image, and position for an explosion Sprite. Also accepts center rect of a plane sprite as a parameter'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
        # Keep track of the image frame
        self.counter = 0
        # Create list for each frame
        self.explosionList = []
        #Add image frames to list
        for i in range (23):
            self.explosionList.append(pygame.image.load("images/Explosion"+str(i)+".gif"))

        # Define the position of our explosion using center of plane
        self.image = self.explosionList[self.counter]
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center= planeCenter
        

    def update(self):
        '''Automatically called in the Refresh section to update explosion frames'''
        self.counter +=1
        #Animate the explosion, if the last frame is finished, kill the sprite
        if self.counter <= len(self.explosionList) - 1:
            self.image = self.explosionList[self.counter]
        else:
            self.kill()
class BossBody(pygame.sprite.Sprite):
    '''Our Boss Body class inherits from the Sprite class'''
    def __init__(self, screen):
        '''Initializer to set the image, position, and direction'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define a frame count
        self.frameNum = 0
        # Create List for frames 
        self.frameList =[]
        # Define hit indicator
        self.hit = 0
        # Append each frame to list
        for i in range (4):
            self.frameList.append(pygame.image.load("images/bossBody"+str(i)+".png"))
        #Set first frame and create mask for better collision
        self.image = self.frameList[self.frameNum]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
          
        # Define the position using it's rect=
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width()/2
        self.dy = 5
        self.rect.bottom = -19300
        # Define health of boss
        self.health = 30000
    def loseHealth(self,bulletDmg):
        '''This mutator method causes the boss to take damage depening on bullet damage and sets hit indicator to 1'''
        self.health -= bulletDmg
        self.hit = 1
    def getHealth(self):
        '''This accessor method returns the remaining health of the boss' body'''
        return self.health
    def update(self):
        '''Automatically called in the Refresh section to update our Boss Sprite's position.'''
        self.rect.centery += self.dy 
        # Change to next frame, if reached last frame, reset frame count
        self.frameNum +=1
        if self.frameNum<= len(self.frameList) - 1:
            self.image = self.frameList[self.frameNum]
        else:
            self.frameNum = 0        
        #If center of boss reaches 165 then change y direction to 0
        if self.rect.centery > 165:
            self.dy = 0
        #Change image if hit
        if self.hit:
            self.image = pygame.image.load("images/bossBodyoof.png")
            self.hit = 0
        #If health is 0 or less, kill the sprite
        if self.health <= 0:
            self.kill()
class BossWings(pygame.sprite.Sprite):
    '''Our Boss Wing class inherits from the Sprite class'''
    def __init__(self, screen,wingNum):
        '''Initializer to set the image, position, and direction, accepts wing number as a parameter'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define an image based on wing number
        self.image = pygame.image.load("images/bosswing"+str(wingNum)+".png")
        # Define a hit indicator
        self.hit = 0
        #Define the wingnum as an instance variable
        self.wingNum = wingNum
        # Define the position depending on wing num, and create mask for better collision
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if wingNum == 1:
            self.rect.centerx = 100 
        elif wingNum == 2:
            self.rect.centerx = 459
        self.dy = 5
        self.rect.bottom = -19300
        #Set the health of the wing
        self.health = 15000
    def loseHealth(self,bulletDmg):
        '''This mutator method causes the boss to take damage depening on bullet damage and sets hit indicator to 1'''
        self.health -= bulletDmg
        self.hit = 1
    def getHealth(self):
        '''This accessor method returns the remaining health of the wing'''
        return self.health
    def update(self):
        '''Automatically called in the Refresh section to update our Boss Wing Sprite's position.'''
        self.rect.centery += self.dy 
        #Resets wing image if not hit
        self.image = pygame.image.load("images/bossWing"+str(self.wingNum)+".png")
        #If wing center goes past 167 then change y direction to 0
        if self.rect.centery > 167:
            self.dy = 0
        #If plane is hit change image
        if self.hit:
            self.image = pygame.image.load("images/bossWing"+str(self.wingNum)+"oof.png")
            self.hit = 0
        #If plane has less than or equal to 0 health then kill it
        if self.health <= 0:
            self.kill()
class BossMinions(pygame.sprite.Sprite):
    '''Our Boss Minion class inherits from the Sprite class'''
    def __init__(self, screen,minionNum):
        '''Initializer to set the image, position, and direction, accepts Minion number as a parameter'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Keep track of the screen
        self.window = screen
         
        # Define an image based on wing number
        self.image = pygame.image.load("images/bossMinion.png")
        # Define a hit indicator
        self.hit = 0
        #Define the wingnum as an instance variable
        self.minionNum = minionNum
        # Define the position depending on wing num, and create mask for better collision
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = screen.get_width()/2
        self.dx = 0
        self.dy = 5
        self.rect.bottom = -19400
        #Set the health of the wing
        self.health = 7500
        
    def loseHealth(self,bulletDmg):
        '''This mutator method causes the boss to take damage depening on bullet damage and sets hit indicator to 1'''
        self.health -= bulletDmg
        self.hit = 1
    def getHealth(self):
        '''This accessor method returns the remaining health of the minion'''
        return self.health
    
    def moveOut(self):
        '''This mutator method changes the x direction of the minion'''
        if self.minionNum == 1:
            self.dx = -5
        elif self.minionNum ==2:
            self.dx = 5
        if self.rect.right < 159 or self.rect.left > 402:
            self.dx = 0
    def update(self):
        '''Automatically called in the Refresh section to update our Minion Sprite's position.'''
        self.rect.centery += self.dy 
        self.rect.centerx += self.dx
        #Resets wing image if not hit
        self.image = pygame.image.load("images/bossMinion.png")
        #If wing center goes past 167 then change y direction to 0
        if self.rect.centery > 220:
            self.dy = 0
        #If plane is hit change image
        if self.hit:
            self.image = pygame.image.load("images/bossMinionoof.png")
            self.hit = 0
        #If plane has less than or equal to 0 health then kill it
        if self.health <= 0:
            self.kill()

class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self,screen,tabNum):
        '''This initializer loads the font "trench", and
        sets the starting score to 0 and lives to 3'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Load our custom font, and initialize the starting score.
        self.font = pygame.font.Font("fonts/trench.ttf", 40)
        self.playerScore = 0
        self.playerLives = 3
        self.playerHighScore = 0
        self.tabNum = tabNum
    def planeKilled(self,value):
        '''This method adds points to the score depending on the value of the plane killed'''
        self.playerScore += value
    def getLives(self):
        '''This accessor method returns the number of player Lives'''
        return self.playerLives
    def playerGainLife(self):
        '''This mutator method increases the life count by 1'''
        self.playerLives +=1
    def playerLoseLife(self):
        '''This mutator method causes the player to lose 1 life'''
        self.playerLives -=1
    def getScore(self):
        '''This accessor method returns the player's current score'''
        return self.playerScore
    def setHighScore(self,score):
        ''' This mutator method accepts a score value and changes the high score'''
        self.playerHighScore = score

    
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        #If tab is 1 (Tutorial) display highscore, if tab is 2 (ingame) display player score and lives
        if self.tabNum == 1:
            message = ("High Score: " +str(self.playerHighScore))
            self.image = self.font.render(message, 1, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (280, 15)        
        elif self.tabNum == 2:
            message = ("Score: "+ str(self.playerScore)+"    Lives: "+str(self.playerLives))
            self.image = self.font.render(message, 1, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (280, 15)