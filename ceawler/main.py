import argparse
import sys
from time import sleep
from bs4 import BeautifulSoup
import config  # Импортируем конфигурацию

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import (QApplication, QHeaderView, QMainWindow,
                             QTableWidget, QTableWidgetItem)
from pystyle import Colors, Colorate

CEAWLER_ASCII = """
 ▄████████    ▄████████    ▄████████  ▄█     █▄   ▄█          ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███ ███     ███ ███         ███    ███   ███    ███ 
███    █▀    ███    █▀    ███    ███ ███     ███ ███         ███    █▀    ███    ███ 
███         ▄███▄▄▄       ███    ███ ███     ███ ███        ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███        ▀▀███▀▀▀     ▀███████████ ███     ███ ███       ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    █▄    ███    █▄    ███    ███ ███     ███ ███         ███    █▄  ▀███████████ 
███    ███   ███    ███   ███    ███ ███ ▄█▄ ███ ███▌    ▄   ███    ███   ███    ███ 
████████▀    ██████████   ███    █▀   ▀███▀███▀  █████▄▄██   ██████████   ███    ███ 
                                                 ▀                        ███    ███ 
                        sait: sozidarov.github.io/ceawler/   
"""

def print_gradient_text():
    print(Colorate.Vertical(Colors.yellow_to_red, CEAWLER_ASCII))

class PlatformChecker:
    def __init__(self, username=None, email=None, browser_query=None, phone=None):
        self.username = username
        self.email = email
        self.browser_query = browser_query
        self.phone = phone  # Добавляем phone
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.platforms = [
            # Социальные сети
            ('GitHub', f'https://github.com/{username}', self.check_standard),
            ('Instagram', f'https://instagram.com/{username}', self.check_instagram),
            ('Twitter', f'https://twitter.com/{username}', self.check_twitter),
            ('Facebook', f'https://facebook.com/{username}', self.check_facebook),
            ('Reddit', f'https://reddit.com/user/{username}', self.check_standard),
            ('LinkedIn', f'https://linkedin.com/in/{username}', self.check_linkedin),
            
            # Медиа
            ('YouTube', f'https://youtube.com/@{username}', self.check_youtube),
            ('TikTok', f'https://tiktok.com/@{username}', self.check_tiktok),
            ('Twitch', f'https://twitch.tv/{username}', self.check_standard),
            ('Vimeo', f'https://vimeo.com/{username}', self.check_standard),
            
            # Блоги
            ('Medium', f'https://medium.com/@{username}', self.check_medium),
            ('WordPress', f'https://{username}.wordpress.com', self.check_standard),
            
            # Технологии
            ('Stack Overflow', f'https://stackoverflow.com/users/{username}', self.check_stackoverflow),
            ('GitLab', f'https://gitlab.com/{username}', self.check_standard),
            
            # Дополнительные платформы (50+)
            ('Pinterest', f'https://pinterest.com/{username}', self.check_standard),
            ('Flickr', f'https://flickr.com/people/{username}', self.check_standard),
            ('DeviantArt', f'https://deviantart.com/{username}', self.check_standard),
            ('Behance', f'https://behance.net/{username}', self.check_standard),
            ('VK', f'https://vk.com/{username}', self.check_standard),
            ('Steam', f'https://steamcommunity.com/id/{username}', self.check_standard),
            ('SoundCloud', f'https://soundcloud.com/{username}', self.check_standard),
            ('Last.fm', f'https://last.fm/user/{username}', self.check_standard),
            ('Goodreads', f'https://goodreads.com/{username}', self.check_standard),
            ('Fiverr', f'https://fiverr.com/{username}', self.check_standard),
            ('Etsy', f'https://etsy.com/people/{username}', self.check_standard),
            ('Ebay', f'https://ebay.com/usr/{username}', self.check_standard),
            ('Keybase', f'https://keybase.io/{username}', self.check_standard),
            ('HubPages', f'https://hubpages.com/@{username}', self.check_standard),
            ('Instructables', f'https://instructables.com/member/{username}', self.check_standard),
            ('Patreon', f'https://patreon.com/{username}', self.check_standard),
            ('Wikipedia', f'https://en.wikipedia.org/wiki/User:{username}', self.check_standard),
            ('Slideshare', f'https://slideshare.net/{username}', self.check_standard),
            ('Dribbble', f'https://dribbble.com/{username}', self.check_standard),
            ('500px', f'https://500px.com/p/{username}', self.check_standard),
            ('Gravatar', f'https://gravatar.com/{username}', self.check_standard),
            ('Codepen', f'https://codepen.io/{username}', self.check_standard),
            ('Bitbucket', f'https://bitbucket.org/{username}', self.check_standard),
            ('HackerNews', f'https://news.ycombinator.com/user?id={username}', self.check_standard),
            ('ProductHunt', f'https://producthunt.com/@{username}', self.check_standard),
            ('Telegram', f'https://t.me/{username}', self.check_telegram),
            ('Tumblr', f'https://{username}.tumblr.com', self.check_standard),
            ('Blogger', f'https://{username}.blogspot.com', self.check_standard),
            ('Kickstarter', f'https://kickstarter.com/profile/{username}', self.check_standard),
            ('Pastebin', f'https://pastebin.com/u/{username}', self.check_standard),
            ('Roblox', f'https://roblox.com/user.aspx?username={username}', self.check_standard),
            ('Wikipedia', f'https://en.wikipedia.org/wiki/User:{username}', self.check_standard),
            ('Bandcamp', f'https://bandcamp.com/{username}', self.check_standard),
            ('CashApp', f'https://cash.app/£{username}', self.check_standard),
            ('Venmo', f'https://venmo.com/{username}', self.check_standard),
            ('PayPal', f'https://paypal.me/{username}', self.check_standard),
            ('Imgur', f'https://imgur.com/user/{username}', self.check_standard),
            ('Spotify', f'https://open.spotify.com/user/{username}', self.check_standard),
            ('ReverbNation', f'https://reverbnation.com/{username}', self.check_standard),
            ('Letterboxd', f'https://letterboxd.com/{username}', self.check_standard),
            ('Trakt', f'https://trakt.tv/users/{username}', self.check_standard),
            ('Scribd', f'https://scribd.com/{username}', self.check_standard),
            ('SlideShare', f'https://slideshare.net/{username}', self.check_standard),
            ('Houzz', f'https://houzz.com/user/{username}', self.check_standard),
            ('Vine', f'https://vine.co/{username}', self.check_standard)
        ]

        self.email_platforms = [
            ('HaveIBeenPwned', f'https://haveibeenpwned.com/api/v3/breach/{email}', self.check_hibp),
            ('Gravatar', f'https://gravatar.com/{email}', self.check_standard),
            ('Keybase', f'https://keybase.io/{email}', self.check_standard),
            ('Skype', f'https://web.skype.com/{email}', self.check_standard),
        ]

    def check_telegram(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return "tgme_username" in response.text
        except:
            return False

    def check_youtube(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "channel/@" in response.url
        except:
            return False

    def check_instagram(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "login" not in response.url
        except:
            return False
        
    def check_medium(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "404" not in response.text
        except:
            return False

    def check_wikipedia(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "User does not exist" not in response.text
        except:
            return False
        
    def check_twitter(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "screen-name" in response.text
        except:
            return False

    def check_tiktok(self, url):
        try:
            response = requests.head(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_facebook(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "facebook.com/help/" not in response.text
        except:
            return False
        
    def check_stackoverflow(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "Page Not Found" not in response.text
        except:
            return False
        
    # Добавляем недостающие методы проверки
    def check_reddit(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "empty" not in response.text
        except:
            return False

    def check_linkedin(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "authwall" not in response.url
        except:
            return False

    def check_twitch(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "404" not in response.text
        except:
            return False

    def check_quora(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "Profile Not Found" not in response.text
        except:
            return False

    def check_steam(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200 and "The specified profile could not be found" not in response.text
        except:
            return False

    def check_standard(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_hibp(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            print(f"HIBP: {url} - Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"HIBP Error: {url} - {str(e)}")
            return False
    
    def check_standard(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            print(f"Standard: {url} - Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Standard Error: {url} - {str(e)}")
            return False

    def google_search(self, query, api_key="AIzaSyBdXi8Uu8AUaubae_HVmt3G8J8k7L_6G9w", cx="30ce51494017a465c", num=3):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"q": query, "key": api_key, "cx": cx, "num": num}
        try:
            response = requests.get(url, params=params)
            return response.json().get("items", [])
        except Exception as e:
            print(f"Ошибка Google API: {e}")
            return []

    def get_github_info(self, username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {"name": data.get("name"), "bio": data.get("bio"), "repos": data.get("public_repos"), "link": data.get("html_url")}
        return None

    def fetch_website_data(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "No title"
            return {"title": title, "url": url, "content": soup.get_text()[:200] + "..."}
        except:
            return None

    def process_browser_query(self, query):
        google_results = self.google_search(query)
        github_data = None
        if "username:" in query:
            username = query.split("username:")[1].strip()
            github_data = self.get_github_info(username)

        links = [result["link"] for result in google_results[:3]]
        website_data = [self.fetch_website_data(link) for link in links if link]

        results = []
        for item in google_results:
            results.append(("Google", f"{item['title']}: {item['link']}"))
        if github_data:
            results.append(("GitHub", f"{github_data['name']} - {github_data['link']}"))
        for site in website_data:
            if site:
                results.append(("Website", f"{site['title']} - {site['url']}"))
        return results
    
    def check_phone(self, phone):
        try:
            url = "https://cleaner.dadata.ru/api/v1/clean/phone"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Token {config.DADATA_TOKEN}",
                "X-Secret": config.DADATA_SECRET
            }
            data = [phone]  # DaData принимает список значений
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()[0]  # Берем первый результат
            if response.status_code == 200:
                return [
                    ("Phone", f"Номер: {result['phone']}"),
                    ("Type", f"Тип: {result['type']}"),
                    ("Provider", f"Оператор: {result['provider']}"),
                    ("Country", f"Страна: {result['country']}"),
                    ("Region", f"Регион: {result['region']}"),
                    ("City", f"Город: {result['city']}"),
                    ("Timezone", f"Часовой пояс: {result['timezone']}")
                ]
            return [("Phone", "Ничего не найдено")]
        except Exception as e:
            print(f"Ошибка DaData: {e}")
            return [("Phone", f"Ошибка: {str(e)}")]
    def check_all(self):
        results = []
        if self.username:
            platforms_to_check = self.platforms
            target = self.username
            print(f"Поиск пользователя: {target}")
        elif self.email:
            platforms_to_check = self.email_platforms
            target = self.email
            print(f"Поиск по email: {target}")
        elif self.browser_query:
            print(f"Поиск в браузере: {self.browser_query}")
            return self.process_browser_query(self.browser_query)
        elif self.phone:
            print(f"Поиск по номеру телефона: {self.phone}")
            return self.check_phone(self.phone)

        total = len(platforms_to_check)
        for i, (platform, url, checker) in enumerate(platforms_to_check):
            progress = (i + 1) / total * 100
            self.print_progress(progress)
            if checker(url):
                results.append((platform, url))
            sleep(0.2)
        print("\n")
        return results

    @staticmethod
    def print_progress(percent):
        bar_length = 30
        filled = int(bar_length * (percent / 100))
        bar = '█' * filled + ' ' * (bar_length - filled)
        orange = '\033[38;2;255;165;0m'
        reset = '\033[0m'
        print(f"{orange}[{bar}] {percent:.0f}%{reset}", end='\r')

class ResultsWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Результаты поиска")
        self.setGeometry(300, 300, 800, 400)
        self.initUI(data)

    def initUI(self, data):
        self.table = QTableWidget(self)
        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Платформа', 'Ссылка'])

        for row, (platform, url) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(platform))
            self.table.setItem(row, 1, QTableWidgetItem(url))
            self.table.item(row, 1).setForeground(QBrush(QColor(255, 165, 0)))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                color: #FFA500;
                font-size: 14px;
                border: 2px solid #FFA500;
            }
            QHeaderView::section {
                background-color: #FFA500;
                color: #000000;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

        self.setCentralWidget(self.table)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='Имя пользователя для поиска')
    parser.add_argument('--email', help='Email для поиска')
    parser.add_argument('--cbrowser', action='store_true', help='Поиск через браузер')
    parser.add_argument('--phone', help='Номер телефона для поиска')  # Добавляем --phone
    args = parser.parse_args()

    if not args.username and not args.email and not args.cbrowser and not args.phone:
        parser.error("Требуется указать хотя бы один параметр: --username, --email, --cbrowser или --phone")

    print_gradient_text()

    query = None
    if args.cbrowser:
        query = input("Введите запрос: ")

    checker = PlatformChecker(
        username=args.username,
        email=args.email,
        browser_query=query,
        phone=args.phone  # Передаем phone
    )
    results = checker.check_all()

    if not results:
        print("Ничего не найдено.")

    app = QApplication(sys.argv)
    window = ResultsWindow(results)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()