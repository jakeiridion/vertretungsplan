import requests
from bs4 import BeautifulSoup
import time
from prettytable import PrettyTable


class Fetcher():
    def fetch(self):
        start_url = "https://klengymuc.eltern-portal.org/"
        post_url = "https://klengymuc.eltern-portal.org/includes/project/auth/login.php"
        end_url = "https://klengymuc.eltern-portal.org/service/vertretungsplan"
        login_data = {"username": "",
                      "password": ""}

        with requests.session() as s:
            time.sleep(0.5)
            r = s.get(start_url)
            r = s.post(post_url, data=login_data)
            r = s.get(end_url)
            soup = BeautifulSoup(r.text, "html.parser")

        first_time = 0
        x = 0
        last = 0
        i = 0
        liste1 = []
        liste2 = []

        for line in soup.find("div", attrs={"class": "main_center"}):
            if x == 0:
                # print(soup.find_all("div", attrs={"class": "list bold full_width text_center"})[first_time].text)
                global date
                date = line.text
                x = 1

            if "table" in str(line):
                for tr in line.find_all("tr"):
                    for td in tr.find_all("td"):
                        # print(td.text, end=" ")
                        liste1.append(td.text)

                    if i < 2:
                        liste2.append(date)
                        i = i + 1

                    liste2.append(":".join(liste1))
                    liste1 = []

                if last == 1:
                    break

                first_time = 1
                last = 1
                x = 0

        return liste2

    def ausgabe(self):
        t = PrettyTable(['Std', 'Vertretung', "Fach", "Raum", "Info"])
        for i in f.fetch():
            if "KW" in i:
                print(i + ":")

            if "Keine Vertretungen" in i:
                print(i)
                print("\n")

            if ":" in i:
                if "Std.:Vertretung:Fach:Raum:Info" in i:
                    continue
                x = i.split(":")
                t.add_row(x)

        return t


f = Fetcher()
print(f.ausgabe())
