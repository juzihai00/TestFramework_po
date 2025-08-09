from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Edge()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("http://127.0.0.1/web/guest/home")

driver.find_element(By.CSS_SELECTOR,"#portlet-wrapper-58 > div.portlet-content > div > div > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]").send_keys("user1")
driver.find_element(By.CSS_SELECTOR,"#_58_password").send_keys("1111")
driver.find_element(By.CSS_SELECTOR,"input[value='登录']").click()
driver.find_element(By.CSS_SELECTOR,"li[class='sortable-item'] a span").click()
driver.find_element(By.CSS_SELECTOR,"a[href='http://127.0.0.1/group/10779/upload?p_p_id=20&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_20_struts_action=%2Fdocument_library%2Fview&_20_folderId=53939']").click()
driver.find_element(By.CSS_SELECTOR,"input[value='上传文档']").click()
iframe = driver.find_element(By.XPATH,"//iframe[@id='dlFileEntryUploadProgress-iframe']")
driver.switch_to.frame(iframe)
driver.find_element(By.CSS_SELECTOR,"#_20_file").send_keys(r"D:\code\python_code\TestFramework_po\Data\Temp\upload_file.txt")
driver.find_element(By.CSS_SELECTOR,"#_20_title").send_keys("123")
driver.find_element(By.CSS_SELECTOR,"#_20_description").send_keys("456")
sleep(3)

driver.quit()