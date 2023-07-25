import pygame
from datetime import datetime, timedelta
import math
import pytz

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((600, 400))

# Set font
font = pygame.font.Font(None, 36)

locations = [['Amsterdam','Netherlands',4.895168, 'Europe/Amsterdam'],
['Bangkok','Thailand',100.501765, 'Asia/Bangkok'],
['Beijing','China',116.407396, 'Asia/Shanghai'],
['Berlin','Germany',13.404954, 'Europe/Berlin'],
['Buenos Aires','Argentina',-58.381559, 'America/Argentina/Buenos_Aires'],
['Cairo','Egypt',31.235712, 'Africa/Cairo'],
['Chicago','USA',-87.629798, 'America/Chicago'],
['Delhi','India',77.216721, 'Asia/Kolkata'],
['Dubai','UAE',55.270783, 'Asia/Dubai'],
['Hong Kong','China',114.109497, 'Asia/Hong_Kong'],
['Istanbul','Turkey',28.978359, 'Europe/Istanbul'],
['Jakarta','Indonesia',106.845599, 'Asia/Jakarta'],
['Lisbon','Portugal',-9.139337, 'Europe/Lisbon'],
['London','UK',-0.127758, 'Europe/London'],
['Los Angeles','USA',-118.243685, 'America/Los_Angeles'],
['Madrid','Spain',-3.703790, 'Europe/Madrid'],
['Mexico City','Mexico',-99.133208, 'America/Mexico_City'],
['Moscow','Russia',37.617300, 'Europe/Moscow'],
['Mumbai','India',72.877656, 'Asia/Kolkata'],
['New York','USA',-74.005941, 'America/New_York'],
['Paris','France',2.352222, 'Europe/Paris'],
['Rio de Janeiro','Brazil',-43.172896, 'America/Sao_Paulo'],
['Rome','Italy',12.496366, 'Europe/Rome'],
['San Francisco','USA',-122.419416, 'America/Los_Angeles'],
['Sao Paulo','Brazil',-46.633309, 'America/Sao_Paulo'],
['Seoul','South Korea',126.977969,'Asia/Seoul' ],
['Shanghai','China',121.473701,'Asia/Shanghai' ],
['Singapore','Singapore',103.819836,'Asia/Singapore' ],
['Sydney','Australia',151.209296,'Australia/Sydney' ],
['Tokyo','Japan',139.691706,'Asia/Tokyo']]

def solar_time(longitude, date, local_time):
    # Calculate the difference between the local time zone and UTC
    tz_offset = datetime.now().astimezone().utcoffset().total_seconds() / 3600
    
    # Calculate the equation of time
    day_of_year = date.timetuple().tm_yday
    b = (360 / 365.24) * (day_of_year - 81)
    eot = 9.87 * math.sin(math.radians(2 * b)) - 7.53 * math.cos(math.radians(b)) - 1.5 * math.sin(math.radians(b))
    
    # Calculate the time correction factor
    tc = 4 * (longitude - 15 * tz_offset) + eot
    
    # Calculate the local solar time
    lst = datetime.combine(date, local_time) + timedelta(minutes=tc)
    
    return lst

def format_time(time, decimal_places):
    hours, remainder = divmod(time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    format_str = "{:02.0f}:{:02.0f}:{:0" + str(3 + decimal_places) + "." + str(decimal_places) + "f}"
    return format_str.format(hours, minutes, seconds)


def draw_text(text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text_surface, text_rect)

def settings_page(screen_size, time_format, decimal_places):
    # Initialize Pygame
    pygame.init()

    # Set screen size
    screen = pygame.display.set_mode(screen_size)

    # Set initial value for mouse button release flag
    mouse_released = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle mouse button release
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw settings page
        draw_text("Settings", 300, 50, screen)

        draw_text("Window Size", 150, 100, screen)
        draw_text(str(screen_size[0]) + " x " + str(screen_size[1]), 450, 100, screen)

        draw_text("Time Format", 150, 150, screen)
        draw_text(time_format.capitalize(), 450, 150, screen)

        draw_text("Decimal Places", 150, 200, screen)
        draw_text(str(decimal_places), 450, 200, screen)

        draw_text("Back", 50, 350, screen)

        # Check if back button is clicked
        if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] < 100 and pygame.mouse.get_pos()[1] > 300 and mouse_released:
            return (screen_size,time_format,decimal_places)
            mouse_released = False

        # Check if window size is clicked
        elif pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] > 80 and pygame.mouse.get_pos()[1] <120 and mouse_released:
            if screen_size == (600,400):
                screen_size = (800,600)
            else:
                screen_size = (600,400)
            screen = pygame.display.set_mode(screen_size)
            mouse_released = False

        # Check if time format is clicked
        elif pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] >130 and pygame.mouse.get_pos()[1] <170 and mouse_released:
            if time_format == "digital":
                time_format = "analog"
            else:
                time_format = "digital"
            mouse_released = False

        # Check if decimal places is clicked
        elif pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[1] >180 and pygame.mouse.get_pos()[1] <220 and mouse_released:
            decimal_places +=1 
            if decimal_places >3:
                decimal_places=0 
            mouse_released=False

        # Update screen
        pygame.display.flip()

def scroll(scroll_position, scroll_speed):
    # Set maximum and minimum scroll position
    max_scroll_position = 0
    min_scroll_position = -1000
    
    # Update scroll position based on scroll speed
    scroll_position += scroll_speed
    
    # Limit scroll position to maximum and minimum values
    if scroll_position > max_scroll_position:
        scroll_position = max_scroll_position
    elif scroll_position < min_scroll_position:
        scroll_position = min_scroll_position
    
    # Update scroll speed
    if scroll_speed > 0:
        scroll_speed -= 1
    elif scroll_speed < 0:
        scroll_speed += 1
    
    return (scroll_position, scroll_speed)

def draw_clock(center_x, center_y, radius, hours, minutes, seconds):
    # Draw clock face
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 1)
    
    # Draw hour hand
    hour_angle = math.pi / 2 - (hours + minutes / 60 + seconds / 3600) * math.pi / 6
    hour_x = center_x + int(radius * 0.6 * math.cos(hour_angle))
    hour_y = center_y - int(radius * 0.6 * math.sin(hour_angle))
    pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (hour_x, hour_y), 2)
    
    # Draw minute hand
    minute_angle = math.pi / 2 - (minutes + seconds / 60) * math.pi / 30
    minute_x = center_x + int(radius * 0.8 * math.cos(minute_angle))
    minute_y = center_y - int(radius * 0.8 * math.sin(minute_angle))
    pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (minute_x, minute_y), 2)
    
    # Draw second hand
    second_angle = math.pi / 2 - seconds * math.pi / 30
    second_x = center_x + int(radius * 0.9 * math.cos(second_angle))
    second_y = center_y - int(radius * 0.9 * math.sin(second_angle))
    pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (second_x, second_y), 1)

    
def main(screen_size):
    global screen,font
    clock = pygame.time.Clock()
    
    # Set initial values for selected country, scroll position, and scroll speed
    selected_country = None
    scroll_position = 0
    scroll_speed = 0
    
    # Set initial value for mouse button release flag
    mouse_released = True
    
    # Set initial values for settings
    time_format = "digital"
    decimal_places = 0
    
    # Set initial value for settings page flag
    show_settings_page = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Handle mouse wheel scrolling
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_speed -= 20
                elif event.button == 5:
                    scroll_speed += 20
            
            # Handle mouse button release
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True
        
        # Update scroll position and speed
        (scroll_position, scroll_speed) = scroll(scroll_position, scroll_speed)
        
        # Get current date and time
        date = datetime.now().date()
        local_time = datetime.now().time()
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        if show_settings_page:
            # Draw settings page
            draw_text("Settings", screen_size[0] // 2, screen_size[1] // 8)
            
            draw_text("Window Size", screen_size[0] // 4, screen_size[1] // 4)
            draw_text(str(screen_size[0]) + " x " + str(screen_size[1]), screen_size[0] * 3 // 4, screen_size[1] // 4)
            
            draw_text("Time Format", screen_size[0] // 4, screen_size[1] * 3 // 8)
            draw_text(time_format.capitalize(), screen_size[0] * 3 // 4, screen_size[1] * 3 // 8)
            
            draw_text("Decimal Places", screen_size[0] // 4, screen_size[1] // 2)
            draw_text(str(decimal_places), screen_size[0] * 3 // 4, screen_size[1] // 2)
            
            draw_text("Back", screen_size[0] // 10, screen_size[1] * 7 // 8)
            
                        # Check if back button is clicked
            if (pygame.mouse.get_pressed()[0]
                    and pygame.mouse.get_pos()[0] < screen_size[0] // 5 
                    and pygame.mouse.get_pos()[1] > screen_size[1] * 3 // 4 
                    and mouse_released):
                show_settings_page = False
                mouse_released = False
            
            # Check if window size is clicked
            elif (pygame.mouse.get_pressed()[0]
                    and pygame.mouse.get_pos()[1] > screen_size[1] // 4 - 20 
                    and pygame.mouse.get_pos()[1] < screen_size[1] // 4 + 20 
                    and mouse_released):
                if screen_size == (600,400):
                    screen_size = (800,600)
                    font = pygame.font.Font(None, 50)
                elif screen_size == (800,600):
                    screen_size = (1200,1000)
                    font = pygame.font.Font(None, 55)
                else:
                    screen_size = (600,400)
                    font = pygame.font.Font(None, 36)
                screen = pygame.display.set_mode(screen_size)
                mouse_released = False
            
            # Check if time format is clicked
            elif (pygame.mouse.get_pressed()[0]
                    and pygame.mouse.get_pos()[1] > screen_size[1] * 3 // 8 - 20 
                    and pygame.mouse.get_pos()[1] < screen_size[1] * 3 // 8 + 20 
                    and mouse_released):
                if time_format == "digital":
                    time_format = "analog"
                else:
                    time_format = "digital"
                mouse_released = False
            
            # Check if decimal places is clicked
            elif (pygame.mouse.get_pressed()[0]
                    and pygame.mouse.get_pos()[1] > screen_size[1] // 2 - 20 
                    and pygame.mouse.get_pos()[1] < screen_size[1] // 2 + 20 
                    and mouse_released):
                decimal_places +=1 
                if decimal_places >3:
                    decimal_places=0 
                mouse_released=False
                
        elif selected_country is None:
            # Draw country stack
            y = screen_size[1] // 8 + scroll_position
            for location in locations:
                city, country, longitude, timezone = location
                
                # Check if country is clicked
                if (pygame.mouse.get_pressed()[0]
                        and y - 20 < pygame.mouse.get_pos()[1] < y + 20
                        and mouse_released
                        and pygame.mouse.get_pos()[0]<screen_size[0]*5//6):
                    selected_country = location
                    mouse_released = False
                
                draw_text(city + ", " + country, screen_size[0] // 2, y)
                y += 40
            
            # Draw scroll instructions
            draw_text("Scroll to see", 75, screen_size[1] * 7 // 8)
            draw_text("more countries", 100, screen_size[1] * 7 // 8+30)
            # Draw settings button
            draw_text("Settings", screen_size[0] * 9 // 10, screen_size[1] * 7 // 8)
            
            # Check if settings button is clicked
            if (pygame.mouse.get_pressed()[0]
                    and pygame.mouse.get_pos()[0]>screen_size[0]*4//5
                    and pygame.mouse.get_pos()[1]>screen_size[1]*3//4
                    and mouse_released):
                show_settings_page=True 
                mouse_released=False
                
        else:
            city, country, longitude, timezone = selected_country
            
            # Calculate solar time and UTC time for selected country
            solar_time_dt = solar_time(longitude, date, local_time)
            utc_time_str = datetime.utcnow().strftime("%H:%M:%S")
            
            # Convert UTC time to local time for selected country
            tz = pytz.timezone(timezone)
            local_time_str = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz).strftime("%H:%M:%S")
            
            # Format solar time with specified number of decimal places for seconds
            solar_time_str = solar_time_dt.strftime("%H:%M:%S")
            if decimal_places > 0:
                solar_time_str += ".{:0>{}}".format(solar_time_dt.microsecond // (10 ** (6 - decimal_places)), decimal_places)
            
            # Draw text
            draw_text(city + ", " + country, screen_size[0] // 2, screen_size[1] // 8)
            
            if time_format == "digital":
                draw_text("Solar Time", screen_size[0] // 4, screen_size[1] // 4)
                draw_text(solar_time_str, screen_size[0] // 4, screen_size[1] * 3 // 8)
                draw_text("Local Time", screen_size[0] * 3 // 4, screen_size[1] // 4)
                draw_text(local_time_str, screen_size[0] * 3 // 4, screen_size[1] * 3 // 8)
                
            else:
                # Draw solar time clock
                draw_text("Solar Time", screen_size[0] // 4, screen_size[1] // 4)
                solar_time_dt = solar_time(longitude, date, local_time)
                draw_clock(screen_size[0] // 4, screen_size[1] * 3 // 8, min(screen_size) // 6, solar_time_dt.hour, solar_time_dt.minute, solar_time_dt.second)
                
                # Draw local time clock
                draw_text("Local Time", screen_size[0] * 3 // 4, screen_size[1] // 4)
                tz = pytz.timezone(timezone)
                local_time_dt = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz)
                draw_clock(screen_size[0] * 3 // 4, screen_size[1] * 3 // 8, min(screen_size) // 6, local_time_dt.hour, local_time_dt.minute, local_time_dt.second)

            
            # Draw back button
            draw_text("Back", screen_size[0] // 10, screen_size[1] * 7 // 8)
            
            # Check if back button is clicked
            if (pygame.mouse.get_pressed()[0]
                    and pygame.mouse.get_pos()[0] < screen_size[0] // 5 
                    and pygame.mouse.get_pos()[1] > screen_size[1] * 3 // 4 
                    and mouse_released):
                selected_country = None
                mouse_released = False
        
        # Update screen
        pygame.display.flip()
        
        clock.tick(30)


if __name__ == "__main__":
    main((600,400))

