import logging
from datetime import date
from random import randint
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import random
from configuration import Configuration
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Configuration.init_config("./config.ini")
file_path = Configuration.get('input', 'input_file_name')
sheet_name = Configuration.get('input', 'sheet_name')
logging.basicConfig(filename="logfilename" + date.today().__str__().replace(" ", "").replace(':', '') + ".log",
                    level=logging.INFO)

f = [i.strip('\n').split(' ') for i in open(Configuration.get('input', 'USER_CREDENTIAL'))]
number = int(Configuration.get('input', 'user'))
i_d = f[number - 1][0]
password = f[number - 1][1]
email = f[number - 1][2]

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options)

# driver.minimize_window()
# opens Chrome on Twitter's login page


driver.get("https://twitter.com/i/flow/login")

sign_in_xpath = "//*[@id="'react-root'"]/div/div/div/main/div/div/div/div[1]/div/div[3]/div[4]/span/span"

email_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]/div/input'

verify_email_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[' \
                     '1]/div/div[2]/label/div/div[2]/div/input'

vnext_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div'

next_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]/div/span/span'

password_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input'

login_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div'

time.sleep(5)  # It will wait for laoding page

driver.find_element(By.XPATH, email_xpath).send_keys(i_d)
time.sleep(3.0)
driver.find_element(By.XPATH, next_xpath).click()
time.sleep(2.0)

try:
    driver.find_element(By.XPATH, verify_email_xpath).send_keys(email)
    time.sleep(2.0)
    driver.find_element(By.XPATH, vnext_xpath).click()
    time.sleep(2.0)
except:
    pass
time.sleep(2.0)

driver.find_element(By.XPATH, password_xpath).send_keys(password)
time.sleep(2.0)
driver.find_element(By.XPATH, login_xpath).click()

tweet_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[' \
              '1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[' \
              '2]/div/div/div/div '
message_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[' \
                '1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[' \
                '2]/div/div/div/div '
post_tweet_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[' \
                   '1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div '
random_click_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[' \
                     '2]/div[1]/div/div/div/div/div/div/div/div[3]/div[2]/div/div/div[1] '
force_click_tweet = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[' \
                    '1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span '
time.sleep(10)

xl = pd.ExcelFile(file_path)
df = xl.parse(sheet_name, usecols=['username', 'handle'])

# tweet = "Hey!"
names_list = df["username"].tolist()
handle_list = df["handle"].tolist()

count = int(Configuration.get('input', 'start_from'))
# for (handle, name) in zip(handle_list, names_list):
#     proper_name = name
#     user_handle = handle
if int(Configuration.get('input', 'end')) < len(handle_list):
    end_of_loop = int(Configuration.get('input', 'end'))
else:
    end_of_loop = int(len(handle_list))


handle_from = int(Configuration.get('input', 'start_from'))-1
handle_till = handle_from+int(Configuration.get('input', 'handle'))
for i in range(int(Configuration.get('input', 'start_from')), int(end_of_loop)):
    proper_name = names_list[i - 1]

    user_handle = handle_list[handle_from: handle_till]
    listToStr = ' '.join([str(elem) for elem in user_handle])
    handle_from = handle_till
    handle_till = handle_till + int(Configuration.get('input', 'handle'))

    tweets = open('tweets.txt', 'r')
    Lines = tweets.readlines()
    random_tweet = random.choice(Lines)

    time.sleep(5.0)
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, tweet_xpath)))
        time.sleep(2.0)
        element.click()
    except:
        pass
    time.sleep(1.0)
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, tweet_xpath)))
        time.sleep(2.0)
        element.click()
    except:
        pass

    # driver.find_element(By.XPATH, tweet_xpath).click()
    time.sleep(2.0)
    try:
        driver.find_element(By.XPATH, message_xpath).send_keys(random_tweet, "\n", listToStr, Keys.ENTER)
        time.sleep(2.0)
    except:
        pass
    ############################################# media ##############################################################

    media_list = open("D:/_Codes/rario/amelia & olivia/media").readlines()

    media = random.choice(media_list)
    media_path = media.strip('\n').replace('\'', '/')
    try:
        image_path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[' \
                     '1]/div/div/div/div[2]/div[3]/div/div/div[1]/input '
        # image = 'C:/Users/Ashish/PycharmProjects/Twitter Automation/Thanks.jpg'
        driver.find_element(By.XPATH, image_path).send_keys(media_path)
        time.sleep(12.0)
    except:
        pass

    ############################################################################################################
    try:
        driver.find_element(By.XPATH, random_click_xpath).click()
        time.sleep(2.0)
    except:
        pass
    time.sleep(2.0)
    try:
        driver.find_element(By.XPATH, post_tweet_xpath).click()
    except:
        pass

    time.sleep(5.0)

    count += 1
    logging.info(
        'Posted: ' + str(handle_till - int(Configuration.get('input', 'handle'))) + '     To: ' + str(user_handle))

    # print('--------------Report----------------')
    print(
        'Posted Tweet: ' + str(handle_till - int(Configuration.get('input', 'handle'))) + '    To: ' + str(user_handle))

    time.sleep(
        randint(int(Configuration.get('input', 'time_delay_1')), int(Configuration.get('input', 'time_delay_2'))))
    time.sleep(10.0)
    end_of_loop = int(handle_till - int(Configuration.get('input', 'handle')))
