import requests
from bs4 import BeautifulSoup

class API:
    def __init__(self, anime_name:str, ep_num:int):
        # Anime Info
        if len(str(ep_num)) == 1:
            self.ep_num = "episode-" + "0" + str(ep_num)
        else: 
            self.ep_num = "episode-" + str(ep_num)

        self.anime_name = anime_name.replace(" ", "-")
        self.complete_ep_name = f"https://simply.moe/{self.anime_name}"+ f"-{self.ep_num}"

        # Anime website settup
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
        self.url = requests.get(f"https://simply.moe/anime/{self.anime_name}", headers=self.headers)
        self.anime_serie = BeautifulSoup(self.url.content, 'html.parser')

        # Anime List containers
        self.anime_ep_list = []
        self.anime_episode_link = []

        # Anime Episode Link list
        self.anime_episode_website_list = []

        # Search for anime
        if self.exist() == True:
            self.download_episode()

        else:
            pass

    def exist(self):
        if "Page not found" in str(self.anime_serie.title):
            return False

        else:
            return True

    def get_episode(self):
        # Append all links to anime_ep_list
        for link in self.anime_serie.find_all('a'):
            self.anime_ep_list.append(str(link.get('href')))

        # Looks for anime episode with corresponding episode number
        for ep in self.anime_ep_list:
            if self.complete_ep_name in str(ep):
                self.anime_episode_link.append(str(ep))

            else:
                pass
            
        return requests.get(self.anime_episode_link[0], headers=self.headers)

    def download_episode(self):
        self.anime_ep_link = self.get_episode()
        self.anime_episode = BeautifulSoup(self.anime_ep_link.content, 'html.parser')
        
        for link in self.anime_episode.find_all('a'):
            if "mp4" in str(link):
                self.anime_episode_website_list.append(str(link.get('href')))

        for i in self.anime_episode_website_list:
            print(i)
            input("Click ctrl+S or cmd+S to save mp4 vid")

if __name__ == '__main__':
    api = API("shingeki no kyojin", 1)