import pygame
import math

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drawing App")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Drawing state variables
drawing = False
last_pos = None
current_color = BLACK
brush_size = 5
current_tool = "pen"  # Available tools: pen, eraser, rectangle, circle, square, right_triangle, equilateral_triangle, rhombus

# Store all drawings
drawings = []

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mouse button down - start drawing
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
                last_pos = event.pos
                
                # For shapes that need start and end positions
                if current_tool in ["rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
                    drawings.append({
                        "type": current_tool,
                        "start_pos": event.pos,
                        "end_pos": event.pos,
                        "color": current_color,
                        "size": brush_size
                    })
        
        # Mouse button up - stop drawing
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                last_pos = None
        
        # Mouse motion - handle drawing
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                # Freehand drawing with pen
                if current_tool == "pen":
                    if last_pos:
                        drawings.append({
                            "type": "line",
                            "start_pos": last_pos,
                            "end_pos": event.pos,
                            "color": current_color,
                            "size": brush_size
                        })
                    last_pos = event.pos
                
                # Eraser (draws white lines)
                elif current_tool == "eraser":
                    if last_pos:
                        drawings.append({
                            "type": "line",
                            "start_pos": last_pos,
                            "end_pos": event.pos,
                            "color": WHITE,
                            "size": brush_size
                        })
                    last_pos = event.pos
                
                # Update end position for shapes
                elif current_tool in ["rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
                    if drawings and drawings[-1]["type"] == current_tool:
                        drawings[-1]["end_pos"] = event.pos
        
        # Keyboard input for tool selection and settings
        elif event.type == pygame.KEYDOWN:
            # Tool selection
            if event.key == pygame.K_p:
                current_tool = "pen"
            elif event.key == pygame.K_r:
                current_tool = "rectangle"
            elif event.key == pygame.K_c:
                current_tool = "circle"
            elif event.key == pygame.K_e:
                current_tool = "eraser"
            elif event.key == pygame.K_s:
                current_tool = "square"
            elif event.key == pygame.K_t:
                current_tool = "right_triangle"
            elif event.key == pygame.K_q:
                current_tool = "equilateral_triangle"
            elif event.key == pygame.K_h:
                current_tool = "rhombus"
            
            # Color selection
            elif event.key == pygame.K_1:
                current_color = BLACK
            elif event.key == pygame.K_2:
                current_color = RED
            elif event.key == pygame.K_3:
                current_color = GREEN
            elif event.key == pygame.K_4:
                current_color = BLUE
            elif event.key == pygame.K_5:
                current_color = YELLOW
            elif event.key == pygame.K_6:
                current_color = PURPLE
            elif event.key == pygame.K_7:
                current_color = CYAN
            
            # Brush size adjustment
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(50, brush_size + 1)
            elif event.key == pygame.K_MINUS:
                brush_size = max(1, brush_size - 1)
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw all elements
    for element in drawings:
        if element["type"] == "line":
            pygame.draw.line(screen, element["color"], element["start_pos"], element["end_pos"], element["size"])
        
        elif element["type"] == "rectangle":
            start_x = min(element["start_pos"][0], element["end_pos"][0])
            start_y = min(element["start_pos"][1], element["end_pos"][1])
            width = abs(element["end_pos"][0] - element["start_pos"][0])
            height = abs(element["end_pos"][1] - element["start_pos"][1])
            pygame.draw.rect(screen, element["color"], (start_x, start_y, width, height), element["size"])
        
        elif element["type"] == "circle":
            center_x = (element["start_pos"][0] + element["end_pos"][0]) // 2
            center_y = (element["start_pos"][1] + element["end_pos"][1]) // 2
            radius = int(math.sqrt((element["end_pos"][0] - element["start_pos"][0])**2 + 
                               (element["end_pos"][1] - element["start_pos"][1])**2) // 2)
            pygame.draw.circle(screen, element["color"], (center_x, center_y), radius, element["size"])
        
        elif element["type"] == "square":
            start_x = element["start_pos"][0]
            start_y = element["start_pos"][1]
            end_x = element["end_pos"][0]
            end_y = element["end_pos"][1]
            
            # Calculate side length as the minimum of width and height to maintain square proportions
            side = min(abs(end_x - start_x), abs(end_y - start_y))
            
            # Determine direction
            if end_x < start_x:
                start_x -= side
            if end_y < start_y:
                start_y -= side
                
            pygame.draw.rect(screen, element["color"], (start_x, start_y, side, side), element["size"])
        
        elif element["type"] == "right_triangle":
            start_x = element["start_pos"][0]
            start_y = element["start_pos"][1]
            end_x = element["end_pos"][0]
            end_y = element["end_pos"][1]
            
            # Points for right triangle (right angle at start position)
            points = [
                (start_x, start_y),
                (start_x, end_y),
                (end_x, end_y)
            ]
            pygame.draw.polygon(screen, element["color"], points, element["size"])
        
        elif element["type"] == "equilateral_triangle":
            start_x = element["start_pos"][0]
            start_y = element["start_pos"][1]
            end_x = element["end_pos"][0]
            end_y = element["end_pos"][1]
            
            # Calculate side length
            side = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            
            # Calculate height of equilateral triangle
            height = (math.sqrt(3)/2) * side
            
            # Calculate points
            points = [
                (start_x, start_y),
                (end_x, end_y),
                (start_x + (end_x - start_x)/2 - height*(end_y - start_y)/side, 
                 start_y + (end_y - start_y)/2 + height*(end_x - start_x)/side)
            ]
            pygame.draw.polygon(screen, element["color"], points, element["size"])
        
        elif element["type"] == "rhombus":
            start_x = element["start_pos"][0]
            start_y = element["start_pos"][1]
            end_x = element["end_pos"][0]
            end_y = element["end_pos"][1]
            
            # Calculate center point
            center_x = (start_x + end_x) / 2
            center_y = (start_y + end_y) / 2
            
            # Calculate vectors
            dx = end_x - start_x
            dy = end_y - start_y
            
            # Calculate perpendicular vector (for the other diagonal)
            perp_dx = -dy
            perp_dy = dx
            
            # Scale perpendicular vector to make a proper rhombus
            perp_length = math.sqrt(perp_dx**2 + perp_dy**2)
            if perp_length > 0:
                scale = math.sqrt(dx**2 + dy**2) / perp_length
                perp_dx *= scale
                perp_dy *= scale
            
            # Calculate the four points
            points = [
                (start_x, start_y),  # First corner
                (center_x + perp_dx/2, center_y + perp_dy/2),  # Second corner
                (end_x, end_y),  # Third corner
                (center_x - perp_dx/2, center_y - perp_dy/2)   # Fourth corner
            ]
            pygame.draw.polygon(screen, element["color"], points, element["size"])
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()