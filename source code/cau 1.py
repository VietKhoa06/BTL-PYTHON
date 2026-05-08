import pandas as pd
import time
import io
import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawl_premier_league_stats():
    options = uc.ChromeOptions()
    driver = None
    try:
        print("Dang khoi tao trinh duyet ...")
        driver = uc.Chrome(options=options,version_main=147)

        url = "https://fbref.com/en/comps/9/misc/Premier-League-Stats"
        print(f"Dang truy cập: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 25)
        table_element = wait.until(EC.presence_of_element_located((By.ID, "stats_misc")))

        html_content = table_element.get_attribute('outerHTML')
        df_list = pd.read_html(io.StringIO(html_content))
        df = df_list[0]

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(df.columns.nlevels - 1)

        df.columns = [str(col).strip() for col in df.columns]
        df = df.iloc[:, 1:]

        if 'Nation' in df.columns:
            df['Nation'] = df['Nation'].str.split().str[-1]
        if 'Min' in df.columns:
            col_min = 'Min'
        else:
            col_min = 'Minutes'

        if col_min in df.columns:
            df[col_min] = pd.to_numeric(df[col_min], errors='coerce')
            df = df[df[col_min] > 90].copy()
        else:
            if '90s' in df.columns:
                df['90s'] = pd.to_numeric(df['90s'], errors='coerce')
                df = df[df['90s'] > 1.0].copy()

        df = df[df['Player'] != 'Player']

        df = df.fillna("N/a")

        df.reset_index(drop=True, inplace=True)
        df.insert(0, 'STT', range(1, len(df) + 1))

        file_name = "cầu thủ thi đấu trên 90ph.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')

        print(f"THÀNH CÔNG!")
        print(f"Đã thu thập dữ liệu của {len(df)} cầu thủ.")
        print(f"File lưu tại: {file_name}")

    except Exception as e:
        print(f"[-] Có lỗi xảy ra trong quá trình chạy: {e}")
    finally:
        if driver:
            print("Đang đóng trình duyệt an toàn...")
            driver.close()
            driver.quit()
        driver = None
if __name__ == "__main__":
    crawl_premier_league_stats()