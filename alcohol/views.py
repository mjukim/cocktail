from django.shortcuts import render
from django.views import View
from django.db import connection
from django.http import JsonResponse
from cachetools import TTLCache
import googletrans
import openai
import json
import os
class NewRecipe(View):
    def get(self, request):
        return render(request, "customer/new_recipe.html")

class Result3(View):
    template_name = 'customer/new_recipe.html'
    cache = TTLCache(maxsize=100, ttl=1800)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        flavor = request.POST.get('flavor')
        nose = request.POST.get('nose')
        mood = request.POST.get('mood')
        alcohol_level = request.POST.get('alcohol_level')

        new_recipe = self.generate_cocktail_recipe(flavor, nose, mood, alcohol_level)
        translated_recipe = self.translate_recipe(new_recipe)

        context = {
            'flavor': flavor,
            'nose': nose,
            'mood': mood,
            'alcohol_level': alcohol_level,
            'translated_recipe': translated_recipe
        }
        return render(request, 'customer/result3.html', context)

    def generate_cocktail_recipe(self, flavor, nose, mood, alcohol_level):
        cache_key = f"{flavor}_{nose}_{mood}_{alcohol_level}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        prompt = f"Generate a cocktail recipe with a {flavor} flavor, nose {nose}, {mood} mood, and {alcohol_level} alcohol level. Recipe:"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates cocktail recipes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.9
        )
        
        recipe = response.choices[0].message['content'].strip()
        self.cache[cache_key] = recipe
        
        return recipe

    def translate_recipe(self, recipe):
        translation_prompt = f"레시피: {recipe}\n스타일: 자연스러운 한국어로 번역해주세요.칵테일명: 에 칵테일 이름을 적고 불필요한건 적지않습니다,레시피: 는 뺴주세요,칵테일명: 은 하나면충분"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates cocktail recipes."},
                {"role": "user", "content": translation_prompt}
            ],
            max_tokens=500,
            temperature=0.9
        )
        
        translated_recipe = response.choices[0].message['content'].strip()
        return translated_recipe

cache = TTLCache(maxsize=100, ttl=1800)
class CocktailInfo(View):
    def get(self, request):
        return render(request, "customer/cocktail_info.html")
    

class Result2(View):
    template_name = 'customer/cocktail_info.html'
    translator = googletrans.Translator()
    cache = TTLCache(maxsize=100, ttl=1800)

    def get(self, request):
        return render(request, 'customer/cocktail_info')

    def post(self, request):
        user_input = request.POST.get('user_input')

        # 두 번째 코드 조각 (칵테일 정보와 번역)
        if 'search_cocktail' in request.POST:
            return self.search_cocktail(request, user_input)

    def search_cocktail(self, request, user_input):
        cache_key = f"info_{user_input}"
        
        if cache_key in self.cache:
            translated_info = self.cache[cache_key]
        else:
            prompt = f"Provide information and recipe for the cocktail: {user_input}. Information:"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides information and recipes for cocktails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9
            )
            
            info = response.choices[0].message['content'].strip()
            translated_info = self.translator.translate(info, src='en', dest='ko').text
            self.cache[cache_key] = translated_info

        context = {
            'user_input': user_input,
            'translated_info': translated_info
        }
        return render(request, 'customer/result2.html', context)


class Recommend(View):
    def get(self, request):
        return render(request, "customer/recommend.html")
class Result(View):
    def post(self, request):
        user_input = request.POST.get('user_input')

        # 가상의 주류 데이터
        beers = []

        file_path = os.path.join(os.path.dirname(__file__), 'last1.jsonl')
        # JSONL 파일 불러오기
        with open(file_path, 'r') as jsonl_file:
            for line in jsonl_file:
                entry = json.loads(line)
                beers.append(entry)

        # GPT API 키 설정
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # GPT API를 사용하여 설명 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # GPT-3 채팅 모델 선택
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides information about beers."},
                {"role": "user", "content": user_input}
            ]
        )
        generated_description = response.choices[0].message["content"].strip()

        # 주류 데이터에서 사용자 입력에 맞는 주류 찾기
        matching_beers = []
        for beer in beers:
            if user_input.lower() in beer['prompt'].lower():
                matching_beers.append(beer)

        # 추천 출력
        recommended_beer = None
        if matching_beers:
            recommended_beer = matching_beers[0]  # 첫 번째 추천만 출력

        context = {
            'user_input': user_input,
            'generated_description': generated_description,
            'recommended_beer': recommended_beer['completion']
        }
        return render(request, 'customer/result.html', context)

    def get(self, request):
        return render(request, 'customer/recommend.html')
    
class Service(View):
    def get(self, request):
        return render(request, "customer/service.html")
        
class Index(View):
    def get(self, request):
        return render(request, "customer/index.html")
    
class Alcohol(View):
    def get(self, request):
        return render(request, 'customer/alcohol.html')

class Recommend(View):
    def get(self, request):
        return render(request, "customer/recommend.html")
    
class Jin_list(View):
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM jins"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)

        except:
            connection.rollback()
            print("Failed selecting in Jin_list")

        return render(request, 'customer/Jin_list.html', {'alcohols': alcohols})
    
class Whisky_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM whiskys"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
            
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/whisky_list.html', {'alcohols':alcohols})

class Beer_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM beers"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
            
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/beer_list.html', {'alcohols': alcohols})

class Cognac_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM cognacs"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
                
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")

            
        return render(request, 'customer/cognac_list.html', {'alcohols': alcohols})

class Liqueur_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM liqueurs"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
            
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/liqueur_list.html', {'alcohols': alcohols})

class Rum_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM rums"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
                
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/rum_list.html', {'alcohols': alcohols})

class Sake_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM sakes"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
            
            
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/sake_list.html', {'alcohols': alcohols})

class Tequila_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM tequilas"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
            
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/tequila_list.html', {'alcohols': alcohols})

class Vodka_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM vodkas"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
                
            
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/vodka_list.html', {'alcohols': alcohols})

class Wine_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM wines"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
                
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/wine_list.html', {'alcohols':alcohols})
    
class Bbaigan_list(View):
    # items = Item.objects.all()
    def get(self, request):
        try:
            cursor = connection.cursor()

            strSql = "SELECT name, Aroma, Taste, Finish, Kind, Alcohol FROM bbaigans"
            result = cursor.execute(strSql)
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            alcohols = []
            for data in datas:
                row = {'name': data[0],
                       'Aroma': data[1],
                       'Taste': data[2],
                       'Finish': data[3],
                       'Kind': data[4],
                       'Alcohol': data[5],
                       }
                
                alcohols.append(row)
                
        except:
            connection.rollback()
            print("Failed selecting in ItemlisView")


        return render(request, 'customer/bbaigan_list.html', {'alcohols':alcohols})
    
