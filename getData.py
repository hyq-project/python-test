import csv
import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Bs4


def get_data():
    # 设置浏览器驱动参数,该驱动和googl浏览器在同一目录下，否则报错
    driver = webdriver.Chrome('D:\QQPCmgr\Google\chromedriver.exe')
    # 访问网页地址
    driver.get("https://iftp.chinamoney.com.cn/english/bdInfo/")
    # 获取select元素，设置两个下拉框的值
    Select(driver.find_element(By.XPATH,
                               "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[4]/div[2]/select")).select_by_value(
        '100001')
    Select(driver.find_element(By.XPATH,
                               "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/select")).select_by_value(
        '2023')

    # 点击提交按钮
    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[8]/a[1]').click()

    # 获取页数
    pages = int(driver.find_element(By.CLASS_NAME, 'page-total').text)
    # print(pages)
    data = [["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"]]
    for i in range(1, pages):
        table = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/table/tbody')
        # print(table)
        # 获取每一行数据tr
        table_tr_list = table.find_elements(By.TAG_NAME, "tr")
        # 按行查询表格的数据，取出的数据是一整行
        for tr in table_tr_list:
            td_list = tr.get_attribute('innerText').split("\t")
            if td_list:
                # print(td_list)
                data.append([td_list[0], td_list[1], td_list[2], td_list[3], td_list[4], td_list[5]])
        time.sleep(1)
        # 点击下一页按钮
        driver.find_element(By.XPATH,
                            '/html/body/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[3]/ul/li[4]/a').click()
        time.sleep(1)
    # 将数据保存到csv文件中
    with open('./bond_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    driver.quit()
    print(data)
