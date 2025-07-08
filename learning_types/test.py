# learning_types/test.py
import time
import random
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def wait_and_click(driver, by, identifier, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, identifier))
        )
        driver.execute_script("arguments[0].click();", element)
        return True
    except TimeoutException:
        return False

def wait_for_element(driver, by, identifier, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, identifier))
        )
        return element
    except TimeoutException:
        return None

def run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1, da_e_clean, da_k_clean):
    print("테스트학습을 시작합니다...")

    initial_steps = [
        (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div"),
        (By.CSS_SELECTOR, "#wrapper-test > div > div.quiz-start-div > div.layer.retry-layer.box > div.m-t-xl > a"),
        (By.XPATH, "//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a")
    ]

    for by, identifier in initial_steps:
        if not wait_and_click(driver, by, identifier, time_1):
            print("로딩 중 문제가 발생하여 테스트학습을 종료합니다.")
            return
        time.sleep(0.7)

    for _ in range(2):
        if not wait_and_click(driver, By.XPATH, "//*[@id='confirmModal']/div[2]/div/div[2]/a[3]", timeout=1):
            break
        time.sleep(0.7)

    if not wait_for_element(driver, By.XPATH, "//*[@id='testForm']/div[1]/div/div[1]/div[2]/div/div/div", timeout=time_1):
        print("화면 전환이 완료되지 않았습니다. 테스트학습을 종료합니다.")
        return
    
    for i in range(1, num_d):
        time.sleep(0.2)
        try:
            cash_d = driver.find_element(By.XPATH,
                                         f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]/div/div/div"
                                         ).text
            cash_d_clean = re.sub(r'[;,\s]+', '', cash_d)
            cash_d_clean = re.sub(r'[^\w가-힣]', '', cash_d_clean)  # 모든 기호 제거
            element = driver.find_element(By.XPATH,
                                          f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]"
                                          )
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)
            cash_dby = ["", "", "", "", "", ""]
            for j in range(0, 6):
                cash_dby[j] = driver.find_element(By.XPATH,
                                                  f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                  ).text
                cash_dby[j] = re.sub(r'[;,\s]+', '', cash_dby[j])
                cash_dby[j] = re.sub(r'[^\w가-힣]', '', cash_dby[j])  # 모든 기호 제거
            notFindData = False
            if cash_d.upper() != cash_d.lower():
                for j in range(0, 6):
                    try:
                        idx_e = da_e_clean.index(cash_d_clean)
                    except ValueError:
                        idx_e = -1
                    try:
                        idx_k = da_k_clean.index(cash_dby[j])
                    except ValueError:
                        idx_k = -1
                    try:
                        idx_kn = da_kn.index(cash_dby[j])
                    except ValueError:
                        idx_kn = -1
                    try:
                        idx_ked = da_ked.index(cash_dby[j])
                    except ValueError:
                        idx_ked = -1
                    if idx_e != -1 and idx_k != -1 and idx_e == idx_k:
                        element = driver.find_element(By.XPATH,
                                                      f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                      )
                        driver.execute_script("arguments[0].click();", element)
                        notFindData = True
                        break
                    elif idx_e != -1 and idx_kn != -1 and idx_e == idx_kn:
                        element = driver.find_element(By.XPATH,
                                                      f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                      )
                        driver.execute_script("arguments[0].click();", element)
                        notFindData = True
                        break
                    elif idx_e != -1 and idx_ked != -1 and idx_e == idx_ked:
                        element = driver.find_element(By.XPATH,
                                                      f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                      )
                        driver.execute_script("arguments[0].click();", element)
                        notFindData = True
                        break
            else:
                for j in range(0, 6):
                    try:
                        idx_k = da_k_clean.index(cash_d_clean)
                    except ValueError:
                        idx_k = -1
                    try:
                        idx_e = da_e_clean.index(cash_dby[j])
                    except ValueError:
                        idx_e = -1
                    try:
                        idx_kn = da_kn.index(cash_d_clean)
                    except ValueError:
                        idx_kn = -1
                    try:
                        idx_ked = da_ked.index(cash_d_clean)
                    except ValueError:
                        idx_ked = -1
                    if idx_k != -1 and idx_e != -1 and idx_k == idx_e:
                        element = driver.find_element(By.XPATH,
                                                      f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                      )
                        driver.execute_script("arguments[0].click();", element)
                        notFindData = True
                        break
                    elif idx_kn != -1 and idx_e != -1 and idx_kn == idx_e:
                        element = driver.find_element(By.XPATH,
                                                      f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                      )
                        driver.execute_script("arguments[0].click();", element)
                        notFindData = True
                        break
                    elif idx_ked != -1 and idx_e != -1 and idx_ked == idx_e:
                        element = driver.find_element(By.XPATH,
                                                      f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{j + 1}]/label/div/div"
                                                      )
                        driver.execute_script("arguments[0].click();", element)
                        notFindData = True
                        break
            if notFindData != True:
                print("\nDetected Missing Words!!, Randomly Selected\n")
                try:
                    # 모달 창이 있다면 먼저 닫기
                    try:
                        modal_close = driver.find_element(By.XPATH, "//*[@id='confirmModal']/div[2]/div/div[2]/a[3]")
                        if modal_close.is_displayed():
                            modal_close.click()
                            time.sleep(0.5)
                    except:
                        pass
                    
                    # 랜덤 선택
                    random_choice = random.randint(1, 6)
                    element = driver.find_element(By.XPATH,
                                                f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{random_choice}]/label/div/div"
                                                )
                    # JavaScript click 대신 일반 click 사용
                    element.click()
                    time.sleep(time_1)
                    
                    # 랜덤 선택 후 더 긴 대기 시간 적용
                    print(f"랜덤 선택 완료, 추가 대기 중... (문제 {i})")
                    time.sleep(3)  # 3초 추가 대기
                        
                except Exception as e:
                    print(f"랜덤 선택 중 오류 발생: {e}")
                    # 강제로 JavaScript click 시도
                    try:
                        element = driver.find_element(By.XPATH,
                                                    f"//*[@id='testForm']/div[{i}]/div/div[2]/div/div[1]/div[{random.randint(1, 6)}]/label/div/div"
                                                    )
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(time_1)
                        
                        # 랜덤 선택 후 더 긴 대기 시간 적용
                        print(f"JavaScript 랜덤 선택 완료, 추가 대기 중... (문제 {i})")
                        time.sleep(3)  # 3초 추가 대기
                            
                    except:
                        print("클릭 실패, 다음 문제로 넘어갑니다.")
                        pass
            time.sleep(1.5)
        except NoSuchElementException:
            print("단어가 더 이상 존재하지 않습니다. 테스트학습을 종료하는 중입니다...")
            break
    print("테스트학습이 완료되었습니다.")
