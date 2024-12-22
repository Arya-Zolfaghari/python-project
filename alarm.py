# Python alarm clock
import time
import datetime
import pygame 


def set_alarm(alarm_time):
          print(f"Alarm set for {alarm_time}")
          sound_file = "C:/Users/Arya/OneDrive/Dokumente/python/sound/alarm.wav"
          is_running = True
          
          while is_running:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(current_time)



                    if current_time == alarm_time:
                              print(" Wake Up !! 🥱")
                              
                              pygame.mixer.init()
                              pygame.mixer.music.load(sound_file)
                              pygame.mixer.music.play()
                              
                              
                              while pygame.mixer.music.get_busy():
                                        time.sleep(1)
                                        
                              
                              is_running = False
                    
                    
                    time.sleep(1)




if __name__ == "__main__":
          alarm_time = input("Enter the time of alarm to be set:  HH:MM:SS :   \n")

          set_alarm(alarm_time)
