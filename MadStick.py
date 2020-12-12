import pygame, pygame.freetype
import sys
import random
import os

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("The Mad Stick")
Window_size = (400, 400)
screen = pygame.display.set_mode(Window_size, 0, 32)

# tiles config --------------------------------------------------------
tile_img = os.path.join("data", "tile.png")
tiles = pygame.image.load(tile_img)

# Player configs ------------------------------------------------------
player_img = os.path.join("data", "Stick.png")
player = pygame.image.load(player_img)
player.set_colorkey((255, 255, 255))

# Danger --------------------------------------------------------------
danger_img = os.path.join("data", "danger.png")
danger = pygame.image.load(danger_img)

# Star ----------------------------------------------------------------
star_img = os.path.join("data", "star.png")
star = pygame.image.load(star_img)
star.set_colorkey((255 ,255 ,255))

# Cloud ---------------------------------------------------------------
cloud_img = os.path.join("data", "cloud.png")
cloud = pygame.image.load(cloud_img)
cloud.set_colorkey((0, 0, 0))
black_cloud_img = os.path.join("data", "blackcloud.png")
black_cloud = pygame.image.load(black_cloud_img)
black_cloud.set_colorkey((0, 0, 0))

# Icon
icon_img = os.path.join("data", "icon.png")
icon = pygame.image.load(icon_img)
pygame.display.set_icon(icon)

# Sound
jump_sound = pygame.mixer.Sound(os.path.join("data", "jump.wav"))
hurt_sound = pygame.mixer.Sound(os.path.join("data", "hurt.wav"))

global mode

def main():
	running = True
	clicked = False

	while running:
		screen.fill((0,0,0))

		# All Text
		comman_font = pygame.freetype.Font(os.path.join("data", "Blue.ttf"), 13)
		menu_font = pygame.freetype.Font(os.path.join("data", "Blue.ttf"), 30)

		# Main menu and Modes text and render
		menu_font.render_to(screen, (Window_size[0]//3, 10), "Main Menu" , (255, 255, 255))
		comman_font.render_to(screen,(10, 50), "Collect Zen Stone to kill the monster" , (255, 255, 255))


		# Mode and render------------------------------------
		easy_button_rect = pygame.Rect(Window_size[0]//3, Window_size[1]//4, 150, 35)
		medium_button_rect = pygame.Rect(Window_size[0]//3, Window_size[1]//4 + 50, 150, 35)
		hard_button_rect = pygame.Rect(Window_size[0]//3, Window_size[1]//4 + 100, 150, 35)

		mode_font = pygame.freetype.Font(os.path.join("data", "Blue.ttf"), 25)

		easy_mode = mode_font.render_to(screen, (Window_size[0]//3 + 20, Window_size[1]//4 + 10), "Easy" , (255, 255, 255))
		medium_mode = mode_font.render_to(screen, (Window_size[0]//3 + 20, Window_size[1]//4 + 50 + 10), "medium" , (255, 255, 255))
		hard_mode = mode_font.render_to(screen, (Window_size[0]//3 + 20, Window_size[1]//4 + 100 + 10), "Hard" , (255, 255, 255))

		# Controls and render ---------------------------------------------------------------
		comman_font.render_to(screen,(10, Window_size[1] - 100) ,"Controls-", (255, 255, 255))

		comman_font.render_to(screen,(15, Window_size[1] - 80) ,"D - to move right", (255, 255, 255))
		comman_font.render_to(screen,(15, Window_size[1] - 60) ,"A - to move left", (255, 255, 255))
		comman_font.render_to(screen,(15, Window_size[1] - 40) ,"Enter - to jump", (255, 255, 255))


		# Check mouse press ------------------------------------------------------
		mx, my = pygame.mouse.get_pos()

		if easy_button_rect.collidepoint((mx, my)):
			mode = "easy"
			if clicked:
				game_loop(mode)
				
		if medium_button_rect.collidepoint((mx, my)):
			mode = "medium"
			if clicked:
				game_loop(mode)
				
		if hard_button_rect.collidepoint((mx, my)):
			mode = "hard"
			if clicked:
				game_loop(mode)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					clicked = True
			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False

		pygame.draw.rect(screen, (255, 255, 255), easy_button_rect, 2)
		pygame.draw.rect(screen, (255, 255, 255), medium_button_rect, 2)
		pygame.draw.rect(screen, (255, 255, 255), hard_button_rect, 2)
		pygame.display.update()
		
	pygame.quit()


def game_loop(mode):
	# PLAYER CONFIGS ----------------------------------------------
	player_pos_x = Window_size[0]//2
	player_pos_y = Window_size[1] - tiles.get_height() - player.get_height()
	player_pos_x = Window_size[0]//2
	player_pos_y = Window_size[1] - tiles.get_height() - player.get_height()
	moving_right = False
	moving_left  = False
	player_momentum = 0
	start_jump = False
	gravity_start = False

	# Danger configs ------------------------------------------------
	danger_pos_x = random.randint(0, Window_size[0] - danger.get_width())
	danger_pos_y = -1000
	danger_speed = 4
	danger_alive = True

	# Star configs --------------------------------------------------
	star_pos_x = random.randint(0, Window_size[0] - danger.get_width())
	star_pos_y = 250

	# cloud pos 
	cloud_pos_x = -cloud.get_width()
	cloud_pos_y = 10
	black_cloud_pos_x = -(cloud.get_width() + black_cloud.get_width())
	black_cloud_pos_y = 10

	BASICFONT = pygame.freetype.Font(os.path.join("data", "Blue.ttf"), 13)
	score = 0
	done = None
	is_won = False

	running = True
	while running:
		clock.tick(60)
		screen.fill((146, 244, 255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					moving_right = True
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					moving_left = True
				if event.key == pygame.K_RETURN:
					start_jump = True
					player_momentum = 6
					jump_sound.play()

				if event.key == pygame.K_s:
					if score >= done:
						danger_alive = False
						is_won = True
				if event.key == pygame.K_ESCAPE:
					main()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					moving_right = False
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					moving_left = False

		if is_won and danger_pos_y < 0:
			game_over(mode, "YOU WON")

		# player right left movement -------------------------------------
		if moving_right == True:
			player_pos_x += 4
		if moving_left == True:
			player_pos_x -= 4

		# All Rects ------------------------------------------------------
		player_rect = pygame.Rect(player_pos_x - 1, player_pos_y - 1, player.get_width() - 1, player.get_height() - 1)
		star_rect = pygame.Rect(star_pos_x, star_pos_y, star.get_width(), star.get_height())
		danger_rect = pygame.Rect(danger_pos_x - 2, danger_pos_y - 2, danger.get_width() - 2, danger.get_height() - 2)

		# check collisons -----------------------------------------------
		if player_rect.colliderect(star_rect):
			star_pos_x = random.randint(0, Window_size[0] - danger.get_width())
			score += 1
		if player_rect.colliderect(danger_rect):
			hurt_sound.play()
			game_over(mode, "YOU LOST")

		# Block player in screen -----------------------------------------
		if player_pos_x < 0 :
			player_pos_x = 0
		elif player_pos_x > Window_size[0] - player.get_width():
			player_pos_x = Window_size[0] - player.get_width()

		# JUMP LOGIC ------------------------------------------------------
		if start_jump:
			player_pos_y -= player_momentum
		if gravity_start:
			player_pos_y += player_momentum

		if player_pos_y > Window_size[1] - player.get_height() - 3 - tiles.get_height():
			player_momentum = 0
			gravity_start = False

		if player_pos_y < 270:
			start_jump = False
			gravity_start = True
		if start_jump == True and gravity_start == True:
			start_jump = False
			gravity_start = True


		# Danger velocity  -----------------------------------------------
		if danger_alive:
			if danger_pos_y < Window_size[0] - danger.get_height() - tiles.get_height():
				enemy_reached = True
				danger_pos_y += 6
			
			if danger_pos_y >= Window_size[0] - danger.get_height() - tiles.get_height():
				enemy_reached = False
				if danger_pos_x >= 0 and danger_pos_x <= Window_size[0]:
					danger_pos_x += danger_speed
					if danger_pos_x > Window_size[0] - danger.get_width():
						danger_speed = -danger_speed
					elif danger_pos_x <= 4:
						danger_speed = 4

		if not danger_alive:
			danger_pos_y -= 6

		if mode == "easy":
			done = 20
			if score < 20:
				message = "Collect 20 to kill him"
		if mode == "medium":
			done = 69
			if score < 69:
				message = "collect 69 to kill him"
		if mode == "hard":
			done = 100
			if score < 100:
				message = "collect 100 to kill him"

		if score >= done:
			message = "Press S to Kill him"

		# Cloud reset
		if (cloud_pos_x > Window_size[0]):
			cloud_pos_x = -(cloud.get_width() + 100)
		if (black_cloud_pos_x > Window_size[0]):
			black_cloud_pos_x = -( black_cloud.get_width())
		
		cloud_pos_x += 0.8
		black_cloud_pos_x += 1

		# All blit ------------------------------------------------------- 
		screen.blit(cloud, (cloud_pos_x, cloud_pos_y))
		screen.blit(black_cloud, (black_cloud_pos_x, black_cloud_pos_y))
		screen.blit(danger, (danger_pos_x, danger_pos_y))
		screen.blit(player, (player_pos_x , player_pos_y))
		screen.blit(star, (star_pos_x, star_pos_y))

		num = 0
		while num < Window_size[0]:
			screen.blit(tiles, (num, Window_size[1] - tiles.get_height()))
			num += tiles.get_width()

		# Score and message -----------------------------------------------
		BASICFONT.render_to(screen,(Window_size[0] - 140, 10) , 'Zen Stones: %s' % (score), (0, 0, 0))
		BASICFONT.render_to(screen, (0, 10) , message, (0, 0, 0))
		pygame.display.update()

	pygame.quit()

def game_over(mode, message):
	running = True
	if mode == "easy":
		message += " EASY MODE"
	if mode == "medium":
		message+= " MEDIUM MODE"
	if mode == "hard":
		message+= " HARD MODE"
	while running:
		screen.fill((0,0,0))
		game_font = pygame.freetype.Font(os.path.join("data", "Blue.ttf"), 25)
		restart_font = pygame.freetype.Font(os.path.join("data", "Blue.ttf"), 11)

		game_font.render_to(screen, (10, Window_size[1]//2 - 50) ,message, (255, 255, 255))
		restart_font.render_to(screen, (Window_size[1]//2 - 15, Window_size[1]//2) ,"Press R Restart Game", (255, 255, 255))
		restart_font.render_to(screen, (Window_size[1]//2 - 20, Window_size[1]//2 + 15) ,"Press ESCAPE for main menu", (255, 255, 255))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					game_loop(mode)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					main()

		pygame.display.update()
	pygame.quit()


if __name__ == '__main__':
	main()