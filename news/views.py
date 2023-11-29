from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NewsSerializer


class NewsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sites = ['https://zamin.uz/uz/']
        news_list = []

        for site in sites:
            try:
                response = requests.get(site)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                short_item_divs = soup.find_all('div', class_='short-item')

                for tags in short_item_divs:
                    title_element = tags.find('a', class_='short-title')
                    content_element = tags.find('p')
                    image_element = f"https://zamin.uz/{tags.find('a', class_='short-img').find('img')['src']}"
                    link = tags.find('a', class_='short-img')['href']

                    if title_element and content_element:
                        title = title_element.text.strip()
                        content = content_element.text.strip()

                        news_data = {
                            'title': title,
                            'content': content,
                            'image_url': image_element,
                            'link': link,
                        }

                        serializer = NewsSerializer(data=news_data)
                        if serializer.is_valid():
                            serializer.save()
                            news_list.append(serializer.data)

            except requests.RequestException as e:
                print(f"Error fetching data from {site}: {e}")

        # Use Response instead of JsonResponse
        return Response(news_list)
