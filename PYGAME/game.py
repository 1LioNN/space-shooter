'''
Author: Lion Su
Date: 24/05/2019
Description: A bullet hell game made by yours truly. The player must shoot down enemy
planes while trying to dodge enemy projectiles in order to beat the final boss which has 
3 phases
'''

# I - Import and Initialize
import pygame
import mySprites
import random
pygame.init()
pygame.mixer.init()

def tutorial():
    # D - Display configuration
    screen = pygame.display.set_mode((560, 820))
    pygame.display.set_caption("Tutorial")
    # E - Entities
    #Create background
    background = pygame.image.load("images/backgroundTutorial.png")
    background = background.convert()
    screen.blit(background,(0,0))
    #Create player, player bullets, and scorekeeper
    player = mySprites.Player(screen)
    playerBullets = pygame.sprite.Group()
    scorekeeper = mySprites.ScoreKeeper(screen,1)
    #Update sprites
    playerBulletGroup = pygame.sprite.OrderedUpdates(playerBullets)
    allSprites = pygame.sprite.OrderedUpdates(player,playerBullets,scorekeeper)
    #Music 
    pygame.mixer.music.load("sound/dogsong.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    #Display High Score
    highScores = open('highScores.txt','r')
    score = highScores.readline()
    highScores.close()
    scorekeeper.setHighScore(score)
        
     
    # A - Action 
     
        # A - Assign values to key variables
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    keepGoing = True
    quitGame = False
     
        # L - Loop
    while keepGoing:
     
        # T - Timer to set frame rate
        clock.tick(30)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #If the 'X' button is pressed then completely quit the game
                keepGoing = False
                quitGame = True
            elif event.type == pygame.KEYUP:
                player.stopMoving()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                        playerBullet = mySprites.PlayerBullets(screen,player.rect.centerx,player.rect.top,player.getBulletLvl(),0,0)
                        playerBullets.add(playerBullet)
                        allSprites.add(playerBullets)
                if event.key == pygame.K_p:
                    #Press P to exit tutorial and play the game
                    keepGoing = False
        #Check keystates for smooth movement, supports for wasd and arrow keys
        keyStates = pygame.key.get_pressed()
        #WASD Movement
        if keyStates[pygame.K_w]:
            player.moveUp()           
        if keyStates[pygame.K_a]:
            player.moveLeft()
        if keyStates[pygame.K_s]:
            player.moveDown()          
        if keyStates[pygame.K_d]:
            player.moveRight()    
        #Arrow keys movement
        if keyStates[pygame.K_UP]:
            player.moveUp()           
        if keyStates[pygame.K_LEFT]:
            player.moveLeft()
        if keyStates[pygame.K_DOWN]:
            player.moveDown()          
        if keyStates[pygame.K_RIGHT]:
            player.moveRight()
     
        # R - Refresh display
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)      
        pygame.display.flip()
    return quitGame
     
def game():
    '''This function defines the 'mainline logic' for our game.'''
    # Display
    screen = pygame.display.set_mode((560, 820))
    pygame.display.set_caption("Space Shooter")
     
    # Entities   
    #Create Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    space = mySprites.Space(screen)
    screen.blit(background, (0,0))
    #Create Player and player bullets
    player = mySprites.Player(screen)
    playerBullets = pygame.sprite.Group()
    #Create enemies and enemy bullets
    enemyBullets = pygame.sprite.Group()
    enemy1 = mySprites.EnemyPlane1(screen)
    enemy2 = mySprites.EnemyPlane1(screen)
    enemy3 = mySprites.EnemyPlane1(screen)
    enemyBig1 = mySprites.EnemyPlane2(screen,1)
    enemyBig2 = mySprites.EnemyPlane2(screen,2)
    bossBody = mySprites.BossBody(screen)
    bossWing1 = mySprites.BossWings(screen,1)
    bossWing2 = mySprites.BossWings(screen,2)
    bossMinion1 = mySprites.BossMinions(screen,1)
    bossMinion2 = mySprites.BossMinions(screen,2)
    #Create Power Ups
    powerUp1 = mySprites.PowerUp(screen,1)
    powerUp2 = mySprites.PowerUp(screen,2) 
    #Create ScoreKeeper and explosions
    scorekeeper = mySprites.ScoreKeeper(screen,2)
    explosionGroup = pygame.sprite.Group()   
    enemyGroup = pygame.sprite.Group()    
    #Creating sprite groups for updating and collision
    enemyGroup = pygame.sprite.OrderedUpdates(enemy1, enemy2, enemy3, enemyBig1, enemyBig2, bossMinion1, bossMinion2,bossBody, bossWing1, bossWing2)
    playerBulletGroup = pygame.sprite.OrderedUpdates(playerBullets)
    allSprites = pygame.sprite.OrderedUpdates(space,player,playerBullets,enemyBullets,enemyGroup,explosionGroup,powerUp1,powerUp2,scorekeeper)
    #Gameover image
    gameover = pygame.image.load("images/gameover.png")
    #Victory image
    victory = pygame.image.load("images/victory.png")
    #Music and sound effects
    pygame.mixer.music.load("sound/spearOfJustice.mp3")
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_volume(0.1)
    playerHit = pygame.mixer.Sound("sound/playerHit.wav")
    playerHit.set_volume(0.3)
    enemyKilled = pygame.mixer.Sound("sound/enemyKilled.wav")
    enemyKilled.set_volume(0.3)
    win = pygame.mixer.Sound("sound/win.wav")
    win.set_volume(0.3)
    lose = pygame.mixer.Sound("sound/lose.wav")
    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    keepGoing = True
     
    # Loop
    while keepGoing: 
     
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            #Keyboard input, if no keys pressed player stops moving, if space pressed then shoot
            elif event.type == pygame.KEYUP:
                player.stopMoving()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #If the bullets are level 4, shoot 3 at a time, other wise just shoot one
                    if player.getBulletLvl() == 4:
                        for i in range (-1,2):
                            playerBullet = mySprites.PlayerBullets(screen,player.rect.centerx,player.rect.top,player.getBulletLvl(),i*2,i+1)
                            playerBullets.add(playerBullet)
                            allSprites.add(playerBullets)
                    else: 
                        playerBullet = mySprites.PlayerBullets(screen,player.rect.centerx,player.rect.top,player.getBulletLvl(),0,0)
                        playerBullets.add(playerBullet)
                        allSprites.add(playerBullets)                        
        #Check keystates for smooth movement, supports both arrow keys and wasd
        keyStates = pygame.key.get_pressed()
        #WASD Movement
        if keyStates[pygame.K_w]:
            player.moveUp()           
        if keyStates[pygame.K_a]:
            player.moveLeft()
        if keyStates[pygame.K_s]:
            player.moveDown()          
        if keyStates[pygame.K_d]:
            player.moveRight()
        #Arrow Key movement
        if keyStates[pygame.K_UP]:
            player.moveUp()           
        if keyStates[pygame.K_LEFT]:
            player.moveLeft()
        if keyStates[pygame.K_DOWN]:
            player.moveDown()          
        if keyStates[pygame.K_RIGHT]:
            player.moveRight()        
            
        #If the boss is more 1000 pixels away from the screen then spawn power ups and reset planes after killing   
        if bossBody.rect.bottom < -1000:
            #Small plane shooting
            if random.randrange(100) == 1 and enemy1.rect.bottom >= 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - enemy1.rect.centerx)/45,(player.rect.centery - enemy1.rect.bottom)/45, enemy1.rect.centerx,enemy1.rect.bottom))  
                allSprites.add(enemyBullets)
            if random.randrange(100) == 2 and enemy2.rect.bottom >= 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - enemy2.rect.centerx)/45,(player.rect.centery - enemy2.rect.bottom)/45, enemy2.rect.centerx,enemy2.rect.bottom))   
                allSprites.add(enemyBullets)
            if random.randrange(100) == 3 and enemy3.rect.bottom >= 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - enemy3.rect.centerx)/45,(player.rect.centery - enemy3.rect.bottom)/45, enemy3.rect.centerx,enemy3.rect.bottom))   
                allSprites.add(enemyBullets)
                
            #Big Plane shooting V shaped bullet patterns
            if random.randrange(250) == 4 and enemyBig1.rect.centery >= 0:
                for i in range (-4,5,2):
                    enemyBullets.add(mySprites.EnemyBullets(screen, i, 10- abs(i), enemyBig1.rect.centerx,enemyBig1.rect.bottom))
                    allSprites.add(enemyBullets)
            if random.randrange(250) == 5 and enemyBig2.rect.centery >= 0:
                for i in range (-4,5,2):
                    enemyBullets.add(mySprites.EnemyBullets(screen, i, 10- abs(i), enemyBig2.rect.centerx,enemyBig2.rect.bottom))
                    allSprites.add(enemyBullets)
                    
            #Power ups
            #Gain life power pp
            if random.randrange(2100) == 6:
                powerUp1.appear()
            #Level up bullets power up, once bullets are max level stop spawning
            if random.randrange(1700) == 7 and player.getBulletLvl() < 4:
                powerUp2.appear()
            elif player.getBulletLvl() == 4:
                powerUp2.kill()
                    
            #Collision detection creates explosion when it kills a planes, resets after killing 
            #ENEMY COLLISION
            #Normal Plane Collision
            if pygame.sprite.spritecollide(enemy1,playerBullets,True):
                enemyKilled.play()
                scorekeeper.planeKilled(250)                
                explosion = mySprites.Explosion(screen,enemy1.rect.center)
                explosionGroup.add(explosion)
                allSprites.add(explosionGroup)
                enemy1.reset()  
                
            if pygame.sprite.spritecollide(enemy2,playerBullets,True):
                enemyKilled.play()
                scorekeeper.planeKilled(250)
                explosion = mySprites.Explosion(screen,enemy2.rect.center)
                explosionGroup.add(explosion)
                allSprites.add(explosionGroup)
                enemy2.reset()     
                
            if pygame.sprite.spritecollide(enemy3,playerBullets,True):
                enemyKilled.play()
                scorekeeper.planeKilled(250)
                explosion = mySprites.Explosion(screen,enemy3.rect.center)
                explosionGroup.add(explosion)
                allSprites.add(explosionGroup)
                enemy3.reset()
            #Big plane collision   
            if pygame.sprite.spritecollide(enemyBig1,playerBullets,True,pygame.sprite.collide_mask):
                enemyBig1.loseHealth(player.returnDmg())
                if enemyBig1.getHealth() <= 0:
                    enemyKilled.play()
                    explosion = mySprites.Explosion(screen,enemyBig1.rect.center)
                    explosionGroup.add(explosion)
                    allSprites.add(explosionGroup)                   
                    scorekeeper.planeKilled(1500)
                    
            if pygame.sprite.spritecollide(enemyBig2,playerBullets,True,pygame.sprite.collide_mask):
                enemyBig2.loseHealth(player.returnDmg()) 
                if enemyBig2.getHealth() <= 0:
                    enemyKilled.play()
                    explosion = mySprites.Explosion(screen,enemyBig2.rect.center)
                    explosionGroup.add(explosion)
                    allSprites.add(explosionGroup)                   
                    scorekeeper.planeKilled(1500) 
                    
            #PLAYER COLLISION
                    
            #PowerUp collision
            if player.rect.colliderect(powerUp1.rect):
                scorekeeper.playerGainLife()
                powerUp1.reset()        
                    
            if player.rect.colliderect(powerUp2.rect):
                player.bulletLvlUp()
                powerUp2.reset()
                
                
            #Player and Enemy bullet collision
            if pygame.sprite.spritecollide(player,enemyBullets,True,pygame.sprite.collide_mask):
                player.playerHit()
                playerHit.play()
                scorekeeper.playerLoseLife()
                
            #If player collides with any enemy from enemy group, then deal damage, lose life, and different things happen depending on enemy type    
            if pygame.sprite.spritecollide(player,enemyGroup,False,pygame.sprite.collide_mask): 
                for enemy in pygame.sprite.spritecollide(player,enemyGroup,False,pygame.sprite.collide_mask):
                    if enemy == enemy1 or enemy == enemy2 or enemy == enemy3:
                        enemyKilled.play()
                        explosion = mySprites.Explosion(screen,enemy.rect.center)
                        explosionGroup.add(explosion)
                        allSprites.add(explosionGroup)
                        scorekeeper.planeKilled(250)
                        enemy.reset()
                    if enemy == enemyBig1 or enemy == enemyBig2:
                        enemy.loseHealth(player.returnDmg())
                        if enemy.getHealth() == 0:
                            enemyKilled.play()
                            explosion = mySprites.Explosion(screen,enemyBig2.rect.center)
                            explosionGroup.add(explosion)
                            allSprites.add(explosionGroup)                   
                            scorekeeper.planeKilled(1500)
                            enemyBig2.reset()
                playerHit.play()
                player.playerHit()
                scorekeeper.playerLoseLife()  
                 
        #Change in music to prepare for boss fight
        if bossBody.rect.bottom == -2350: 
            pygame.mixer.music.load("sound/megalovania.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
        #If boss is about to approach the screen then kill planes when they die and stop spawning powerups
        if bossBody.rect.bottom >= -1000:    
            #If Boss is about to appear and big planes haven't spawned yet, prevent them from spawning
            if enemyBig1.rect.bottom <= 50:
                enemyBig1.reset()
                enemyBig1.kill()
            if enemyBig2.rect.bottom <= 50:
                enemyBig2.reset()
                enemyBig2.kill()
                
            #Small plane shooting
            if random.randrange(100) == 1 and enemy1.rect.bottom >= 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - enemy1.rect.centerx)/45,(player.rect.centery - enemy1.rect.bottom)/45, enemy1.rect.centerx,enemy1.rect.bottom))  
                allSprites.add(enemyBullets)
            if random.randrange(100) == 2 and enemy2.rect.bottom >= 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - enemy2.rect.centerx)/45,(player.rect.centery - enemy2.rect.bottom)/45, enemy2.rect.centerx,enemy2.rect.bottom))   
                allSprites.add(enemyBullets)
            if random.randrange(100) == 3 and enemy3.rect.bottom >= 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - enemy3.rect.centerx)/45,(player.rect.centery - enemy3.rect.bottom)/45, enemy3.rect.centerx,enemy3.rect.bottom))   
                allSprites.add(enemyBullets)
                
            #Big Plane shooting V shaped bullet patterns
            if random.randrange(250) == 4 and enemyBig1.rect.centery >= 0:
                for i in range (-4,5,2):
                    enemyBullets.add(mySprites.EnemyBullets(screen, i, 10- abs(i), enemyBig1.rect.centerx,enemyBig1.rect.bottom))
                    allSprites.add(enemyBullets)
            if random.randrange(250) == 5 and enemyBig2.rect.centery >= 0:
                for i in range (-4,5,2):
                    enemyBullets.add(mySprites.EnemyBullets(screen, i, 10- abs(i), enemyBig2.rect.centerx,enemyBig2.rect.bottom))
                    allSprites.add(enemyBullets)
                    
                    
            #BOSS WINGS SHOOTING
            #V Pattern
            if random.randrange(265) == 4 and bossBody.rect.bottom >= 100:
                for i in range (-6,7,2):
                    if bossWing1.getHealth() > 0:
                        enemyBullets.add(mySprites.EnemyBullets(screen, i, 10- abs(i), bossWing1.rect.right - 50,bossWing1.rect.bottom-50))
                    if bossWing2.getHealth() > 0:
                        enemyBullets.add(mySprites.EnemyBullets(screen, i, 10- abs(i), bossWing2.rect.left + 50,bossWing2.rect.bottom-50))
                    allSprites.add(enemyBullets)
                    
            #DIAGONAL PATTERN
            if random.randrange(305) == 4 and bossBody.rect.bottom >= 100 and bossWing1.getHealth() > 0:
                for i in range (-4,5,2):
                    enemyBullets.add(mySprites.EnemyBullets(screen, i, 8 + i, bossWing1.rect.right - 50,bossWing1.rect.bottom-50))
                    allSprites.add(enemyBullets)
            if random.randrange(305) == 4 and bossBody.rect.bottom >= 100 and bossWing2.getHealth() > 0:
                for i in range (-4,5,2):
                    enemyBullets.add(mySprites.EnemyBullets(screen, i, 8 - i, bossWing2.rect.left +50 ,bossWing2.rect.bottom-50))
                    allSprites.add(enemyBullets) 
                    
            #Regular shooting (Like the small planes)
            if random.randrange(65) == 4 and bossBody.rect.bottom >= 100 and bossWing1.getHealth() > 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - bossWing1.rect.left + 20)/45,(player.rect.centery - bossWing1.rect.bottom)/45, bossWing1.rect.left+20,bossWing1.rect.bottom -50 ))   
                allSprites.add(enemyBullets) 
            if random.randrange(65) == 4 and bossBody.rect.bottom >= 100 and bossWing2.getHealth() > 0:
                enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - bossWing2.rect.right - 25)/45,(player.rect.centery - bossWing2.rect.bottom)/45, bossWing2.rect.right-25,bossWing2.rect.bottom-50))   
                allSprites.add(enemyBullets) 
                
                
            #PHASE 2 SHOOTING/COLLISION
            #If both wings are killed then allow collision on boss body
            if bossWing1.getHealth() <=0 and bossWing2.getHealth() <=0:
                if not random.randrange(8):
                    enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - bossBody.rect.centerx)/45,(player.rect.centery - bossBody.rect.bottom)/45, bossBody.rect.centerx,bossBody.rect.bottom))   
                    allSprites.add(enemyBullets)
                #If the hp is above 10000 then boss collides with bullets
                if bossBody.getHealth() > 10000 and pygame.sprite.spritecollide(bossBody,playerBullets,True,pygame.sprite.collide_mask):
                    bossBody.loseHealth(player.returnDmg())
                    
                    
                #PHASE 2.5 SHOOTING AND COLLISION
                #Once the body of the boss is 10000 or less start phase 2.5
                if bossBody.getHealth() <= 10000:
                    bossMinion1.moveOut()
                    bossMinion2.moveOut() 
                    #Shoot reverse V shapes from boss Minion
                    if random.randrange(175) == 3 and bossMinion1.getHealth() > 0:
                        for i in range (-4,5,2):
                            enemyBullets.add(mySprites.EnemyBullets(screen, i, 10+ abs(i), bossMinion1.rect.centerx,bossMinion1.rect.bottom))
                            allSprites.add(enemyBullets)
                    if random.randrange(175) == 3 and bossMinion2.getHealth() > 0:
                        for i in range (-4,5,2):
                            enemyBullets.add(mySprites.EnemyBullets(screen, i, 10+ abs(i), bossMinion2.rect.centerx,bossMinion2.rect.bottom))
                            allSprites.add(enemyBullets)  
                    #Boss Minion Collision
                    if bossMinion1.getHealth() > 0 and pygame.sprite.spritecollide(bossMinion1,playerBullets,True,pygame.sprite.collide_mask):
                        bossMinion1.loseHealth(player.returnDmg())
                        if bossMinion1.getHealth() <= 0:
                            enemyKilled.play()
                            explosion = mySprites.Explosion(screen,bossMinion1.rect.center)
                            explosionGroup.add(explosion)
                            allSprites.add(explosionGroup)                   
                            scorekeeper.planeKilled(2500)                        
                    
                    if bossMinion2.getHealth() > 0 and pygame.sprite.spritecollide(bossMinion2,playerBullets,True,pygame.sprite.collide_mask):
                        bossMinion2.loseHealth(player.returnDmg())
                        if bossMinion2.getHealth() <= 0:
                            enemyKilled.play()
                            explosion = mySprites.Explosion(screen,bossMinion2.rect.center)
                            explosionGroup.add(explosion)
                            allSprites.add(explosionGroup)                   
                            scorekeeper.planeKilled(2500) 
                            
                            
                    #PHASE 3 SHOOTING AND COLLISION
                    #If both minions are dead then boss takes damage
                    if bossMinion1.getHealth() <= 0 and bossMinion2.getHealth() <=0:
                        if not random.randrange(23):
                            enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - bossBody.rect.centerx+50)/45,(player.rect.centery - bossBody.rect.bottom-25)/45, bossBody.rect.centerx+50,bossBody.rect.bottom-35))
                            enemyBullets.add(mySprites.EnemyBullets(screen,(player.rect.centerx - bossBody.rect.centerx-50)/45,(player.rect.centery - bossBody.rect.bottom-25)/45, bossBody.rect.centerx-50,bossBody.rect.bottom-35))
                            allSprites.add(enemyBullets) 
                        if bossBody.getHealth() > 0 and bossBody.getHealth() <=10000 and pygame.sprite.spritecollide(bossBody,playerBullets,True,pygame.sprite.collide_mask):
                            bossBody.loseHealth(player.returnDmg())
                            if bossBody.getHealth() <= 0:
                                #Play more explosion noises for boss death
                                for i in range (7):
                                    enemyKilled.play()
                                    pygame.time.delay(125)
                                explosion = mySprites.Explosion(screen,bossBody.rect.center)
                                explosionGroup.add(explosion)
                                allSprites.add(explosionGroup)                   
                                scorekeeper.planeKilled(7500)
       
      
            #Collision detection, but this time kills planes instead of resetting
            #ENEMY COLLISION
            #Normal Planes
            if pygame.sprite.spritecollide(enemy1,playerBullets,True):
                enemyKilled.play()
                scorekeeper.planeKilled(250)
                explosion = mySprites.Explosion(screen,enemy1.rect.center)
                explosionGroup.add(explosion)
                allSprites.add(explosionGroup)
                enemy1.reset()
                enemy1.kill()
                
            if pygame.sprite.spritecollide(enemy2,playerBullets,True):
                enemyKilled.play()
                scorekeeper.planeKilled(250)                
                explosion = mySprites.Explosion(screen,enemy2.rect.center)
                explosionGroup.add(explosion)
                allSprites.add(explosionGroup)
                enemy2.reset()
                enemy2.kill()
                
            if pygame.sprite.spritecollide(enemy3,playerBullets,True):
                enemyKilled.play()
                scorekeeper.planeKilled(250)
                explosion = mySprites.Explosion(screen,enemy3.rect.center)
                explosionGroup.add(explosion)
                allSprites.add(explosionGroup)
                enemy3.reset()
                enemy3.kill()
                
            #Big Plane Collision, Kills the plane if boss is approaching    
            if enemyBig1.getHealth() > 0 and pygame.sprite.spritecollide(enemyBig1,playerBullets,True,pygame.sprite.collide_mask):
                enemyBig1.loseHealth(player.returnDmg())
                if enemyBig1.getHealth() <= 0:
                    enemyKilled.play()
                    explosion = mySprites.Explosion(screen,enemyBig1.rect.center)
                    explosionGroup.add(explosion)
                    allSprites.add(explosionGroup)                   
                    scorekeeper.planeKilled(1500)
                    enemyBig1.kill()
                    
            if enemyBig2.getHealth() > 0 and pygame.sprite.spritecollide(enemyBig2,playerBullets,True,pygame.sprite.collide_mask):
                enemyBig2.loseHealth(player.returnDmg()) 
                if enemyBig2.getHealth() <= 0:
                    enemyKilled.play()
                    explosion = mySprites.Explosion(screen,enemyBig2.rect.center)
                    explosionGroup.add(explosion)
                    allSprites.add(explosionGroup)                   
                    scorekeeper.planeKilled(1500)
                    enemyBig2.reset()
                    enemyBig2.kill()
                    
            #Boss Wing 1 Collision      
            if bossWing1.getHealth() > 0 and pygame.sprite.spritecollide(bossWing1,playerBullets,True,pygame.sprite.collide_mask):
                bossWing1.loseHealth(player.returnDmg())
                if bossWing1.getHealth() <= 0:
                    enemyKilled.play()
                    explosion = mySprites.Explosion(screen,bossWing1.rect.center)
                    explosionGroup.add(explosion)
                    allSprites.add(explosionGroup)                   
                    scorekeeper.planeKilled(5000)                   
      
            #Boss Wing 2 collision
            if bossWing2.getHealth() > 0 and pygame.sprite.spritecollide(bossWing2,playerBullets,True,pygame.sprite.collide_mask):
                bossWing2.loseHealth(player.returnDmg()) 
                if bossWing2.getHealth() <= 0:
                    enemyKilled.play()
                    explosion = mySprites.Explosion(screen,bossWing2.rect.center)
                    explosionGroup.add(explosion)
                    allSprites.add(explosionGroup)                   
                    scorekeeper.planeKilled(5000) 
                    
            #Power Up Collision, in case of the rare chance a power up spawns before boss is > -1000 and stays on the screen when boss is > -1000
            if player.rect.colliderect(powerUp1.rect):
                scorekeeper.playerGainLife()
                powerUp1.reset()        
                            
            if player.rect.colliderect(powerUp2.rect):
                player.bulletLvlUp()
                powerUp2.reset()        
            #Player and Enemy Bullet Collision
            if pygame.sprite.spritecollide(player,enemyBullets,True,pygame.sprite.collide_mask):
                player.playerHit()
                playerHit.play()
                scorekeeper.playerLoseLife()
            #If plane collides with any enemy from enemy group, then deal damage, lose life, and different things happen depending on enemy type
            if pygame.sprite.spritecollide(player,enemyGroup,False,pygame.sprite.collide_mask): 
                for enemy in pygame.sprite.spritecollide(player,enemyGroup,False,pygame.sprite.collide_mask):
                    #Normal Planes
                    if enemy == enemy1 or enemy == enemy2 or enemy == enemy3:
                        enemyKilled.play()
                        explosion = mySprites.Explosion(screen,enemy.rect.center)
                        explosionGroup.add(explosion)
                        allSprites.add(explosionGroup)
                        scorekeeper.planeKilled(250)
                        enemy.reset()
                        enemy.kill()
                    #Big Planes
                    if enemy == enemyBig1 or enemy == enemyBig2:
                        enemy.loseHealth(player.returnDmg())
                        if enemy.getHealth() <= 0:
                            enemyKilled.play()
                            explosion = mySprites.Explosion(screen,enemy.rect.center)
                            explosionGroup.add(explosion)
                            allSprites.add(explosionGroup)                   
                            scorekeeper.planeKilled(1500)
                            enemy.reset()
                            enemy.kill()
                    #Boss Wings and Boss Body
                    if enemy == bossWing1 or enemy == bossWing2 or enemy == bossBody:
                        enemy.loseHealth(player.returnDmg())
                        if enemy.getHealth() <= 0:
                            enemyKilled.play()
                            explosion = mySprites.Explosion(screen,enemy.rect.center)
                            explosionGroup.add(explosion)
                            allSprites.add(explosionGroup)                   
                            scorekeeper.planeKilled(5000)
                    #Boss Minions
                    if enemy == bossMinion1 or enemy == bossMinion2:
                        enemy.loseHealth(player.returnDmg())
                        if enemy.getHealth() <= 0:
                            enemyKilled.play()
                            explosion = mySprites.Explosion(screen,enemy.rect.center)
                            explosionGroup.add(explosion)
                            allSprites.add(explosionGroup)                   
                            scorekeeper.planeKilled(2500)                  
                playerHit.play()
                player.playerHit()
                scorekeeper.playerLoseLife()  
                
        if scorekeeper.getLives() <= 0 or bossBody.getHealth() <= 0:
            #Sets the highscore in current game
            pygame.mixer.music.fadeout(500)
            highScores = open("highScores.txt",'r')
            line = highScores.readline()
            if scorekeeper.getScore() > int(line):
                highScores = open("highScores.txt",'w')
                highScores.write(str(scorekeeper.getScore()))
                highScores.close()
            keepGoing = False
                
                # Refresh screen
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)      
        pygame.display.flip()
    #Play different sound effects and display message depending on win/loss
    if scorekeeper.getLives() <= 0:
        lose.play()
        pygame.time.delay(2000)
        screen.blit(gameover, (0, 200))
        pygame.display.flip()
        pygame.time.delay(3000)        
    if bossBody.getHealth() <=0:
        win.play()
        screen.blit(victory, (35, 350))
        pygame.display.flip()
        pygame.time.delay(3000)
   
def main():
    '''This function defines our mainline logic'''
    #While quitGame in tutorial function returns false, run the game
    while not tutorial():
        game()
    #Reset highscores after player closes game
    highScores = open("highScores.txt",'w')
    highScores.write("0")
    highScores.close()
    #If quitGame in tutorial function is true then quit the game, and set mouse as visible
    pygame.mouse.set_visible(True)
    pygame.quit()
               
# Call the main function
main()