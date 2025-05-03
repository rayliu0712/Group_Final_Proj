import pygame
import thorpy

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    thorpy.init(screen)

    cards = [
        {"type": "Attack", "name": "Attack1", "color": (255, 100, 100)},
        {"type": "Attack", "name": "Attack2", "color": (255, 100, 100)},
        {"type": "Attack", "name": "Attack3", "color": (255, 100, 100)},
        {"type": "Attack", "name": "Attack4", "color": (255, 100, 100)},
        {"type": "Attack", "name": "Attack5", "color": (255, 100, 100)},
        {"type": "Defense", "name": "Defense1", "color": (100, 100, 255)},
        {"type": "Defense", "name": "Defense2", "color": (100, 100, 255)},
        {"type": "Defense", "name": "Defense3", "color": (100, 100, 255)},
        {"type": "Defense", "name": "Defense4", "color": (100, 100, 255)},
        {"type": "Defense", "name": "Defense5", "color": (100, 100, 255)},
        {"type": "Special", "name": "Special1", "color": (100, 255, 100)},
        {"type": "Special", "name": "Special2", "color": (100, 255, 100)},
    ]

    card_elements = []
    for card in cards:
        element = thorpy.make_text(f"{card['name']}\n({card['type']})", font_size=18)
        element.set_size((120, 80))
        element.set_main_color(card['color'])
        card_elements.append(element)

    rows = []
    for i in range(0, len(card_elements), 5):
        row = thorpy.Box()  # Initialize Box without 'elements' argument
        row.add_elements(card_elements[i:i+5])  # Add elements to the Box
        rows.append(row)

    back_button = thorpy.make_button("Back", func=lambda: print("Back clicked"))
    start_button = thorpy.make_button("Start", func=lambda: print("Start clicked"))
    button_row = thorpy.Box()
    button_row.add_elements([back_button, start_button])

    title = thorpy.Element(text="Card Deck")
    title.set_font_size(24)

    all_elements = [title] + rows + [button_row]
    main_box = thorpy.Box()
    main_box.add_elements(all_elements)
    main_box.set_position((50, 50))

    background = thorpy.Background(color=(240, 240, 240), elements=[main_box])

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            background.react(event)

        screen.fill((240, 240, 240))
        background.blit()
        background.update()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
