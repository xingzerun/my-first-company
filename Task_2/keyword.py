# 基于selenium，但是只能翻到第二页，就会报错
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

headers = {
	'Cookie':'BIDUPSID=D4E83E84E6A2208F63BE1733F751E07E; BAIDUID=2221992CE99AFA0F9F0F1BD6E66396A1:FG=1; PSTM=1498788943; BDSFRCVID=TIKsJeCCxG3GiIbZookQ5OGHba7whtMiNC4n3J; H_BDCLCKID_SF=JJFOoC_ytDvhKROmK4r2q4tehHRWLPneWDTm_D_X2p6-SbcLhUoMbPDuQNKeKMnBMRkt-pPKKR7m8Dt60b5YK4_UhRolXPQM3mkjbnQzfn02OPKzDxv4-P4syPRrJfRnWIjybIFhJKI2hC8meno_Mt4HqxOK2tbbKCoMsJOOaCvxOqvRy4oTLnk1DPJ0B4jzaKOWbC5v3hnDHD36MbOYMfCdjMIeBjT2-DA_oKPKJInP; locale=zh; BDRCVFR[mkUqnUt8juD]=mk3SLVN4HKm; H_PS_645EC=aa4asICl2T3NneUu5nyIS3y4vSHmVQ472iM7bRRrv6nzS6r9pdCKS28nexPH%2FrsvBbf7AQ; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BD_CK_SAM=1; PSINO=3; BD_HOME=0; H_PS_PSSID=1437_13701_21088_23632_20927; BD_UPN=12314353',
	'Host':'www.baidu.com',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def search():
	print('正在搜索...')
	try:
		driver.get('https://www.baidu.com')
		input = wait.until(
		    EC.presence_of_element_located((By.CSS_SELECTOR, "#kw"))
		)
		submit = wait.until(
		    EC.element_to_be_clickable((By.CSS_SELECTOR, "#su"))
		)
		input.send_keys('游戏')
		submit.click()
		firstpage = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#page > strong > span.pc')))
		return firstpage.text
	except TimeoutException:
		return search()


def nextPage():
	print('正在翻页...')
	nextPage = wait.until(
		EC.element_to_be_clickable((By.LINK_TEXT, '下一页>'))
	)
	nextPage.click()
	page = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#page > strong > span.pc')))



def main():
	print('开始搜索...')
	firstpage = search()
	print(firstpage)
	for i in range(5):
		nextPage()

if __name__ == '__main__':
	main()
