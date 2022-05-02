from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os

single_player = True

# Load add-blocker plugin, not playing with ads.
chrome_options = Options()
chrome_options.add_extension('extensions/uBlock-Origin.crx')

# Open controlled browser
driver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
# driver.implicitly_wait(1)
driver.maximize_window()
driver.get('https://colonist.io/')
driver.find_element_by_xpath("//*[contains(text(), 'Find Game')]").click()

if single_player:
    driver.find_elements_by_class_name("matchmaking_option_item_content")[0].click()
else:
    driver.find_elements_by_class_name("matchmaking_option_item_content")[1].click()

while len(driver.find_elements_by_class_name("game_chat_text_div")) is 0:
    time.sleep(1)

start = datetime.now()
print(f"Game started: {start}")

while len(driver.find_elements_by_class_name("chartjs-render-monitor")) is 0:
    # print("Not found: chartjs-render-monitor")
    time.sleep(1)

end = datetime.now()
print(f"Game ended: {end}")

chat_html = driver.find_element_by_class_name("game_chat_text_div").get_attribute('innerHTML')

if not os.path.exists('data'):
    os.makedirs('data')

save_filename = os.path.join('data', f'{end.strftime("%Y%m%d-%H%M%S")}.txt')
with open(save_filename, 'w') as f:
    f.write(chat_html)
    f.write(str((end - start).total_seconds()))
    print(f"Saved chat in: {save_filename}")

time.sleep(5)
driver.quit()
