#Rokcet Animation
#@Michael Brown: BubbleCipherStudios

from kivy.config import Config

DisplayWidth = 1080
DisplayHeight = 720

Dimensions = (DisplayWidth, DisplayHeight)

Config.set('graphics', 'width', DisplayWidth)
Config.set('graphics', 'height', DisplayHeight)

Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

#Needed for compiling exe with additional files per Kivy Docs
from kivy.resources import resource_add_path, resource_find

import os
import sys
import math
from random import randint


WindowStartx = DisplayWidth//2
WindowStarty = DisplayHeight//3

class WindowManager(ScreenManager):
	pass
	
class RocketButton(Button):
	def __init__(self,**kwargs):
		super(RocketButton, self).__init__(**kwargs)
		
		self.size=(145,160)
		self.pos=(WindowStartx-(self.size[0]/2), WindowStarty/2)
		
		self.rocket = Image('rocket.png').texture
		self.rocket_rect = Rectangle(texture = self.rocket, size=self.size, pos = self.pos)

		#this is needed to override default button image and color
		self.background_normal = ''
		self.color = [0,0,0,0]
		self.background_color = (0,0,0,0)
	
		
		self.canvas.before.add(self.rocket_rect)
		
	def on_parent(self, widget, parent):
		self.size_hint_x = None
		self.size_hint_y = None

class ClickmeLabel(Label):
	def __init__(self,**kwargs):
		super(ClickmeLabel, self).__init__(**kwargs)
		self.markup = True
		self.text = ' Click the Rocket\n'+'to begin animation'
		self.center_x = DisplayWidth/2-(self.width/2)
		self.center_y = DisplayHeight-(DisplayHeight//3)

		

		self.font_size='30sp'
		self.bind(size=self.setter('text_size'))
		#self.pos=(WindowStartx, (DisplayHeight/2))
	
	
class MenuScreen(Screen):
	def __init__(self, **kwargs):
		super(MenuScreen, self).__init__(**kwargs)
		
		self.fl = FloatLayout()
		self.btn2 = RocketButton()
		self.label = ClickmeLabel()
		self.fl.add_widget(self.label)
		self.fl.add_widget(self.btn2)
		self.add_widget(self.fl)
		self.btn2.bind(on_press = self.screen_transition)

	def screen_transition(self, *args):
		self.manager.current = 'rocketscreen'

class RocketScreen(Screen):
	def __init__(self, **kwargs):
		super(RocketScreen, self).__init__(**kwargs)
	
	def on_pre_enter(self):
	
		#bx = BoxLayout()
		self.add_widget(MainLayout())
		#self.add_widget(bx)

class MainLayout(FloatLayout):
	def __init__(self,**kwargs):
		super(MainLayout, self).__init__(**kwargs)
		self.size = (DisplayWidth, DisplayHeight)
		self.canvas.add(Color(.01,.01,.01,1))
		self.bg = Rectangle(pos=self.pos, size=(DisplayWidth,DisplayHeight))
		self.canvas.add(self.bg)
		self.bind(height=self.redraw_background)
		self.bind(width=self.redraw_background)
		
		self.num_of_lines = self.width//26
		
		for i in range(self.num_of_lines):
			self.add_widget(Fallingline())
		self.rocket = RocketWidget()
		self.add_widget(self.rocket)
		
	
	def redraw_background(self, *args):
		self.bg.size = (self.width,self.height)
		self.bg.pos = self.pos
		
	def on_touch_up(self, touch):
		if touch.is_double_tap:
			self.parent.manager.current = 'mainmenu'
			self.rocket.animation_clock.cancel()
			self.parent.remove_widget(self)
			
		
	#def on_parent(self, widget, parent):
		#self.size = (parent.width, parent.height)
		
class Fallingline(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.size = (randint(1,3),randint(DisplayHeight//7,DisplayHeight//4))
		self.pos = ((randint(0,DisplayWidth-self.width)),DisplayHeight)
		self.color = Color(1,1,1,1)
		self.rect = Rectangle(size=self.size,pos = self.pos)
		self.canvas.add(self.color)
		self.canvas.add(self.rect)
		self.bind(pos=self.redraw)
		
		self.scale = randint(1,4)
		
		###ADD DELAY ###


		Clock.schedule_once(self.start_anim, randint(1,3))

	#there will be a for loop that determines the index for this function	
	def start_anim(self, dt):
		Clock.schedule_interval(self.animate_center,1/60)
		
	def animate_center(self, dt):

		current_x = self.pos[0]
		current_y = self.pos[1]
		step = 600
		stepsize = step  * self.scale * dt
		
		if current_y + self.height < 0:
			current_y = DisplayHeight-10
			self.scale = randint(1,4)
			
		else:
			current_y -= stepsize
		
		self.pos = (current_x, current_y)	

	
	def redraw(self, *args):
		self.rect.pos = self.pos
		

class RocketWidget(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.rocket = Image('rocket.png').texture
		self.flames = Image('flames.png').texture
		
		self.size = (180, 200)
		self.flame_size = self.get_flames_size()
		
		window_center = (WindowStartx-(self.width//2),WindowStarty-(self.height//2))
		
		self.pos = window_center
		
		self.rocket_rect = Rectangle(texture = self.rocket, size=self.size,pos = self.pos)
		self.flames_rect = Rectangle(texture = self.flames, size=self.flame_size, pos = self.get_flames_pos(self.pos))
		
		self.canvas.add(self.flames_rect)
		self.canvas.add(self.rocket_rect)
		
		self.bind(pos=self.redraw)
		
		self.index = 0
		self.counter_x = 0
		self.counter_y = 0
		self.slope_x = 0
		self.slope_y = 0
		
		self.flames_counter_x = 0
		self.flames_counter_y = 0
		self.flames_slope_y = 0
		self.flames_slope_x = 0
		
		self.scale = 3
		
		self.passed_x = False
		self.passed_y = False

		
		self.next_pos = (0,0)
		self.flames_next_pos = (0,0)
		self.animating = False
		
		
		self.list_coords = []
		self.flame_coords = []
		max_list_length = 100
		
		for i in range(max_list_length):
			rand_x = randint(self.pos[0]-5, self.pos[0]+5)
			rand_y = randint(self.pos[1]-10, self.pos[1]+10)
			rand_pos = rand_x, rand_y
			self.list_coords.append(rand_pos)
		
		for coord in self.list_coords:
			f_coord = self.get_flames_pos((coord[0],coord[1]))
			f_coord = (math.ceil(f_coord[0]),math.ceil(f_coord[1]))
			rand_x = randint(f_coord[0]-1,f_coord[0]+1)
			rand_y = randint(f_coord[1]-1,f_coord[1]+1)
			self.flame_coords.append((rand_x,rand_y))

		self.animation_clock = Clock.schedule_interval(self.animate_center, 1/60)


	def get_flames_pos(self, pos):
		padding = -5
		flame_size = self.flame_size
		
		diff_x = self.size[0]-flame_size[0]
		flame_x = pos[0] + (diff_x/2)
		
		diff_y = pos[1]-flame_size[1]
		flame_y = diff_y - padding
		
		return (flame_x,flame_y)
		
		
	def get_flames_size(self):
		flame_width = self.width/1.85
		flame_height = self.height/1.7
		return (flame_width,flame_height)
		
	def getslope(self):
		self.slope_x = 0
		self.slope_y = 0
		
		self.flames_slope_y = 0
		self.flames_slope_x = 0
		
		self.passed_x = False
		self.passed_y = False
		#get the current x,y
		
		current_x = self.pos[0]
		current_y = self.pos[1]
		
		flames_current_x = self.flames_rect.pos[0]
		flames_current_y = self.flames_rect.pos[1]
		
		#get the next x,y
		
		if self.index == len(self.list_coords)-1:
			self.next_pos = self.list_coords[0]
			self.flames_next_pos = self.flame_coords[0]
			self.index = 0
		else:
			self.next_pos = self.list_coords[self.index+1]
			self.flames_next_pos = self.flame_coords[self.index+1]
			self.index +=1
		
		next_x = self.next_pos[0]
		next_y = self.next_pos[1]
		
		flames_next_x = self.flames_next_pos[0]
		flames_next_y = self.flames_next_pos[1]
		
		#determine the slope for x 
		self.slope_x = next_x - current_x
		self.counter_x = self.slope_x
		
		self.flames_slope_x = flames_next_x - flames_current_x
		self.flames_counter_x = self.flames_slope_x
		
		
		#determine the slope for y 
		self.slope_y = next_y - current_y
		self.counter_y = self.slope_y
		
		self.flames_slope_y = flames_next_y - flames_current_y
		self.flames_counter_y = self.flames_slope_y
		
		self.animating = True
		
	
	def animate_center(self, dt):
	
		current_x = self.pos[0]
		current_y = self.pos[1]
		
		stepsize_x = self.slope_x * dt * self.scale
		stepsize_y = self.slope_y * dt * self.scale
		
		#decrease the remained slope with respect to negative or positive slope
		
		if self.animating:
			self.animate_flame(dt)
			if self.slope_x > 0:
				if (stepsize_x <= self.counter_x):
					self.counter_x -= stepsize_x
					current_x+= stepsize_x
					
				else:
					current_x = self.next_pos[0]
					self.passed_x = True
					
			elif self.slope_x < 0:
				if stepsize_x >= self.counter_x:
					self.counter_x -= stepsize_x
					current_x += stepsize_x
				else:
					current_x = self.next_pos[0]
					self.passed_x = True
			else:
				current_x = self.next_pos[0]
				self.passed_x = True
				
			if self.slope_y > 0:
				if (stepsize_y <= self.counter_y):
					self.counter_y -= stepsize_y
					current_y += stepsize_y
				else:
					current_y = self.next_pos[1]
					self.passed_y = True
					
			elif self.slope_y < 0:
				if stepsize_y >= self.counter_y:
					self.counter_y -= stepsize_y
					current_y += stepsize_y
				else:
					current_y = self.next_pos[1]
					self.passed_y = True
			else:
				current_y = self.next_pos[1]
				self.passed_y = True
				
			if self.passed_x and self.passed_y:
				self.animating = False
						
			
			self.pos = (current_x, current_y)
		else:
			self.getslope()


	def animate_flame(self, dt):
		
		
		current_x = self.flames_rect.pos[0]
		current_y = self.flames_rect.pos[1]
		
		stepsize_x = self.flames_slope_x * dt * self.scale
		stepsize_y = self.flames_slope_y * dt * self.scale
		
		#decrease the remained slope
		

		if self.flames_slope_x > 0:
			if stepsize_x <= self.flames_counter_x:
				self.flames_counter_x -= stepsize_x
				current_x+= stepsize_x
				
			else:
				current_x = self.flames_next_pos[0]
				
		elif self.flames_slope_x < 0:
			if stepsize_x >= self.flames_counter_x:
				self.flames_counter_x -= stepsize_x
				current_x += stepsize_x
			else:
				current_x = self.flames_next_pos[0]
		else:
			current_x = self.flames_next_pos[0]
			
		if self.flames_slope_y > 0:
			if (stepsize_y <= self.flames_counter_y):
				self.flames_counter_y -= stepsize_y
				current_y += stepsize_y
			else:
				current_y = self.flames_next_pos[1]
				
		elif self.flames_slope_y < 0:
			if stepsize_y >= self.flames_counter_y:
				self.flames_counter_y -= stepsize_y
				current_y += stepsize_y
			else:
				current_y = self.flames_next_pos[1]
		else:
			current_y = self.flames_next_pos[1]
					
		self.flames_rect.pos = (current_x, current_y)


	def redraw(self, *args):
		self.rocket_rect.pos = self.pos
		
class RocketAnimationApp(App):
	def build(self):
		sm = ScreenManager()
		sm.add_widget(MenuScreen(name='mainmenu'))
		sm.add_widget(RocketScreen(name='rocketscreen'))
		sm.current = 'mainmenu'
		return sm

if __name__ == '__main__':
	#necessary if compiling exe and adding files to --onefile option per Kivy docs
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
		
	RocketAnimationApp().run()
