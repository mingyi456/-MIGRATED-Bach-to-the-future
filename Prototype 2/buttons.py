
import rgb
import pygame
import config
pygame.init()

def isWithin(point, rect):
	if point[0] > rect[0] and point[0] < (rect[0] + rect[2]):
		if point[1] > rect[1] and point[1] < (rect[1] + rect[3]):
			return True
	return False

class Button:
	def __init__(self, name, pos, size, key, colour,font, font_colour, hl_colour, sel_colour):
		self.name= name
		self.coords= list(pos)
		self.size= list(size)
		self.rect= self.coords+self.size
		self.def_colour= self.colour= colour
		self.font_colour= font_colour
		self.hl_colour= hl_colour
		self.sel_colour= sel_colour
		self.font= font

class Button_Manager:
	def __init__(self):
		self.buttons= []
	
	def add_button(self, name, pos, size, key= None, colour= rgb.GREY, font=pygame.font.SysFont(config.DEF_FONT, config.DEF_FONT_SIZE), font_colour= rgb.BLACK, hl_colour= rgb.YELLOW, sel_colour= rgb.GREEN):
		self.buttons.append(Button(name, pos, size, key, colour, font, font_colour, hl_colour, sel_colour))
	
	def chk_buttons(self, events):
		curr_pos= pygame.mouse.get_pos()
		for event in events:
	
			if event.type == pygame.MOUSEBUTTONDOWN:
	
				if event.button == 1:
	
					for button in self.buttons:
	
						if isWithin(curr_pos, button.rect):
							button.colour= button.sel_colour
	
							print(f"Button \"{button.name}\" clicked!")
							return button.name
	
					print(f"No buttons clicked! Cursor position : {curr_pos}")
					return
	
			elif event.type == pygame.MOUSEBUTTONUP:
	
				for button in self.buttons:
					button.colour= button.def_colour
	
				return
		
		for button in self.buttons:
			if isWithin(curr_pos, button.rect):
				button.colour= rgb.GREY
			else:
				button.colour= button.def_colour
		
	def draw_buttons(self, screen):
		for button in self.buttons:
			text= button.font.render(button.name, 1, button.font_colour)
			text_len= text.get_width()
			button.rect[2]= max( ( text_len, button.rect[2]))
	
			pygame.draw.rect(screen, button.colour, button.rect)
			screen.blit(text, button.rect)