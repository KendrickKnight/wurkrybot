from playwright.sync_api import sync_playwright
import time
import json

def main():
    print("Reporter reporting in!")
    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=True)
        page =  browser.new_page()
        page.goto("https://littlewargame.com/play/", timeout = 0)

        def report():
            source =  page.locator("#gamesWindowTextArea p")
            players_source = page.locator("#playersListOnline p")
            print(source)

            data = {
                "searching" : False,
                "lobbies" : []
            }
            for i in range(players_source.count()):
                player_status = players_source.nth(i).locator(".lobbyLabel").text_content()
                if player_status.replace(" ","") == "(searching)":
                    print("someone is searching!")
                    data["searching"] = True

            for i in range(source.count()):
                ld = { #ld = lobby details
                    "name" : "",
                    "host" : "",
                    "map" : "",
                    "player_count" : "",
                    "running": False,
                    "locked" : False
                }
                attribute_data =  source.nth(i).get_attribute("title").split(" | ")
                content_data =  source.nth(i).text_content()
                

                if content_data[-8:-1] == 'running':
                    ld.update({'running': True})
                    ld.update({'name': content_data[0:-15]})
                    ld.update({'player_count':content_data[-14:-8]})
                else:
                    ld.update({'name': content_data[0:-6]})
                    ld.update({'player_count':content_data[-6:-1]})

                ld.update({'host':attribute_data[0][6:]})
                ld.update({'map':attribute_data[2][5:]})

                if source.nth(i).locator('img').count() > 0:
                    ld.update({'locked': True})

                data["lobbies"].append(ld)

            with open('data.json', "w") as file:
                json.dump(data, file, indent=4)
        
        while True:
            report()
            time.sleep(2)

        browser.close

main()