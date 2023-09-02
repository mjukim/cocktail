import requests
import json
from bs4 import BeautifulSoup

# Function to scrape data from a given URL
def scrape_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {url}")
        return None

    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    target_div_class = "dailyshot-Stack-root dailyshot-1nmrv06"
    name_target_div_class = "dailyshot-Stack-root dailyshot-1178y6y"
    target_divs = soup.find_all("div", {"class": target_div_class})
    name_divs = soup.find_all("div", {"class": name_target_div_class})

    if target_divs:
        result_dict = {}
        # 네임
    for name_div in name_divs:
        name_text_element = name_div.find("h1", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-2eov7z"})
        if name_text_element:
            name_text = name_text_element.text
            result_dict["name"] = name_text
    # 각각의 요소에서 Aroma, Taste, Finish 정보 추출하기
    for target_div in target_divs[1:2]:  # 인덱스 1부터 2까지 (두 번째 요소만 선택)
        # Aroma
        try:
            aroma_div = target_div.find("div", {"class": "dailyshot-Group-root dailyshot-8k3bl3"})
            if aroma_div:
                aroma_title_element = aroma_div.find("h3", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-o22yry"})
                aroma_text_element = aroma_div.find("div", {"class": "dailyshot-Text-root dailyshot-uc2z2z"})
                if aroma_title_element and aroma_text_element:
                    aroma_title = aroma_title_element.text if aroma_title_element else None
                    aroma_text = aroma_text_element.text if aroma_text_element else None
                    result_dict[aroma_title] = aroma_text
            try:
                taste_div = aroma_div.find_next("div", {"class": "dailyshot-Group-root dailyshot-8k3bl3"})
                if taste_div:
                    taste_title_element = taste_div.find("h3", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-o22yry"})
                    taste_text_element = taste_div.find("div", {"class": "dailyshot-Text-root dailyshot-uc2z2z"})
                    if taste_title_element and taste_text_element:
                        taste_title = taste_title_element.text if taste_title_element else None
                        taste_text = taste_text_element.text if taste_text_element else None
                        result_dict[taste_title] = taste_text
                try:
                    finish_div = taste_div.find_next("div", {"class": "dailyshot-Group-root dailyshot-8k3bl3"})
                    if finish_div:
                        finish_title_element = finish_div.find("h3", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-o22yry"})
                        finish_text_element = finish_div.find("div", {"class": "dailyshot-Text-root dailyshot-uc2z2z"})
                        if finish_title_element and finish_text_element:
                            finish_title = finish_title_element.text if finish_title_element else None
                            finish_text = finish_text_element.text if finish_text_element else None
                            result_dict[finish_title] = finish_text
                except AttributeError:
                    pass
            except AttributeError:
                pass
        except AttributeError:
            pass
        # Taste

        # Finish

        
    for target_div in target_divs[2:3]:  # 인덱스 2부터 3까지 (세 번째 요소만 선택)
        # 종류
        try:
            kind_div = target_div.find("div", {"class": "dailyshot-Group-root dailyshot-8k3bl3"})
            if kind_div:
                kind_title_element = kind_div.find("h3", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-o22yry"})
                kind_text_element = kind_div.find("div", {"class": "dailyshot-Text-root dailyshot-uc2z2z"})
                if kind_title_element and kind_text_element:
                    kind_title = kind_title_element.text if kind_title_element else None
                    kind_text = kind_text_element.text if kind_text_element else None
                    result_dict[kind_title] = kind_text
        except AttributeError:
            pass
        
        # 용량
        try:
            volume_div = kind_div.find_next("div", {"class": "dailyshot-Group-root dailyshot-8k3bl3"})
            if volume_div:
                volume_title_element = volume_div.find("h3", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-o22yry"})
                volume_text_element =volume_div.find("div", {"class": "dailyshot-Text-root dailyshot-uc2z2z"})
                if volume_title_element and volume_text_element:
                    volume_title = volume_title_element.text if volume_title_element else None
                    volume_text = volume_text_element.text if volume_text_element else None
                    result_dict[volume_title] = volume_text
        except AttributeError:
            pass
        
        # 도수
        try:
            acl_div = volume_div.find_next("div", {"class": "dailyshot-Group-root dailyshot-8k3bl3"})
            if acl_div:
                acl_title_element = acl_div.find("h3", {"class": "dailyshot-Text-root dailyshot-Title-root dailyshot-o22yry"})
                acl_text_element = acl_div.find("div", {"class": "dailyshot-Text-root dailyshot-uc2z2z"})
                if acl_title_element and acl_text_element:
                    acl_title = acl_title_element.text if acl_title_element else None
                    acl_text = acl_text_element.text if acl_text_element else None
                    result_dict[acl_title] = acl_text
        except AttributeError:
            pass
        
        return result_dict

    else:
        print(f"Target divs not found: {url}")
        return None

# Starting and ending item numbers
data_list = []

# Starting and ending item numbers
start_item = 1
end_item = 87000

for item_number in range(start_item, end_item + 1):
    url = f"https://dailyshot.co/m/items/{item_number}"
    data = scrape_data(url)
    if data:
        data_list.append(data)


# 데이터를 JSON 파일로 저장
with open("./data.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)