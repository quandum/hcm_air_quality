# -*- coding: utf-8 -*-
7### I/O and OS functions
from pprint import pprint
import os,sys,platform

import json,csv

### Selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of


from unidecode import unidecode ## chuyển tiếng việt thành không dấu.
CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# CURRENT_WORKING_DIRECTORY = r'd:\HCMUS\Data Engineer\project'

CHROMEDRIVER_PATH =  os.path.join(CURRENT_WORKING_DIRECTORY,("chromedriver.exe" if 'windows' in platform.system().lower() else "chromedriver" ))
FIREFOX_DRIVER_PATH =  os.path.join(CURRENT_WORKING_DIRECTORY,("geckodriver.exe" if 'windows' in platform.system().lower() else "geckodriver" ))
print("CHROMEDRIVER_PATH: " + CHROMEDRIVER_PATH)
print("FIREFOX_DRIVER_PATH: " + FIREFOX_DRIVER_PATH)

DATA_DIRECTORY = os.path.join(CURRENT_WORKING_DIRECTORY,'data')
    
    
print("working directory: " + CURRENT_WORKING_DIRECTORY)
print("data directory: " + DATA_DIRECTORY)

log_file = open("crawl_log.txt",'w',encoding='utf8')
def log_print(string, CONSOLE = True):
    log_file.write("%s\n"%string)
    if (CONSOLE==True):
        print(string)

if (os.path.exists(DATA_DIRECTORY)==False):
    log_print('DATA_DIRECTORY NOT EXISTED! CREATING ONE....')
    os.mkdir(DATA_DIRECTORY)
    log_print('DATA_DIRECTORY CREATED AT "%s"! '%DATA_DIRECTORY)
else:
    log_print('DATA_DIRECTORY EXISTED AT "%s"! '%DATA_DIRECTORY)



if (os.path.exists(CHROMEDRIVER_PATH)==False):
    print("File not found at '%s'" %CHROMEDRIVER_PATH)
    print("Pleáse put in the correct file chromedriver")
    exit(0)

# browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
browser = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)


browser.get(r"https://www.iqair.com/vi/vietnam/ho-chi-minh-city")
WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH,r"/html/body/app-root/app-portal-container/div/app-routes-resolver/div/app-city/div[2]/div[1]/app-aqi-ranking[1]/div")))
loc_table=browser.find_element(By.XPATH,r"/html/body/app-root/app-portal-container/div/app-routes-resolver/div/app-city/div[2]/div[1]/app-aqi-ranking[2]/div/table/tbody")




locs=loc_table.find_elements_by_tag_name("tr")
print("Table locations detected")

f=open(os.path.join(DATA_DIRECTORY,"locations_link.csv"),"w")
CRAWLING_SITE_URLS={}
writer=csv.DictWriter(f,fieldnames=['location','url',"vn_no_accent"])
writer.writeheader()
for loc in locs:
    c1,c2,c3=loc.find_elements_by_tag_name("td")
    loc_name=c2.text.strip()
    loc_url=c2.find_element_by_tag_name("a").get_attribute("href").strip()
    no_accent=unidecode(loc_name).strip()
    writer.writerow({'location':loc_name,'url':loc_url,"vn_no_accent":no_accent})
    CRAWLING_SITE_URLS[no_accent]=loc_url
    log_print("Found location '%s' at the url: '%s'"%(loc_name,loc_url))
f.close()
pprint(CRAWLING_SITE_URLS)



def find_button_by_text(text,strictly_matched=False):
    global browser
    try:
        WebDriverWait(browser,0.025).until(EC.visibility_of_all_elements_located((By.TAG_NAME,'button')))
    except:
        pass
    all_buttons=browser.find_elements(By.TAG_NAME,"button")
    for bt in all_buttons:
        if (strictly_matched==False):
            if (text.lower().strip() in bt.text.strip().lower()):
                return bt
        else:
            if (text == bt.text.strip()):
                return bt
    return None




for SOURCE_NAME, url in CRAWLING_SITE_URLS.items():

    log_print("LOADING PAGE '%s' at: %s"%(SOURCE_NAME,url))
    browser.get(url)
    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH,r"/html/body/app-root/app-site-cookie-dialog/div/div/div[2]/button")))
        find_button_by_text("TÔI ĐỒNG Ý").click()
        log_print("Clicked button agree!")
    except:
        log_print("Unable to click the button agree, or not found button!")


    BRAND_DATA_DIRECTORY = os.path.join( DATA_DIRECTORY , SOURCE_NAME)
    if (os.path.exists(BRAND_DATA_DIRECTORY)==False):
        os.mkdir(BRAND_DATA_DIRECTORY)
        log_print("Folder '%s' was created"%BRAND_DATA_DIRECTORY)
    else:
        log_print("Folder '%s' was found!"%BRAND_DATA_DIRECTORY)


    for mode1 in ['daily','hourly']:
        for mode2 in ["AQI","PM2.5"]:
            try:
                WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.XPATH,r"/html/body/app-root/app-site-cookie-dialog/div/div/div[2]/button")))
            except:
                pass

            if (mode1 == 'daily'):
                find_button_by_text('HẰNG NGÀY').click()
            else:
                find_button_by_text('HẰNG GIỜ').click()
            browser.implicitly_wait(1)
            if (mode2=='AQI'):
                find_button_by_text('AQI').click()
            else:
                find_button_by_text('PM2.5').click()

            data_file_path=os.path.join(BRAND_DATA_DIRECTORY,"%s%s.csv"%(mode2.lower(),mode1))
            data=[]
            if (os.path.exists(data_file_path)==True):
                f=open(data_file_path,'r',encoding='utf8')
                for rec in csv.DictReader(f):
                    data.append(dict(rec))
                f.close()
            
            browser.implicitly_wait(1)
            
            try:
                WebDriverWait(browser,0.5).until(EC.presence_of_element_located((By.CLASS_NAME,'highcharts-series-group')))
            except:
                pass
            
            chart=browser.find_element(By.CLASS_NAME,'highcharts-series-group')
            try:
                WebDriverWait(browser,1).until(EC.EC.presence_of_all_elements_located((By.TAG_NAME,'rect')))
            except:
                pass
            browser_actions=ActionChains(browser)
            bars=chart.find_elements(By.TAG_NAME,"rect")
            for b in bars:
                browser_actions.move_to_element(b).perform() 
                browser.implicitly_wait(0.025)
                all_texts=browser.find_elements(By.TAG_NAME,"text")
                bar_info_found=False
                for t in all_texts:
                    try:
                        tspans=t.find_elements(By.TAG_NAME,"tspan")
                        if (len(tspans)==3):
                            print(t.text)
                            timestamp=tspans[0].text.strip()
                            rating = tspans[1].text.strip()
                            value = tspans[2].text.strip()
                            new_rec={"timestamp":timestamp,"value":value,"rating":rating}
                            new_data=True
                            for ind in range(len(data)):
                                if (data[ind]['timestamp']==timestamp):
                                    data[ind]=new_rec
                                    new_data=False
                                    break
                            if (new_data):
                                data.append(new_rec)
                            bar_info_found=True
                    except:
                        pass
                assert (bar_info_found==True)
            f=open(data_file_path,"w",encoding='utf8')
            writer=csv.DictWriter(f,fieldnames=["timestamp","value",'rating'])
            writer.writeheader()
            for rec in data:
                writer.writerow(rec)
            f.close()
            log_print("The file '%s' now has %d rows."%(data_file_path,len(data)))
browser.quit()
log_print("ALL DONE!")
log_file.close()