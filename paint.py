import pygame, sys, math


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

draw_color = (0, 0, 255)  
bg_color = (0, 0, 0)    
radius = 5       


mode = "free"
start_pos = None

points = []

def draw_freehand(color):

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, radius)

while True:
    pressed = pygame.key.get_pressed()
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_f:
                mode = "free"
                print("Режим: свободное рисование")
            elif event.key == pygame.K_t:
                mode = "rect"
                print("Режим: прямоугольник")
            elif event.key == pygame.K_c:
                mode = "circle"
                print("Режим: круг")
            elif event.key == pygame.K_e:
                mode = "eraser"
                print("Режим: ластик")

            elif event.key == pygame.K_r:
                draw_color = (255, 0, 0)
                print("Цвет: красный")
            elif event.key == pygame.K_g:
                draw_color = (0, 255, 0)
                print("Цвет: зелёный")
            elif event.key == pygame.K_b:
                draw_color = (0, 0, 255)
                print("Цвет: синий")
            elif event.key == pygame.K_KP_PLUS and ctrl_held:
                radius+=5
            elif event.key == pygame.K_KP_MINUS and ctrl_held:
                if radius > 5:
                    radius -=5
                    


                

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                start_pos = event.pos
                if mode in ["free", "eraser"]:
                    points = [event.pos]  
                    
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if mode in ["free", "eraser"]:
                    points.append(event.pos)
                    
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and start_pos is not None:
                end_pos = event.pos

                current_color = bg_color if mode == "eraser" else draw_color
                if mode == "rect":
    
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(start_pos[0] - end_pos[0])
                    h = abs(start_pos[1] - end_pos[1])
                    pygame.draw.rect(screen, current_color, (x, y, w, h), radius)
                elif mode == "circle":

                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    r = int(math.hypot(dx, dy))
                    pygame.draw.circle(screen, current_color, start_pos, r, radius)

                start_pos = None
                points = []


    current_color = bg_color if mode == "eraser" else draw_color


    if mode in ["free", "eraser"] and points:
        draw_freehand(current_color)

    pygame.display.flip()
    clock.tick(60)