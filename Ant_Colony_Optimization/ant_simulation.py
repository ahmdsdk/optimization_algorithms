import math
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from graph import Graph
from ant import setAnt, setAntPopulationSurfaces
from colony_functions import generateTSAColony, getShortestPath, updatePheromoneMatrix

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MIN_PHEROMONE = 0.1

def createSlider(screen, x, y, min, max, step, value):
    slider = Slider(screen, x, y, 150, 10, min = min, max = max, step = step)
    slider_text = TextBox(screen, x + 65, y + 25, 90, 20, fontSize = 14, borderThickness = 1)
    slider.setValue(value)
    return slider, slider_text

def startSimulation():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ant Colony Optimization")
    colony_area_x = SCREEN_WIDTH - 250
    colony_area = pygame.Rect(0, 0, colony_area_x, SCREEN_HEIGHT)

    graph = Graph([], [])
    distanceMatrix = graph.distanceMatrix
    pheromoneMatrix = graph.pheromoneMatrix

    distances = []
    pos_list = []
    ant_surfaces = []

    font = pygame.font.Font(pygame.font.get_default_font(), 10)

    alpha_slider, alpha_slider_text = createSlider(screen, SCREEN_WIDTH - 200, 50, 1, 2, 0.1, 1.4)
    beta_slider, beta_slider_text = createSlider(screen, SCREEN_WIDTH - 200, 150, 1, 2, 0.1, 1.1)
    q_slider, q_slider_text = createSlider(screen, SCREEN_WIDTH - 200, 250, 1, 1000, 1, 100)
    population_slider, population_slider_text = createSlider(screen, SCREEN_WIDTH - 200, 350, 1, 5000, 1, 100)
    rho_slider, rho_slider_text = createSlider(screen, SCREEN_WIDTH - 200, 450, 0, 0.9, 0.1, 0.3)
    speed_slider, speed_slider_text = createSlider(screen, SCREEN_WIDTH - 200, 550, 1, 30, 1, 15)

    clear_button_x = SCREEN_WIDTH - 162.5
    clear_button_y = 650
    clear_button_width = 75
    clear_button_height = 25
    clear_button = pygame.Rect(clear_button_x, clear_button_y, clear_button_width, clear_button_height)
    clear_text = font.render("Clear", True, (0, 0, 0))

    is_line_length_shown = True
    show_hide_button_x = SCREEN_WIDTH - 162.5
    show_hide_button_y = 700
    show_hide_button_width = 75
    show_hide_button_height = 25
    show_hide_button = pygame.Rect(show_hide_button_x, show_hide_button_y, show_hide_button_width, show_hide_button_height)

    is_start_simulation = False
    start_simulation_button_x = SCREEN_WIDTH - 162.5
    start_simulation_button_y = 750
    start_simulation_button_width = 75
    start_simulation_button_height = 25
    start_simulation_button = pygame.Rect(start_simulation_button_x, start_simulation_button_y, start_simulation_button_width, start_simulation_button_height)

    population_size = population_slider.getValue()
    ant_surfaces = setAntPopulationSurfaces(population_size)

    average_distance = 0
    total_distances = []
    speed = 1

    pheromone_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(pheromone_timer, 2000)

    run = True
    while run:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), colony_area, 1)
        events = pygame.event.get()
        # set up events
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # pheronome update timer event
            if event.type == pheromone_timer and is_start_simulation:
                updatePheromoneMatrix(pheromoneMatrix, distanceMatrix, ant_surfaces, ro = rho_value, Q = q_value)

            # mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # add nodes
                if event.pos[0] < colony_area_x - 20 and not is_start_simulation:
                    pos_list.append(event.pos)
                    distanceMatrix = [[0 for i in range(len(pos_list))] for j in range(len(pos_list))]
                    pheromoneMatrix = [[0 for i in range(len(pos_list))] for j in range(len(pos_list))]

                # clear nodes
                elif not is_start_simulation and event.pos[0] > clear_button_x and event.pos[0] < clear_button_x + clear_button_width and event.pos[1] > clear_button_y and event.pos[1] < clear_button_y + clear_button_height:
                    ant_surfaces = setAntPopulationSurfaces(population_size)
                    pos_list.clear()
                    total_distances.clear()
                    distances.clear()

                # show/hide line length
                elif event.pos[0] > show_hide_button_x and event.pos[0] < show_hide_button_x + show_hide_button_width and event.pos[1] > show_hide_button_y and event.pos[1] < show_hide_button_y + show_hide_button_height:
                    is_line_length_shown = not is_line_length_shown

                # start/stop simulation
                elif len(pos_list) > 1 and event.pos[0] > start_simulation_button_x and event.pos[0] < start_simulation_button_x + start_simulation_button_width and event.pos[1] > start_simulation_button_y and event.pos[1] < start_simulation_button_y + start_simulation_button_height:
                    total_distances.clear()
                    population_size = population_slider.getValue()
                    ant_surfaces = setAntPopulationSurfaces(population_size)
                    for i in range(len(ant_surfaces)):
                        ant = ant_surfaces[i]
                        surface, is_generated, position_node, ant_position, path, did_finish, did_update_pheromone = ant.__getall__()
                        ant_x_position = pos_list[0][0]
                        ant_y_position = pos_list[0][1]
                        ant_position = (ant_x_position, ant_y_position)
                        ant.ant_position = ant_position
                    is_start_simulation = not is_start_simulation

        # draw lines
        for i in range(len(pos_list)):
            for j in range(len(pos_list)):
                if i == j and not is_start_simulation:
                    distanceMatrix[i][j] = 0
                    pheromoneMatrix[i][j] = 0
                if i != j:
                    dx = pos_list[i][0] - pos_list[j][0]
                    dy = pos_list[i][1] - pos_list[j][1]
                    # b = sqrt(a^2 + c^2)
                    line_length = round(math.sqrt(dx**2 + dy**2), 1)
                    distances.append(line_length)
                    if not is_start_simulation:
                        distanceMatrix[i][j] = line_length
                        pheromoneMatrix[i][j] = MIN_PHEROMONE
                    line_color = (125, 125, 125, 100) if pheromoneMatrix[i][j] <= MIN_PHEROMONE else (0, 255, 0)
                    width = 1 + round(pheromoneMatrix[i][j]) if pheromoneMatrix[i][j] <= MIN_PHEROMONE else 2 + round(pheromoneMatrix[i][j])
                    pygame.draw.line(screen, line_color, pos_list[i], pos_list[j], width)
                    if is_line_length_shown:
                        text_surface = font.render(f"{line_length} km", True, (125, 125, 125))
                        screen.blit(text_surface, ((pos_list[i][0] + pos_list[j][0]) / 2, (pos_list[i][1] + pos_list[j][1]) / 2))
                        text_surface = font.render(f"{round(pheromoneMatrix[i][j], 2)}", True, (0, 255, 0))
                        screen.blit(text_surface, ((pos_list[i][0] + pos_list[j][0]) / 2, ((pos_list[i][1] + pos_list[j][1]) / 2) + 10))

        # draw nodes
        for i in range(len(pos_list)):
            x, y = pos_list[i]
            if i == 0:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, 15, 15), border_radius = 10)
            else:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(x, y, 15, 15), border_radius = 10)
            node_font = pygame.font.Font(pygame.font.get_default_font(), 10)
            node_text_surface = node_font.render(f"{i}", True, (0, 0, 0) if i == 0 else (255, 255, 255))
            screen.blit(node_text_surface, (pos_list[i][0] + 5, pos_list[i][1] + 2))

        # print total distances
        if is_start_simulation and len(total_distances) > 0:
            y = 0
            x = 0
            total_distance, path = total_distances[len(total_distances) - 1]
            i = len(total_distances) - 1
            text_surface = font.render(f"All {i} ants best path: {path} shortest distance: {total_distance}" if i == len(ant_surfaces) else f"Ant {i} path: {path} covered distance: {total_distance}", True, (0, 0, 0))
            screen.blit(text_surface, (10, 30))

        # print average distance
        if len(distances) > 0:
            average_distance = round(sum(distances) / len(distances), 2)
            text_surface = font.render(f"Average distance = {round(average_distance)}", True, (0, 0, 0))
            screen.blit(text_surface, (10, 10))

        alpha_slider_text.setText(f"alpha value: {round(alpha_slider.getValue(), 1)}")
        beta_slider_text.setText(f"beta value: {round(beta_slider.getValue(), 1)}")
        population_slider_text.setText(f"population: {population_slider.getValue()}")
        q_slider_text.setText(f"Q value: {round(q_slider.getValue())}")
        q_value = q_slider.getValue()
        rho_slider_text.setText(f"rho value: {round(rho_slider.getValue(), 1)}")
        rho_value = rho_slider.getValue()
        speed_slider_text.setText(f"speed: {round(speed_slider.getValue())}")
        speed = speed_slider.getValue()

        pygame.draw.rect(screen, (255, 0, 125), clear_button, border_radius = 15)
        screen.blit(clear_text, (clear_button_x + (clear_button_width / 2) - clear_text.get_width() / 2, clear_button_y + (clear_button_height / 2) - clear_text.get_height() / 2))

        show_hide_text = font.render("Hide" if is_line_length_shown else "Show", True, (0, 0, 0))
        show_hide_text_position = (show_hide_button_x + (show_hide_button_width / 2) - show_hide_text.get_width() / 2, show_hide_button_y + (show_hide_button_height / 2) - show_hide_text.get_height() / 2)
        pygame.draw.rect(screen, (255, 125, 125), show_hide_button, border_radius = 15)
        screen.blit(show_hide_text, show_hide_text_position)

        start_simulation_text = font.render("Start" if not is_start_simulation else "Stop", True, (0, 0, 0))
        start_simulation_text_position = (start_simulation_button_x + (start_simulation_button_width / 2) - start_simulation_text.get_width() / 2, start_simulation_button_y + (start_simulation_button_height / 2) - start_simulation_text.get_height() / 2)
        pygame.draw.rect(screen, (0, 255, 0), start_simulation_button, border_radius = 15)
        screen.blit(start_simulation_text, start_simulation_text_position)

        # start simulation
        if is_start_simulation:
            # loop over all ants
            for i in range(len(ant_surfaces)):
                ant = ant_surfaces[i]
                surface, is_generated, position_node, ant_position, path, did_finish, did_update_pheromone = ant.__getall__()
                ant_x_position, ant_y_position = ant_position
                # create new path if ant is not generated
                if not is_generated:
                    path = generateTSAColony(distanceMatrix, pheromoneMatrix, Q = q_value, ro = rho_value, alpha = alpha_slider.getValue(), beta = beta_slider.getValue())
                    path.append(0)
                    ant.is_generated = True
                    ant.path = path
                    total_distance = 0
                    for sp in range(len(path) - 1):
                        total_distance += distanceMatrix[path[sp]][path[sp + 1]]
                    total_distances.append((round(total_distance, 2), path))
                # move ant to next node until path is finished
                if not did_finish:
                    if position_node < len(path) - 1:
                        node_j = path[position_node + 1]
                        dx, dy = (pos_list[node_j][0] - ant_x_position, pos_list[node_j][1] - ant_y_position)
                        stepx, stepy = (speed *  dx / 30, speed *  dy / 30)
                        ant_x_position += stepx
                        ant_y_position += stepy
                        # theta = tan^-1(dy / dx)
                        angle_to_rotate = round(math.degrees(math.atan(dy / dx)), 0) if dx != 0 else 0
                        surface = setAnt(-90 -angle_to_rotate if dx > 0 else -90 -angle_to_rotate + 180).surface
                        ant_position = (ant_x_position, ant_y_position)
                        ant.ant_position = ant_position
                        ant.surface = surface
                        ant.draw(screen)
                        if ant_x_position <= pos_list[node_j][0] + 5 and ant_x_position >= pos_list[node_j][0] - 5 and ant_y_position <= pos_list[node_j][1] + 5 and ant_y_position >= pos_list[node_j][1] - 5:
                            position_node += 1
                            ant.position_node = position_node
                    else:
                        did_finish = True
                        ant.did_finish = did_finish
                        if i == len(ant_surfaces) - 1:
                            shortest_path = getShortestPath(pheromoneMatrix, 0, [])
                            shortest_path.append(0)
                            total_distance = 0
                            for sp in range(len(shortest_path) - 1):
                                total_distance += distanceMatrix[shortest_path[sp]][shortest_path[sp + 1]]
                            total_distances.append((round(total_distance, 2), shortest_path))
                    if (i + 1) % 10 == 0:
                        break
                # if not did_finish:
                #     ant.draw(screen)
                #     break

        pygame_widgets.update(events)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

startSimulation()