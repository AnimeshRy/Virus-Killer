import sys
import pygame
from .bullet import Bullet
from .virus import Virus
from time import sleep


def check_keydown_events(event, st_settings, screen, stats, sanit, bullets):
    """Respond to keypresses."""

    if event.key == pygame.K_RIGHT:
        sanit.moving_right = True
    elif event.key == pygame.K_LEFT:
        sanit.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(st_settings, screen, sanit, bullets)
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_p:
        stats.game_active = True
        pygame.mixer.music.load('./music/bg.wav')
        pygame.mixer.music.play(-1)


def check_keyup_events(event, sanit):
    """Respoond to leaving key."""
    
    if event.key == pygame.K_RIGHT:
        sanit.moving_right = False
    elif event.key == pygame.K_LEFT:
        sanit.moving_left = False


def check_events(st_settings, screen, stats, play_button, sb, sanit, viruses, bullets):
    """Respond to key press and mouse"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # mouse.gte_pos() gets a tuple of the mouse's x and y coordinate values
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(st_settings, screen, stats,
                            play_button, sanit, sb, viruses, bullets, mouse_x, mouse_y)

        # each key is registered as a keydown
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, st_settings,
                                screen, stats, sanit, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, sanit)


def check_play_button(st_settings, screen, stats, play_button, sanit, sb, viruses, bullets, mouse_x, mouse_y):
    """ Start a new game when player click play
    - it checks if the mouse poistion is overlaping the the play_button rect
    - music load """
    
    pygame.mixer.music.load('./music/bg.wav')
    click_button = play_button.rect.collidepoint(mouse_x, mouse_y)

    if click_button and not stats.game_active:
        pygame.mixer.music.play(-1)

        # reset the game to level 1
        st_settings.initialize_dynamic_settings()

        # make the mouse not visible
        pygame.mouse.set_visible(False)

        # reset the game again
        stats.reset_stats()
        stats.game_active = True

        # reset everythings
        sb.prep_highscore()
        sb.prep_level()
        sb.prep_score()
        sb.prep_bottles()

        # empty the virus and bullets
        viruses.empty()
        bullets.empty()

        # make a new fleep and center the sanit
        create_fleet(st_settings, screen, sanit, viruses)
        sanit.center_bottle()


"""BULLET SECTION"""


def fire_bullets(st_settings, screen, sanit, bullets):
    """ Fire a bullet if limit not reached yet.
    - create a new bullet to add to the game when you press space and add it to the group 'bullets'
    - new functionality - limiting the number of bullets to keep the game optimized
    """

    if len(bullets) < st_settings.bullet_allowed:
        new_bullet = Bullet(st_settings, screen, sanit)
        bullets.add(new_bullet)


def bullet_update(st_settings, screen, sanit, sb, stats, viruses, bullets):
    """Update bullets and get rid of old bullets"""

    # update position of bullets
    bullets.update()

    # get rid of bullets that go out of the screen as they consume memory
    for bullet in bullets.copy():

        # iterate over a copy to not disturb the main list and remove the bullet from the group
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

            # print(len(bullets)) keep this intact to check for optimization

    # check for bullet collision with the virus group
    check_bullet_collisions(st_settings, screen, sanit,
                            sb, stats, viruses, bullets)


def check_bullet_collisions(st_settings, screen, sanit, sb, stats, viruses, bullets):

    # check if bullets have hit any virus
    # if so then get rid of the bullet and the alien
    # syntax used (REMEMBER) - groupcollide(group1, group2, dokill1, dokill2, collided = None)
    # make the dokill false if you want a bullet to not get removed

    collision = pygame.sprite.groupcollide(bullets, viruses, True, True)

    if collision:
        # looping through all the values as groupcollice returns a dict with key value pairs where one key(bullet) corresponds to
        # number of virus so len(viruses) would give out the len of all the virus a single bullet kills

        for viruses in collision.values():
            stats.score += st_settings.virus_hitpoint * len(viruses)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(viruses) == 0:

        # empty bullets when every virus is killed and speedup the game
        bullets.empty()
        st_settings.increase_speed()

        # increase game level
        stats.level += 1
        sb.prep_level()
        
        # if the number of virus are killed in one fleet, make another fleet and start over
        create_fleet(st_settings, screen, sanit, viruses)


"""BULLET SECTION"""
"""VIRUS SECTION"""


def get_number_viruses_x(st_settings, virus_width):
    # formula to fit virus as a row

    available_space_x = st_settings.screen_width - (2*virus_width)
    number_of_viruses_x = int(available_space_x/(2*virus_width))
    return number_of_viruses_x


def create_virus(st_settings, screen, viruses, virus_num, row_number):
    """create a virus after refactoring"""

    virus = Virus(st_settings, screen)
    virus_width = virus.rect.width

    # this algorithm gives space like this
    # x = 5 - 15 - 25 - 35 - 45 .. (if virus_width = 5)
    virus.x = virus_width + 2 * virus_width * virus_num
    virus.rect.x = virus.x
    virus.rect.y = virus.rect.height + 2 * virus.rect.height * row_number
    viruses.add(virus)


def get_number_rows(st_settings, sanitizer_height, virus_height):

    # 3/4 *virus_height changed!
    # We subtract the height of virus and sanitizer and divide by 2*virus because we are considereing one space below it too
    available_space_y = (st_settings.screen_height -
                        (4*virus_height) - sanitizer_height)
    number_rows = int(available_space_y/(2*virus_height))
    return number_rows


def create_fleet(st_settings, screen, sanit, viruses):
    """create a fleet of virus coming from top"""

    # create a virus and find the number of virus in a row
    # spacing between each virus is two times as we have to count the space after the virus too

    virus = Virus(st_settings, screen)
    number_virus_x = get_number_viruses_x(st_settings, virus.rect.width)
    number_rows = get_number_rows(
        st_settings, sanit.rect.height, virus.rect.height)

    # create the first row of virus
    for row_number in range(number_rows):
        for virus_num in range(number_virus_x):

            # creating a virus and pushing them to align them in a row and columns
            create_virus(st_settings, screen, viruses, virus_num, row_number)


def update_virus(st_settings, stats, screen, sb, sanit, viruses, bullets):
    """check if the virus is at the edge and then update it's new location"""

    check_fleet_edges(st_settings, viruses)
    # update all surfaces in the viruses group's position
    viruses.update()

    # look for collisions with virus and the bottle
    # collideany takes two arguments - sprite and a group

    if pygame.sprite.spritecollideany(sanit, viruses):
        bottle_hit(st_settings, stats, screen, sb, sanit, viruses, bullets)

    # check if the virus has hit the bottom
    check_virus_bottom(st_settings, stats, screen, sb, sanit, viruses, bullets)


def check_fleet_edges(st_settings, viruses):
    for virus in viruses.sprites():
        if virus.check_edges():
            change_fleet_direction(st_settings, viruses)
            break


def change_fleet_direction(st_settings, viruses):
    for virus in viruses.sprites():
        virus.rect.y += st_settings.fleet_drop_speed
    st_settings.fleet_direction *= -1


def check_virus_bottom(st_settings, stats, screen, sb, sanit, viruses, bullets):
    """check if the virus has reached the bottom"""

    screen_rect = screen.get_rect()
    for virus in viruses.sprites():
        # treat this the same as the bottle got hit
        if virus.rect.bottom >= screen_rect.bottom:
            bottle_hit(st_settings, stats, screen, sb, sanit, viruses, bullets)
            break


"""VIRUS SECTION"""


def update_screen(st_settings, screen, stats, sb, sanit, viruses, bullets, play_button):
    """Update images on the screen and flip on the new screen"""

    # redraw the screen everyloop
    screen.fill(st_settings.bg_color)

    # draw the score on the top right
    sb.show_score()

    # redraw all bullets behind the bottle
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # draw one surface on another
    sanit.blitme()

    # when you call draw on a group, it draws each element with positioning by rect attribute
    viruses.draw(screen)

    # draw the play button when the game is inactive
    # whenever we click on the button, this bool below turns false and the button is gone
    if not stats.game_active:
        play_button.draw_button()

    # make the most recently drawn screen visible
    pygame.display.flip()


"""Bottle section"""


def bottle_hit(st_settings, stats, screen, sb, sanit, viruses, bullets):
    """function defining what to do when the bottle is hit"""

    if stats.bottle_left > 0:
        stats.bottle_left -= 1

        sb.prep_bottles()
        
        # empty the list of viruses and bullets
        viruses.empty()
        bullets.empty()

        # create a new fleet and center the bottle again
        create_fleet(st_settings, screen, sanit, viruses)
        sanit.center_bottle()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """"check to see if there is a new score then replace it """

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_highscore()
