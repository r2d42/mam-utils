#!/usr/bin/env python4
import os
import sys
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# some configuration settings:
login_url = "https://www.myanonamouse.net/login.php"
username = os.environ.get("MAM_USERNAME")
password = os.environ.get("MAM_PASSWORD")
points_to_give = "1000"
bonus_cap = 20000


def open_browser():
    """
    instatiate the selenium webdriver
    """
    opts = Options()
    # change the following setting to False if you want to see the browser
    opts.headless = True

    return Firefox(options=opts)


def site_login():
    browser.get(login_url)
    cookies = browser.get_cookies()
    browser.find_element_by_name("email").send_keys(username)
    browser.find_element_by_name("password").send_keys(password)
    browser.find_element_by_class_name("btn").click()


def goto_homepage():
    browser.find_element_by_class_name("homeLink").click()
    time.sleep(1)


def get_bonus_points():
    """
    return bonus point integer
    """
    goto_homepage()
    bp = browser.find_element_by_id("tmBP")

    return int(bp.text.split()[1])


def get_new_members():
    """
    return a dictionary of usernames: urls
    """
    print("getting new members")
    goto_homepage()
    members_block = browser.find_element_by_id("fpNM")
    members = members_block.find_elements_by_tag_name("a")

    return {member.text: member.get_attribute("href") for member in members}


def give_points(member_username, member_url, points_to_give):
    """
    input:
      member_username = memeber name  (string)
      member_url = memeber page URL(string)
      points_to_give = point to give (integer)

    give the defined points to the user
    """
    print(f"giving {points_to_give} points to: {member_username}")
    browser.get(member_url)
    bg = browser.find_element_by_id("bonusgift")
    bg.clear()
    bg.send_keys(points_to_give)
    browser.find_element_by_id("sendPointsDetailP").click()
    time.sleep(1)
    sending = browser.find_elements_by_class_name("ui-button-text")
    sending[1].click()
    time.sleep(1)
    result = browser.find_element_by_class_name("ui-dialog-title").text
    print(f"{result} for user {member_username}")
    dialog = browser.find_elements_by_class_name("ui-button-text")
    dialog[1].click()
    time.sleep(1)


if __name__ == "__main__":

    # checking credential existance
    if username is None or password is None:
        print(
            "missing credentials"
            " please configure MAM_USERNAME and MAM_PASSWORD environment variables"
        )
        sys.exit(-1)

    print("open the browser session")
    browser = open_browser()
    print("opening browser and logging in MAM")
    site_login()
    print("checking bonus points")
    starting_bonus_points = get_bonus_points()
    print(f"starting bonus points = {starting_bonus_points}")

    if starting_bonus_points < bonus_cap:
        print(
            f"actual bonus points ({starting_bonus_points}) is under the "
            f"configured bonus cap ({bonus_cap})"
        )
        print("exiting")
        browser.close()
        sys.exit(-1)

    print("retriving new members list")
    members_dict = get_new_members()

    for member_username, member_url in members_dict.items():
        give_points(member_username, member_url, points_to_give)

    final_bonus_points = get_bonus_points()
    print(f"final bonous points={final_bonus_points}")

    browser.close()
