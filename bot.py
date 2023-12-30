from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains
import openai
import os
import requests
from dotenv import load_dotenv

driver = webdriver.Chrome()  # Or the appropriate driver for your browser
api_key = os.getenv('OPENAI_API_KEY')
load_dotenv()
driver.get("https://www.messenger.com/marketplace/")
openai.api_key = os.getenv('OPENAI_API_KEY')


email = "7788599320"
password = "Dickpickle2002"


try:
    # Wait for the email field to be interactable
    email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "email"))
    )

    # Send keys to the email field
    email_field.send_keys(email)

    print("email filled")

    pass_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pass"))
    )

    pass_field.send_keys(password)

    print("password filled")

    login_button = driver.find_element(By.ID, "loginbutton")

    login_button.click()

    print("logged in successfully")

except Exception as e:
    print(f"An error occurred: {e}")

time.sleep(3)

try:
    #element = WebDriverWait.until(EC.presence_of_element_located((By.ID, "mw-numeric-code-input-prevent-composer-focus-steal")))
    pin_input = driver.find_element(By.ID, "mw-numeric-code-input-prevent-composer-focus-steal")
    pin_input.send_keys(0)
    pin_input.send_keys(0)
    pin_input.send_keys(0)
    pin_input.send_keys(0)
    pin_input.send_keys(0)
    pin_input.send_keys(0)
except Exception as e:
    print("pin not required for some reason")

try:
    time.sleep(5)
    now_now_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Not now']")
    now_now_button.click()
    print("Security Cleared")

except NoSuchElementException as e:
    print("error trying to remember browser")


try:
    # Wait for elements (adjust the CSS selector as needed)
    WebDriverWait(driver, 10).until(
        #EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[aria-label='Mark as read']"))
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.x1nxh6w3'))
    )

    # Find elements for unread messages
    unread_messages = driver.find_elements(By.CSS_SELECTOR, '[style*="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 19.9995px;"]')


    print("Unread Messages:")
    for i in range(7):
        #unread_messages[i].click()
        action = ActionChains(driver)

        action.move_to_element_with_offset(unread_messages[i], -40, 0).click().perform()
        time.sleep(5)
        chat1 = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-color: var(--chat-incoming-message-bubble-background-color)')]")


        # Locating elements that match the second XPath
        chat2 = driver.find_elements(By.XPATH, "//*[contains(@style, 'background-color: rgb(10, 124, 255)')]")

        # Combining both lists of elements and remove duplicates
        chat = list(dict.fromkeys(chat1 + chat2))
        messages1 = []
        messages2 = []
        for i in chat1:
            messages1.append(i.text)
        for i in chat2:
            messages2.append(i.text)

        completion = openai.chat.completions.create(

            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot that replies to inquiries on facebook marketplace. \
                 You sell nicotine pouches, the brand ZYNS and XQS, ZYNS have 3 mg of nicotine, XQS has 4 mg, you must \
                 not sound like a chatbot, and give to-the-point responses. You will receive a block of text, which is all\
                 the text from the client, none from yourself, the second block of text, is what you already said \
                 make sure you don't repeat yourself and answer the question like a human. Common questions are, 'can you deliver' or \
                 how many mgs, in which you reply as consisely as possible. Once they have confirmed that they would like to \
                 purchase, send them this calendly link for them to book: https://calendly.com/evanwaang2020/30min. Any questions \
                 about the price should be redirected to the description of the listing, if they want to order more than 10, tell them it is $12 dollars each" },
                {"role": "user", "content": f"These are the messages from a customer {messages1}, these are the messages from me:\
                {messages2}, give a consise reply according to the last messages sent, these messages are actually going to be sent \
                therefore, do no have any [Insert here]'s in your response, use this calendly link if client agrees to purchase\
                 https://calendly.com/evanwaang2020/30min"}
            ]
            )
        

        print(completion.choices[0].message)


except Exception as e:
    print(f"An error occurred: {e}")


while True:
    pass

