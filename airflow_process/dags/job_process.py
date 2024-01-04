
import pandas as pd
from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
import json
import pymongo
import re
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime

def mongo_connection(collection_name):

    mongoclient = pymongo.MongoClient("")
    database = mongoclient["jobs_database"]
    collection = database[collection_name]

    return collection

def set_lon_lat(dataframe,dictionnary):
    for row in dataframe.iterrows():
        key = row[1]["jobLocation"].lower().strip()
        if key in dictionnary:
            dataframe.loc[row[0],"latitude"]= dictionnary[key][0]
            dataframe.loc[row[0],"longitude"]= dictionnary[key][1]
            
        else:
            dataframe.loc[row[0],"latitude"]= None
            dataframe.loc[row[0],"longitude"]= None
           


def get_rekrute_data():

    s = Service('/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome-stable"
    options.add_argument('headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--homedir=/tmp/chrome/chrome-user-data-dir')
    options.add_argument('--user-data-dir=/tmp/chrome/chrome-user-data-dir')
    prefs = {"download.default_directory":"/tmp/chrome/chrome-user-data-di",
            "download.prompt_for_download":False
    }
    options.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(service=s, options=options)

    URL="https://www.rekrute.com/offres.html?s=3&p=1&o=1"
    browser.get(URL)
    time.sleep(2)

    jobTitlesLocations = [job.text for job in browser.find_elements(By.XPATH,'//a[@class="titreJob"]')]
    jobTitles = [job.split("|")[0] for job in jobTitlesLocations]
    jobLocations = [job.split("|")[1] for job in jobTitlesLocations]
    jobDescriptions = [description.text for description in browser.find_elements(By.XPATH,'//div[@class="info"]/span[@style="color: #5b5b5b;margin-top: 5px;"]')]
    date_offer = [date.text for date in browser.find_elements(By.XPATH,'//em[@class="date"]')]
    jobs_info = browser.find_elements(By.XPATH,'//div[@class="info"]/ul')
    sector = [info.find_elements(By.XPATH,'./li')[0].text for info in jobs_info]
    function = [info.find_elements(By.XPATH,'./li')[1].text for info in jobs_info]
    experience_required = [info.find_elements(By.XPATH,'./li')[2].text for info in jobs_info]
    level_of_study = [info.find_elements(By.XPATH,'./li')[3].text for info in jobs_info]
    type_of_contract = [info.find_elements(By.XPATH,'./li')[4].text for info in jobs_info]


    date_pattern = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')

    start_date = [date_pattern.findall(date)[0] for date in date_offer]
    end_date = [date_pattern.findall(date)[1] for date in date_offer]
    domain_sectors = [domain.split(":")[1] for domain in sector]
    jobs_function = [job_func.split(":")[1] for job_func in function]
    year_experiences_required = [year_experience.split(":")[1] for year_experience in experience_required]
    study_level = [level.split(":")[1] for level in level_of_study]
    contract_type = [contract.split(":")[1].split("-")[0] for contract in type_of_contract]
    is_remote = [contract.split(":")[2] for contract in type_of_contract]

    dataframe = pd.DataFrame({"jobTitle":jobTitles,"jobLocation":jobLocations,"jobDescription":jobDescriptions,"start_date":start_date,
                          "end_date":end_date,"domain_sectors":domain_sectors,"jobs_function":jobs_function,
                          "year_experiences_required":year_experiences_required,"study_level":study_level,
                          "contract_type":contract_type,"is_remote":is_remote})
    
    collection = mongo_connection("rekrute_collection")
    for row in dataframe.iterrows():
        collection.insert_one({
             "jobTitle":row[1]["jobTitle"],
             "jobLocation":row[1]["jobLocation"],
             "jobDescription":row[1]["jobDescription"],
             "start_date":row[1]["start_date"],
             "end_date":row[1]["end_date"],
             "domain_sectors":row[1]["domain_sectors"],
             "jobs_function":row[1]["jobs_function"],
             "year_experiences_required":row[1]["year_experiences_required"],
             "study_level":row[1]["study_level"],
             "contract_type":row[1]["contract_type"],
             "is_remote":row[1]["is_remote"],
             "date_insert":datetime.now()
        })
    
    
def get_indeed_data():

    collection = mongo_connection("indeed_collection")

    client = ScrapingBeeClient(api_key='')

    # first page
    response = client.get('https://ma.indeed.com/jobs?q=offre+d%27emploi&fromage=1&vjk=39df24deb59b0e39&start=0')
    print('Response HTTP Status Code: ', response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.select('td.resultContent')
    for i in jobs :
        job = {}
        #job title
        job["jobTitle"] = i.find('a').text
        #company location
        try : job["jobLocation"] = i.select('div[class="css-t4u72d eu4oa1w0"]')[0].text
        except : job["jobLocation"] = None
        #company name
        try : job["company_names"] = i.select('span[class="css-1x7z1ps eu4oa1w0"]')[0].text
        except : job["company_names"] = None
        #job link
        job["links"] = i.find('a').get('href')
        job["insert_date"]=datetime.now()
        collection.insert_one(job)


    # other pages
    for i in range(10,10*10,10) :
        response = client.get(f'https://ma.indeed.com/jobs?q=offre+d%27emploi&fromage=1&vjk=39df24deb59b0e39&start={i}')
        print('Response HTTP Status Code: ', response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.select('td.resultContent')
        
        for i in jobs :
            job = {}
            #job title
            job["jobTitle"] = i.find('a').text
            #company location
            try : job["jobLocation"] = i.select('div[class="css-t4u72d eu4oa1w0"]')[0].text
            except : job["jobLocation"] = None
            #company name
            try : job["company_names"] = i.select('span[class="css-1x7z1ps eu4oa1w0"]')[0].text
            except : job["company_names"] = None
            #job link
            job["links"] = i.find('a').get('href')
            job["insert_date"]=datetime.now()
            collection.insert_one(job)
  


def transform_data():
    collection_indeed = mongo_connection("indeed_collection")
    collection_rekrute = mongo_connection("rekrute_collection")
    cursor_indeed = collection_indeed.find()
    cursor_rekrute = collection_rekrute.find()
    data_indeed = list(cursor_indeed)
    data_rekrute = list(cursor_rekrute)
    df_rekrute = pd.DataFrame(data_rekrute)
    df_indeed = pd.DataFrame(data_indeed)

    df_rekrute["jobLocation"] = df_rekrute["jobLocation"].apply(lambda x: x.replace("(Maroc)","").strip())

    dictionnary = None
    with open("/opt/airflow/dags/utilities.json") as f:
        dictionnary = json.load(f)
 
    set_lon_lat(df_rekrute,dictionnary)
    set_lon_lat(df_indeed,dictionnary)

    transformed_collection = mongo_connection("transformed_collection")

    for row_rekrute in df_rekrute.iterrows():
        transformed_collection.insert_one(dict(row_rekrute[1]))

    for row_indeed in df_indeed.iterrows():
        transformed_collection.insert_one(dict(row_indeed[1]))







with DAG('job_process', start_date=datetime(2024, 1, 3),
            schedule_interval="@daily",catchup=False) as dag:

        get_data_rekrute = PythonOperator(
                task_id = 'get_rekrute_data',
                python_callable = get_rekrute_data
        )
        get_data_indeed = PythonOperator(
                task_id = 'get_indeed_data',
                python_callable = get_indeed_data
        )
        data_transformation = PythonOperator(
                task_id = 'transformed_data',
                python_callable = transform_data
        )


        [get_data_rekrute,get_data_indeed] >> data_transformation



