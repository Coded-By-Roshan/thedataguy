from django.shortcuts import render,redirect,HttpResponse
from selenium import webdriver
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
global user_brand,competitor_name,keywords,search_products, single_products, sponsers,search_keyword,driver,prodRatings_count,prodRatings

def iniatilize_selenium(search_keyword):
    global user_brand,competitor_name,keywords,search_products, single_products, driver
    search_keyword = search_keyword
    global search_products,single_products
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--user-agent=roshannn')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.amazon.in/")
    time.sleep(5)
    input_bar = driver.find_element(By.ID,'twotabsearchtextbox')
    input_bar.send_keys(search_keyword)
    input_bar.send_keys(Keys.ENTER)

    try:
        ads_container = driver.find_element(By.CLASS_NAME,'_bGlmZ_headlineCTAContainer_1uDU0')
        ads_company = ads_container.find_elements(By.TAG_NAME,'a')[-1]
        ads_company =  ads_company.text
        ads_company = ads_company.split(" ")
        sponsers.append(ads_company[1])
    except:
        pass

    search_products = driver.find_elements(By.CLASS_NAME,'puis-card-container')
    single_products = driver.find_elements(By.CLASS_NAME,'sbv-video-single-product')




sponsers = []
bestSeller = {}
positions = {}
Reviews = {}
occurance = {}
prices = {}
totalBought = {}
competitorOccurance = {}
userBrandOccur ={}
ratedFor = {}
track_titles = []
prodRatings = {}
prodRatings_count = {}





def get_sponsers():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver,sponsers
    for spon in search_products:
        if("Sponsored" in spon.text):
            sponser_brand = spon.find_element(By.CLASS_NAME,"s-line-clamp-2").text
            sponser_brand = sponser_brand.split(" ")
            sponsers.append(sponser_brand[0])

    for sing_sponser in single_products:
        sponser_brand = sing_sponser.find_element(By.TAG_NAME,"h2").text
        sponser_brand = sponser_brand.split(" ")
        sponsers.append(sponser_brand[0])


def CheckBestSeller():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    for comp in competitor_name:
        for prod in search_products:
            if(comp.lower() in (prod.text).lower() and 'best seller' in (prod.text).lower()):
                bestSeller[comp] = True
                break
            else:
                bestSeller[comp] = False


def checkPositions():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    for comp in competitor_name:
        i = 1
        for prod in search_products:
            if(comp.lower() in (prod.text).lower()):
                positions[comp] = i
                break
            i = i+1
    i = 1
    for prod in search_products:
        if(user_brand.lower() in (prod.text).lower()):
            positions[user_brand] = i
            break
        i = i+1
            

def total_result():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    total_result_container = driver.find_element(By.XPATH,'//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span[1]').text
    total_result = total_result_container.split(' ')
    total_result = total_result[3]
    print(total_result)



def totalReview():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    for comp in competitor_name:
        for prod in search_products:
            if(comp.lower() in (prod.text).lower()):
                total_review = prod.find_element(By.CSS_SELECTOR,'.a-size-base.s-underline-text').text
                Reviews[comp] = total_review
                break

    for prod in search_products:
        if(user_brand.lower() in (prod.text).lower()):
            total_review = prod.find_element(By.CSS_SELECTOR,'.a-size-base.s-underline-text').text
            Reviews[user_brand] = total_review
            break


def totalOccurance():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    for comp in competitor_name:
        i = 0
        for prod in search_products:
            if(comp.lower() in (prod.text).lower()):
                i += 1
        occurance[comp] = i
    i = 0
    for prod in search_products:
        if(user_brand.lower() in (prod.text).lower()):
            i += 1
    occurance[user_brand] = i




def trackPrice():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    i = 1
    for comp in competitor_name:
        for prod in search_products:
            if(comp.lower() in (prod.text).lower()):
                prod_title = prod.find_element(By.TAG_NAME,'h2')
                pro_link = prod_title.find_element(By.TAG_NAME,'a')
                pro_link.click()
                print("clicked..")
                time.sleep(3)
                parent = driver.window_handles[0]
                chld = driver.window_handles[-1]
                driver.switch_to.window(chld)
                prod_price = driver.find_element(By.CLASS_NAME,'a-price-whole').text
                try:
                    total_bought = driver.find_element(By.ID,'social-proofing-faceout-title-tk_bought').text
                    total_bought = total_bought.split(" ")[0]
                except:
                    total_bought = " "
                title_box = driver.find_element(By.ID,'title_feature_div').text
                title_box = str(title_box)

                about_box = driver.find_element(By.ID,'feature-bullets').text
                about_box = str(about_box)
                try:
                    rated_box = driver.find_element(By.CSS_SELECTOR,'.brand-snapshot-flex-row.brand-snapshot-flex-wrap').text
                    ratedFor[f"{comp}-{i}"] = rated_box
                except:
                    ratedFor[f"{comp}-{i}"] = " "

                try:
                    trackTable()
                except:
                    pass
                total_occurance1 = title_box.count(search_keyword)
                total_occurance2 = about_box.count(search_keyword)
                competitorOccurance[f"{comp}-{i}"] = total_occurance1 + total_occurance2
                prices[f"{comp}-{i}"] = prod_price
                totalBought[f"{comp}-{i}"] = total_bought
                driver.switch_to.window(parent)
                
                i += 1




def trackOwnBrand():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    i = 1
    for prod in search_products:
            if(user_brand.lower() in (prod.text).lower()):
                prod_title = prod.find_element(By.TAG_NAME,'h2')
                pro_link = prod_title.find_element(By.TAG_NAME,'a')
                pro_link.click()
                time.sleep(3)
                p = driver.current_window_handle
                parent = driver.window_handles[0]
                chld = driver.window_handles[-1]
                driver.switch_to.window(chld)

                title_box = driver.find_element(By.ID,'title_feature_div').text
                title_box = str(title_box)
                
                about_box = driver.find_element(By.ID,'feature-bullets').text
                about_box = str(about_box)
                
               

                total_occurance1 = title_box.count(search_keyword)
                total_occurance2 = about_box.count(search_keyword)
                userBrandOccur[f"{user_brand}-{i}"] = total_occurance1 + total_occurance2
                driver.switch_to.window(parent)
                
                i += 1


def trackTable():
    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver
    table_container = driver.find_element(By.CLASS_NAME,'_product-comparison-desktop_desktopFaceoutStyle_comparison-table-wrapper__1UCJ-')
    titles = table_container.find_elements(By.CLASS_NAME,'_product-comparison-desktop_titleStyle_psem-comp-truncate__1ScOQ')
    review_row = driver.find_elements(By.CLASS_NAME,'_product-comparison-desktop_reviewsStyle_reviews-rating-icon__2KEGL')
    i = 0
    print(len(review_row))
    for tab in titles:
        brand_names = tab.text
        brand_names = brand_names.split(" ")[0]
        track_titles.append(brand_names)
    
    for rev in review_row:
        item_name = track_titles[i]
        ratings = rev.find_element(By.CSS_SELECTOR,'.a-size-base.a-color-base')
        review_count = rev.find_element(By.CSS_SELECTOR,'.a-size-base.a-color-link')
        print(ratings.text)
        print(review_count.text)
        prodRatings[f"{item_name}-{i}"] = ratings.text
        prodRatings_count[f"{item_name}-{i}"] = review_count.text
        i += 1



print(track_titles)
print(prodRatings)
print(prodRatings_count)

def home(request):
    return render(request,'home.html')


def get_data(request):

    global user_brand,competitor_name,keywords,search_products, single_products, search_keyword,driver,prodRatings_count,prodRatings
    if request.method == 'POST':
        user_brand = request.POST['brandname']
        competitor = request.POST['competitor']
        competitor_name = competitor.split(",")
        search_keyword = request.POST['keyword']
        iniatilize_selenium(search_keyword)
        get_sponsers()
        CheckBestSeller()
        checkPositions()
        total_result()
        totalOccurance()
        totalReview()
        trackOwnBrand()
        trackPrice()
        driver.quit()
        filtered_dict1 = {key: value for key, value in prodRatings.items() if value is not ""}
        filtered_dict2 = {key: value for key, value in prodRatings_count.items() if value is not ""}
        prodRatings = filtered_dict1
        prodRatings_count = filtered_dict2
        for key, value in ratedFor.items():
            ratedFor[key] = value.replace('\n', ', ')
        params ={'sponsers':sponsers,'bestSeller':bestSeller,'positions':positions,'Reviews':Reviews,'occurance':occurance,
                'prices':prices,'totalBought':totalBought,'competitorOccurance':competitorOccurance,
                'userBrandOccur':userBrandOccur,'ratedFor':ratedFor,'prod_ratings':prodRatings,'rating_count':prodRatings_count}

        # print(f"user_brand = {user_brand} | competitor = {competitor} | keyword = {keywords}")

    return render(request,'result.html',params)
    # except:
    #     return HttpResponse("Something went wrong..Try Later !!🫡🫡")