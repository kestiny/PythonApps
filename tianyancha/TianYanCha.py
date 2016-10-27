# coding = utf-8

import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class TianYanCha(object):
	"""docstring for TianYanCha"""
	def __init__(self, sucPath, failedPath):
		super(TianYanCha, self).__init__()
		'''初始化查询结果的存储文件'''
		self.fileSuc = open(sucPath, 'a')
		self.fileFailed = open(failedPath, 'a')
		#self.driver = webdriver.PhantomJS(executable_path = 'C:/Programs/Python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
		self.driver = webdriver.PhantomJS(executable_path = './phantomjs2.1.1/bin/phantomjs.exe')

	def __del__(self):
		print('dle phantomjs')
		self.fileSuc.close()
		self.fileFailed.close()
		self.driver.quit()
		
	def setOutput(self,text):
		self.text = text

	def getCompanyByName(self, company):
		url = 'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % urllib.parse.quote(company)
		self.text.insert('end', '开始查找公司：' + company + ' ' + url + "\r\n")
		self.driver.get(url)
		self.driver.implicitly_wait(10)
		spans = self.driver.find_elements_by_css_selector('span[class=\"c9 ng-binding\"]')
		print(self.driver.page_source)
		if len(spans) > 0:
			href = self.driver.find_elements_by_css_selector('a[class=\"query_name\"]')
			if len(href) > 0:
				result = company
				url = href[0].get_attribute('href')
				self.text.insert('end', '找到公司%s，正在查询详细信息：%s\r\n' %(company, url))
				self.driver.get(url)
				self.driver.implicitly_wait(10)
				#获取公司名称
				name = self.driver.find_elements_by_css_selector('div[class=\"company_info_text\"]')
				if len(name) > 0:
					infos = name[0].text.split('\n')
					self.text.insert('end', infos)
				#获取公司注册资本
				regCapital = self.driver.find_elements_by_css_selector('td[class=\"td-regCapital-value\"]')
				if len(regCapital) > 0:
					result = result + " " + regCapital[0].text
				#获取公司注册状态
				regStatus = self.driver.find_elements_by_css_selector('td[class=\"td-regStatus-value\"]')
				if len(regStatus) > 0:
					result = result + " " + regStatus[0].text
				self.fileSuc.write(result)
				self.fileSuc.write('\r')
				self.fileSuc.flush()
				self.text.insert('end', result + "\r\n")
				self.text.vbar.set(1, 1)
			else:
				self.text.insert('end', self.driver.page_source)
		else:
			spans = self.driver.find_elements_by_css_selector('span[class=\"c8\"]')
			if len(spans) > 0:
				self.text.insert('end', '未找到公司 %s 的相关信息\r\n' % company)
				self.fileFailed.write(company)
				self.fileFailed.write('\r')
			else:
				spans = self.driver.find_elements_by_css_selector('div[class=\"gt-input\"]')
				if len(spans) > 0:
					self.text.insert('end', '需要输入验证码了！！！！' + '\r\n')
				else:
					self.text.insert('end', '查询公司 %s 遇到错误\r\n' % company)
					self.fileFailed.write('               ' + company)
					self.fileFailed.write('\r')
			self.fileFailed.flush()

def main():
	query = TianYanCha('F:/suc.txt', 'F:/fail.txt')
	file = open('F:/all.txt')
	query.getCompanyByName('北京博瑞朗科技有限公司')
	#for line in file.readlines():
		#query.getCompanyByName(line.strip('\n'))

if __name__ == '__main__':
	main()
