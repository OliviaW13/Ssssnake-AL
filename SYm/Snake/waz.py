import pygame
import time
import random


pygame.init()

screen = pygame.display.set_mode((600, 500))

pygame.display.set_caption('Snake')

# Obiekt reprezentujacy 2 wymiarowy wektor
class Vector2(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	# Przeciazenia operatorow

	# Equals: self == other
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	# Multiplication: self * other
	def __mul__(self, other):
		return Vector2(self.x * other, self.y * other)

	# Addition: self + other
	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	# Subtraction: self - other
	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)

	# Negataion: -self
	def __neg__(self):
		return Vector2(-self.x, -self.y)

	# Wartosc absolutna
	def abs(self):
		return Vector2(abs(self.x), abs(self.y))

	# Obroc wektor o 90 stopni w prawo
	def rot_right(self):
		return Vector2(self.y, -self.x)

	# Obroc wektor o 90 stopni w lewo
	def rot_left(self):
		return Vector2(-self.y, self.x)

	# Dlugosc wektora
	def magnitude(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def normalize(self):
		mag = self.magnitude()
		if mag == 0:
			mag = 1
		return Vector2(self.x / mag, self.y / mag)

	# Przeksztalc wektor na jeden z czterech kierunkow
	def to_dir(self):
		if self.abs().x > self.abs().y:
			if self.x > 0:
				return RIGHT
			else:
				return LEFT
		else:
			if self.y > 0:
				return DOWN
			else:
				return UP

	# Metoda zamienia wektor na string
	def __str__(self):
		return "[" + str(self.x) + ", " + str(self.y) + "]"




# Obiekt weza
class Snake(object):
	def __init__(self, pos, dir):
		# Lista Vectoe2 z czesciami weza
		# Element 0 to glowa, a ostatni to koniec
		self.body = [pos]
		# Aktualny kierunek (Vector2)
		self.dir = dir

	# Poczatek weza
	def head(self):
		return self.body[0]
	
	def move(self, pop = True):
		pos = self.body[0] + self.dir
		self.body.insert(0, pos)
		if pop:
			self.body.pop()

	def draw(self):
		for part in self.body:
			pygame.draw.rect(screen, 'green', (part.x - 5, part.y - 5, 10, 10))
	

	def eat(self, food_pos):
		if self.head() == food_pos:
			food_pos = Vector2(random.randrange(1, (600//10)) * 10, random.randrange(1, (500//10)) * 10)
			return True
		return False

	def try_turn(self, dir):
		.
		if dir == Vector2(0, 0):
			return
		
		if dir == -self.dir:
			
			if self.head() + self.dir.rot_right() in self.body:
				self.dir = self.dir.rot_left()
			
			elif self.head() + self.dir.rot_left() in self.body:
				return
			
			else:
				self.dir = self.dir.rot_right()
			return
		elif self.head() + dir in self.body:
			return
		
		else:
			self.dir = dir

	# Srodek weza (srednia arymetyczna pozycji wszystkich jego czesci)
	def center(self):
		x = sum(v.x for v in self.body) / len(self.body)
		y = sum(v.y for v in self.body) / len(self.body)
		return Vector2(x, y)

# Wartosci dla 4 kierunkow
UP = Vector2(0, -10)
DOWN = Vector2(0, 10)
LEFT = Vector2(-10, 0)
RIGHT = Vector2(10, 0)

# Tworz weza
snake = Snake(Vector2(80, 30), RIGHT)
snake = Snake(Vector2(80, 30), LEFT)

# druga czesc
snake.body.append(Vector2(70, 30))
snake.body.append(Vector2(70, 30))


# Wagi 
go_food_weight = 4
avoid_center_weight = 2
avoid_walls_weight = 2

score = 0

game_speed = 50

clock = pygame.time.Clock()
# Pierwsze losowe miejsce jedzenia
food_pos = Vector2(random.randrange(1, (600//10)) * 10, random.randrange(1, (500//10)) * 10)

def show_score():
	font = pygame.font.SysFont('Georgia', 30)
	Font = font.render('Score : ' + str(score), True, 'pink')	
	rect = Font.get_rect()
	screen.blit(Font, rect)


def game_over():
	font = pygame.font.SysFont('Georgia', 50)
	Font = font.render(
		'GAME OVER PUNKTY: ' + str(score), True, 'purple')
	rect = Font.get_rect()
	rect.midtop = (600/2, 500/4)
	screen.blit(Font, rect)
	pygame.display.flip()
	# Zakoncz program automatycznie po 2 sekundach
	time.sleep(2)
	pygame.quit()
	quit()

while True: #petla gry obejmuje rzeczywista obsługe ruchu, gre nad warunkami, figure i funkcje wyniku
	# Obsluga ruchu gracza
	# Podany kierunek ruchu przez gracza
	# input_dir = Vector2(0, 0)
	# for event in pygame.event.get():
	# 	if event.type == pygame.KEYDOWN:
	# 		if event.key == pygame.K_UP:
	# 			input_dir = UP
	# 		if event.key == pygame.K_DOWN:
	# 			input_dir = DOWN
	# 		if event.key == pygame.K_LEFT:
	# 			input_dir = LEFT
	# 		if event.key == pygame.K_RIGHT:
	# 			input_dir = RIGHT
	# snake.try_turn(input_dir)
	
	# Wektor  w kierunku jedzenia
	food_dir = (food_pos - snake.head()).normalize()
	# Wektor normalny skierowany od srodka weza (aby waz unikal wlasnego ciala)
	avoid_dir = (snake.head() - snake.center()).normalize()
	# Wektor normalny skierowany w kierunku srodka ekranu (aby unikac scian)
	avoid_walls_dir = (Vector2(300, 200) - snake.head()).normalize()

	
	dir = (food_dir * go_food_weight + avoid_dir * avoid_center_weight + avoid_walls_dir * avoid_walls_weight).to_dir()
	snake.try_turn(dir)
	
	
	if snake.eat(food_pos):
		score += 10
		# Wylosuj nowa pozycje dla jedzenia
		food_pos = Vector2(random.randrange(1, (600//10)) * 10, random.randrange(1, (500//10)) * 10)
		# Porusz wezem i go wydluz
		snake.move(pop = False)
	else:
		# Jesli waz nie zje przesun weza
		snake.move()
		
	screen.fill('black')
	snake.draw()

	
	pygame.draw.circle(screen, 'dark red', (food_pos.x, food_pos.y), 5)

	
    
	 # Waz uderzyl w lewa/prawa sciane
	if snake.head().x < 0 or snake.head().x > 600 - 10:
		game_over()
	# Waz uderzyl w gorna lub dolna sciane
	if snake.head().y < 0 or snake.head().y > 500 - 10:
		game_over()
	# Waz uderzyl we wlasne cialo
	for part in snake.body[1:]:
		if snake.head() == part:
			game_over()

	# Wyswietl wynik
	show_score()

	pygame.display.update()
	clock.tick(game_speed)
