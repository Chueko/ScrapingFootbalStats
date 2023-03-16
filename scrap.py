from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import writeData
import pycountry

#get country substring for flag reference on site 
#Example: Argentina : ar Brazil:br
def get_country_code(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        code = country.alpha_2.lower()
        return code
    except LookupError:
        return None




def start_chrome():
    chromedriver_path=ChromeDriverManager(path="./chromedriver").install()
    options=Options()
    #Set options for driver
    user_agent={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("--window-size=700,1000")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certofocate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    #on-start parameters
    ext_opt=[
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]
    options.add_experimental_option("excludeSwitches",ext_opt)
    #preference parameters
    prefs={
        "profile.default_content_setting_values.notifications":2, #0=ask,1=allow,2=dont allow
        "intl.accept_languages":["es-ES","es"], #language
        "credentials_enable_service":False #avoid ask for save credentials
    }
    options.add_experimental_option("prefs",prefs)

    #start service
    s=Service(chromedriver_path)
    #instace of chromedriver
    driver=webdriver.Chrome(service=s,options=options)

    return driver

def scrap(country):
    flag="span.flg-"+country
    data=[]
    try:
            driver.get('https://www.whoscored.com/')
            time.sleep(2)
    except WebDriverException:
        print(f"Error ocurrs abort...\n")
        return 0
      
    #create google sheet, set titles on columns and return id
    id=writeData.setTitles()
    #Navigate to statistics menu
    driver.find_element(By.CSS_SELECTOR,"a#statistics-menuitem").click()
    time.sleep(2)
    #Count pages on the players statistics grid
    pagen=driver.find_elements(By.CSS_SELECTOR,"dl.right")
    count=0
    #manage to skip 2 elements found previously that doesnt need to
    for i in pagen:
        if(count==2):
            pages=int(i.text.split(" |")[0].split("/")[1])
        count+=1
    page=1
    #While because the site sometimes doesnt get the click right
    while(page<pages):
        #find the table of player statistics
        elements=driver.find_element(By.CSS_SELECTOR,"div#statistics-table-summary").find_elements(By.CSS_SELECTOR,"td.grid-abs")
        for element in elements:
            aux=[]
            #search for players from the country selected
            try:
                element.find_element(By.CSS_SELECTOR,flag)
                url=element.find_element(By.CSS_SELECTOR,"a.player-link").get_attribute("href")
                #opens player page
                driver_aux.get(url)
                time.sleep(2)
                
                #scrap data
                aux.append(driver_aux.find_element(By.CSS_SELECTOR,"h1.header-name").text)
                table=driver_aux.find_element(By.CSS_SELECTOR,"tbody#player-table-statistics-body")
                table=table.find_elements(By.CSS_SELECTOR,"tr")[-1]
                table=table.find_elements(By.CSS_SELECTOR,"td")
                count=0
                #skip 2 props that doesnt need
                for prop in table:
                    if(count>1):
                        aux.append(prop.text)
                    count+=1
                data.append(aux) 
            except:
                continue
        #search for next button and skip first one
        btns=driver.find_elements(By.CSS_SELECTOR,"a#next.option.clickable")
        cnt=0
        for btn in btns:
            if(cnt==1):
                next=btn
            cnt+=1
        try:
            next.click()
            time.sleep(2)
            page+=1
        except:
            continue           
    writeData.writeData(data,id)  
                
       
        
if __name__ == "__main__":
    country_name=input("Wich country you want to see players? ")
    country=get_country_code(country_name)
    driver=start_chrome()
    driver_aux=start_chrome()
    scrap(country)
    input("Pulsa ENTER para contiunar")
    driver.quit()
    driver_aux.quit()
