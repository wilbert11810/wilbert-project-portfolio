from bs4 import BeautifulSoup
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")


empire_webpage = response.text

soup = BeautifulSoup(empire_webpage, "html.parser")

movie_title = soup.find_all("h3", class_="title")
top_100 = [movie.getText() for movie in movie_title[::-1]]

with open('movies.txt', 'a', encoding="utf-8") as file:
    for name in top_100:
        file.write(f"{name}\n")
