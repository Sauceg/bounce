import sys,pygame,time

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   
   # set the title of the display window
   title = 'Bounce'
   creators = "~Marvin"
   pygame.display.set_caption(title.center(70) + creators)
   # create a pygame display window
   pygame.display.set_mode((420,280))
  
   # get the display surface
   surface = pygame.display.get_surface() 
   
   # create a game object
   game = Game(surface)
  
   # start the main game loop by calling the play method on the game object
   game.play() 
   
   # quit pygame and clean up the pygame window
   pygame.display.flip()  
   pygame.quit() 



class Game():
   def __init__(self,w_surface):
      # pace that the game runs at 
      self.FPS = 50                       # FPS (frames per second) its the speed the game runs at 
      
      self.game_Clock = pygame.time.Clock() # A clock that starts when the window opens  
       
      self.surface = w_surface               # surface the game is played on 
      
      self.ball_image = "clipart237889.png"  # i ended up just drawing a red circleand made it the ball 
      self.spike_image = "kindpng_5633026.png" # spike the image 
      
      self.close_game = False    
      self.continue_game = True
      
      self.size = self.surface.get_size()
      self.bg_color = pygame.Color((135,206,235)) # colour of the background 
      self.ball_diameter = 12 
      self.ball_vertical_increment = 4  # spead ball moves at vetically (number of pixels the ball moves up) 
      self.ball_horizontal_increment =  3 # "     "     "   "   horizontally... side to side 
      
      self.stage1 = True                  # might add different stages later 
      self.lives = 4 
      self.count = 0
    
   
      # initialized the walls 
      self.wall = Wall(73,235,50,45,"white",self.surface)
      self.wall2 = Wall(190,245,10,45,"white",self.surface)
      self.wall3 = Wall(250,235,15,5,"white",self.surface)
      self.wall4 = Wall(320,235,15,5,"white",self.surface)
      self.walls = [self.wall,self.wall2, self.wall3, self.wall4]
         
      # initilaized  the ball
      self.ball = Ball(self.surface,self.ball_diameter,self.walls, self.ball_image)
      self.ring_drawn = False 
     
     
     
   # play method checks if the player closes/quits the game and updates the window 
   
   def play(self): 
      
      while not self.close_game:
        
         
         self.handle_events() # Handle different user inputs 
         self.draw()          # draw the objects on the window
         if self.continue_game:
            self.update()     # just moves the ball for now 
            self.decide_continue()
       
         
         self.game_Clock.tick(self.FPS)
      
         
        
      
         
         
      

   # just initializes spike objects 
   def load_spike(self):
     
      self.spike = pygame.image.load(self.spike_image)
      self.spike = pygame.transform.scale(self.spike,(62,12))
      self.spikerect =  self.spike.get_rect()
     
      self.spike1rect = self.spikerect.copy()
      self.spike1rect.move_ip(123,268)
      self.surface.blit(self.spike,self.spike1rect)
      
      self.spike2rect = self.spikerect.copy()
      self.spike2rect.move_ip(200,268)
      self.surface.blit(self.spike,self.spike2rect)
      
      self.spike3rect = self.spikerect.copy()
      self.spike3rect.move_ip(262,268)
      self.surface.blit(self.spike,self.spike3rect)
      
      self.spike4rect = self.spikerect.copy()
      self.spike4rect.move_ip(324,268)
      self.surface.blit(self.spike,self.spike4rect)
      
      self.spikerects = [self.spike1rect,self.spike2rect,self.spike3rect,self.spike4rect] 
      
      #self.surface.blit(self.spike,(123,268))
      #self.surface.blit(self.spike,(200,268))
      #self.surface.blit(self.spike,(262,268))
      #self.surface.blit(self.spike,(324,268))
         
   # initializes ring 
   def load_ring(self):
     
      self.rings =  ['ring1.gif','ring2.gif','ring3.gif','ring4.gif']
      self.ring = pygame.image.load(self.rings[self.count])
      self.ring = pygame.transform.scale(self.ring,(20,20))
      self.ringrect = self.ring.get_rect()
      self.ringrect.move_ip(395,255)
      self.surface.blit(self.ring,self.ringrect)
      if not self.ring_drawn: 
         self.ring_drawn_time =  pygame.time.get_ticks()
         self.ring_drawn = True 

      print(self.current_time, self.ring_drawn_time)
      if self.current_time - self.ring_drawn_time > 100:
         self.ring_drawn = False 
         self.count  += 1 
      if self.count == 4:
         self.count = 0
         
      
   
   # draws all the obejects in the window 
   def load_stage1(self):
      
      self.surface.fill(self.bg_color)
      
      self.wall4.draw()
      self.wall3.draw()
      self.wall2.draw()
      self.wall.draw()
      self.load_spike()
      self.load_ring()    
      

   def handle_events(self):
      #get events 
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:  # check if the close window event happens and set self.close_clicked to false 
            self.close_game = True
         elif event.type == pygame.KEYDOWN: # check if the user presses a key down and the game uses handle_key_down funtcion to react accodingly 
            self.handle_keydown(event)
         elif event.type == pygame.KEYUP:   # check if the user releases a key and the game uses handle_key_up function to react accodingly
            self.handle_keyup(event)
  
   # Acts based on what evenst being recieved 
   def handle_keydown(self,event):
      # if the user clicks up ball moves up by reducing the center on y axis by vertical increment 
      
      
      if self.ball.rect.bottom ==  self.ball.wall.y or self.ball.rect.bottom ==  self.size[1]:
         if event.key == pygame.K_UP:
            self.ball.set_vertical_velocity(-self.ball_vertical_increment)
      # if the user clicks right, ball moves right, by increasing the center on x axis by horizontal increment 
      if event.key == pygame.K_RIGHT:
         self.ball.set_horizontal_velocity(self.ball_horizontal_increment)
      # if the user clicks left, ball moves left, by reducing the center on x axis by horizontal increment 
      if event.key == pygame.K_LEFT:
         self.ball.set_horizontal_velocity(-self.ball_horizontal_increment)
   
   # handle what happens when the user releases the right and left button- ball stops moving 
   def handle_keyup(self,event):
      if event.key == pygame.K_RIGHT :
         self.ball.set_horizontal_velocity(0)
      if event.key == pygame.K_LEFT:
         self.ball.set_horizontal_velocity(0)
           
   
   def draw(self):
      self.load_stage1()      # draw stage 
      self.ball.draw()        # draw ball 
      self.draw_lives()
      if not self.continue_game:
         if self.is_gameover():
            self.game_over_screen()
         else:
            self.win_screen()
      
      pygame.display.update() # updates window 
     
      
   def update(self):
      self.ball.move()        # move ball 
      
   def draw_lives(self):
      font = pygame.font.SysFont('',25)  # text size 
      test_image = font.render('Lives:',True, pygame.Color('white'), self.bg_color) # text and the text color 
      location = (300,10)    # where txt is to be drawn 
      self.surface.blit(test_image,location)   # blits the text to surface and intended location 
      pos = [360, 19] 
      for i in range(self.lives):
         if i == 0: 
            pygame.draw.circle(self.surface,(235,0,0),(pos[0] , pos[1]) , self.ball_diameter//2 ) 
         else:
            pygame.draw.circle(self.surface,(235,0,0),(pos[0] + (self.ball_diameter *i ) + 3 *i, pos[1]),self.ball_diameter//2) 
          
         
   def game_over_screen(self):
      font = pygame.font.SysFont('',50)  # text size 
      test_image = font.render('Gameover!',True, pygame.Color('white'), self.bg_color) # text and the text color 
      location = (self.size[0]//2 - 100,self.size[1]//2 - 20)    # where tx   
      self.surface.blit(test_image,location)
      
   def win_screen(self):
      font = pygame.font.SysFont('',50)  # text size 
      test_image = font.render('Easy Dubs!!!',True, pygame.Color('white'), self.bg_color) # text and the text color 
      location = (self.size[0]//2 - 100,self.size[1]//2 - 20)    # where tx   
      self.surface.blit(test_image,location)      
      
   def is_gameover(self):
      for spike in self.spikerects:
         if self.ball.rect.colliderect(spike):
            self.lives -= 1 
            self.ball.rect.x = 12 
            self.ball.rect.y = 268
         if self.lives == 0:
            self.continue_game = False 
            return True 
         
            
   def is_win(self):
      if self.ball.rect.colliderect(self.ringrect):
         self.continue_game = False 
         return True 
   def decide_continue(self):
      # when does the game end ?
      self.is_win()
      self.is_gameover()
            
            
            
            
      
      
              
class Ball():
   def __init__(self,surface,ball_diameter,walls,image):
         
      self.surface = surface 
      self.ball_diameter = ball_diameter
      self.horizontal_velocity = 0
      self.vertical_velocity = 0 
      self.start_pos = [self.ball_diameter,self.surface.get_height()-ball_diameter]
      self.image = image 
      self.walls = walls
      self.ball_image =  pygame.image.load(self.image)
      pygame.image.load(self.image)
      self.ball_image = pygame.transform.scale(self.ball_image,(self.ball_diameter,self.ball_diameter))
      self.rect =  self.ball_image.get_rect()   
      self.rect.move_ip(self.start_pos[0],self.start_pos[1])      
      self.touched_wallside = False 
      self.touched_walltop =  False         
      #self.platform = platform 
      #self.traps = traps 
      #self.key = key
  
   def draw(self):
      self.surface.blit(self.ball_image,self.rect)  # draws ball 
   
   def set_horizontal_velocity(self,ball_increment): 
      self.horizontal_velocity = ball_increment 
      
   def set_vertical_velocity(self,ball_increment):
      self.vertical_velocity = ball_increment
      
   def move(self):
      self.size = self.surface.get_size() # get the size of the window
      
      self.rect = self.rect.move(self.horizontal_velocity,self.vertical_velocity)
      
     
   
      if not (self.touched_wallside or self.touched_walltop):
         self.wall = self.collide_point() # function not done but it should chect when the ball hits a wall 
      
      if self.touched_wallside:
         if self.rect.left > self.wall.rect.left:
            self.horizontal_velocity = 0 
         else:
            self.rect.right = self.wall.rect.left
         self.touched_wallside = False 
     
      if self.touched_walltop:
         self.rect.bottom =  self.wall.y
         self.touched_walltop = False 
        
         
      ## checks if the ball is going past the window and updates its position to stay in 
      
      if self.rect.bottom >= self.surface.get_height():
         self.rect.bottom = self.surface.get_height()
      elif self.rect.top <= 185:
         self.set_vertical_velocity(-self.vertical_velocity + .5 )
         #move the paddle back by its width 
      if self.rect.left  <= 0:
         self.rect.left = 0 
      elif self.rect.right >= self.surface.get_width():
         self.rect.right = self.surface.get_width()
      
  
         
  
   def collide_point(self):
      
      for wall in self.walls: 
         if wall.rect.colliderect(self.rect):
            if self.rect.bottom >= wall.rect.y + self.vertical_velocity +1:
               self.touched_wallside = True
               break 
            else:
               self.touched_walltop = True  
               self.touched_wallside = False    
               break 
      return wall 
     
         
         
class Wall():
   def __init__(self,x,y,width,height,color,surface):
      self.x = x
      self.y = y 
      self.width = width 
      self.height = height 
      self.rect = pygame.Rect(x,y,width,height)
      self.color = pygame.Color(color)
      self.surface = surface
   def draw(self):
      pygame.draw.rect(self.surface,self.color,self.rect)
   def copy(self):
      return self.wall.copy()


class Traps():
   def __init__(self,surface,platform,keys,ball):
      self.surface = surface
      self.surface = surface
      self.platform = platform 
      self.traps = traps 
      self.key = key
      self.ball = ball 
           
  

class Key(): 
   def __init__(self,surface,key,platform,traps,ball):
      self.surface = surface
      self.platform = platform 
      self.traps = traps 
      self.key = key
      self.ball = ball 
            
    
          
    

main()


# make the ring gif
# make different stages 
# make 


# make the game end 
# add time =score and gameover animation 