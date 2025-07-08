# main.py

import time
from turtle import clear
import warnings
import random
import json
import os
import logging
import sys

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utility import chd_wh, clear_console, word_get, choice_class, choice_set
from learning_types import (
    memorization,
    recall,
    spelling,
    test,
    matching_game
)

a = input(
    """
    -------------------------------------------------EULA----------------------------------------------------
    이 프로그램은 교육용 목적으로 만들어졌습니다. 절대 실제 수업에서의 사용을 금지합니다. 모든 책임은 사용자에게 있습니다.
    계속하시겠습니까? (y/n): 
    """
    )

if a == "n":
    print("프로그램을 종료합니다.")
    quit()

clear_console()

print(
        """

        -----------------------------------
        Classcard Hack v3.1.2
        -----------------------------------

        Developed by NellLucas(서재형)
        Fixed by SD HS Student

        몇가지 오류 메세지, 로그가 떠도 무시해주세요.

        """
)

time.sleep(2)

# 경고 및 로그 suppress
warnings.filterwarnings("ignore")
logging.getLogger('selenium').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--log-level=3')  # 오류만 출력

# 드라이버 생성 (로그 파일도 버림)
original_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")
service = Service(log_path=os.devnull)
driver = webdriver.Chrome(options=chrome_options, service=service)
sys.stdout.close()
sys.stdout = original_stdout

# 수동 로그인 안내
print("로그인 페이지가 열리면 아이디와 비밀번호를 직접 입력하고 로그인 버튼을 눌러주세요.")
driver.get("https://www.classcard.net/Login")

# 로그인 완료를 URL 변경으로 자동 감지
print("로그인 완료를 기다리는 중...")
try:
    WebDriverWait(driver, 60).until(
        lambda driver: driver.current_url != "https://www.classcard.net/Login" and "Login" not in driver.current_url
    )
    print("로그인이 완료되었습니다. 단어장 선택 페이지로 이동합니다. 잠시 기다려주세요...")
except TimeoutException:
    print("로그인 대기 시간이 초과되었습니다. 프로그램을 종료합니다.")
    driver.quit()
    quit()

def main():
    # account = get_id()  # 삭제
    
    time_1 = round(random.uniform(0.7, 1.3), 4)
    time_2 = round(random.uniform(1.7, 2.3), 4)

    try:

        class_dict = {}
        class_list_element = driver.find_element(
            By.CSS_SELECTOR,
            "body > div.mw-1080 > div:nth-child(6) > div > div > div.left-menu > div.left-item-group.p-t-none.p-r-lg > div.m-t-sm.left-class-list",
        )
        for class_item, i in zip(
            class_list_element.find_elements(By.TAG_NAME, "a"),
            range(len(class_list_element.find_elements(By.TAG_NAME, "a"))),
        ):
            class_temp = {}
            class_temp["class_name"] = class_item.text
            href = class_item.get_attribute("href")
            if href is not None:
                class_temp["class_id"] = href.split("/")[-1]
            else:
                class_temp["class_id"] = None
            if class_temp["class_id"] == "joinClass" or class_temp["class_id"] is None:
                break
            class_dict[i] = class_temp

        if len(class_dict) == 0:
            print("클래스가 없습니다.")
            quit()
        elif len(class_dict) == 1:
            choice_class_val = 0
        else:
            choice_class_val = choice_class(class_dict=class_dict)
        class_id = class_dict[choice_class_val].get("class_id")

        driver.get(f"https://www.classcard.net/ClassMain/{class_id}")
        time.sleep(1)

        sets_div = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div"
        )
        sets = sets_div.find_elements(By.CLASS_NAME, "set-items")
        sets_dict = {}
        for set_item, i in zip(sets, range(len(sets))):
            a_tag = set_item.find_element(By.TAG_NAME, "a")
            set_temp = {}
            set_temp["card_num"] = a_tag.find_element(By.TAG_NAME, "span").text
            set_temp["title"] = a_tag.text.replace(set_temp["card_num"], "")
            set_temp["set_id"] = a_tag.get_attribute("data-idx")
            sets_dict[i] = set_temp

        choice_set_vals = choice_set(sets_dict)
        ch_d_list = chd_wh()  # 여러 개 선택 가능
        for ch_d in ch_d_list:
            for choice_set_val in choice_set_vals:
                set_site = (
                    f"https://www.classcard.net/set/{sets_dict[choice_set_val]['set_id']}/{class_id}"
                )
                driver.get(set_site)
                time.sleep(1)

                user_id = int(driver.execute_script("return c_u;"))

                driver.find_element(By.CSS_SELECTOR,
                    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a"
                ).click()
                driver.find_element(By.CSS_SELECTOR,
                    "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)"
                ).click()

                html = BeautifulSoup(driver.page_source, "html.parser")
                cards_ele = html.find("div", class_="flip-body")
                if cards_ele is not None and hasattr(cards_ele, 'find_all'):
                    num_d = len(cards_ele.find_all("div", class_="flip-card")) + 1
                else:
                    print("세트 내 카드 정보를 찾을 수 없습니다. 건너뜁니다.")
                    continue

                time.sleep(0.5)

                word_d = word_get(driver, num_d)
                da_e, da_k, da_kn, da_kyn, da_ked, da_sd, da_e_clean, da_k_clean = word_d

                print(f"\n====== '{sets_dict[choice_set_val]['title']}' 세트 학습 시작 ======\n")

                if ch_d == 1:
                    test.run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1, da_e_clean, da_k_clean)
                elif ch_d == 2:
                    memorization.run_memorization(driver, num_d)
                elif ch_d == 3:
                    recall.run_recall(driver, num_d, da_e, da_kyn, time_2)
                elif ch_d == 4:
                    spelling.run_spelling(driver, num_d, da_e, da_k)
                elif ch_d == 5:
                    matching_game.run_matching_game(driver, da_e, da_k)
                else:
                    print("잘못된 학습 유형, 프로그램 종료")
                    break

                print(f"\n====== '{sets_dict[choice_set_val]['title']}' 세트 학습 완료 ======\n")
                time.sleep(1)

        print("\n✅ 모든 선택한 세트 학습이 완료되었습니다.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

#hello ;) just a easter egg