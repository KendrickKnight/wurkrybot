from playwright.sync_api import sync_playwright
import time
import json

print("Reporter reporting in!")
with sync_playwright() as p:
    browser =  p.chromium.launch(headless=True)
    page =  browser.new_page()
    page.goto("https://littlewargame.com/play/", timeout = 0)

    def check_connection():
        element = page.query_selector("#NoConnectionWindow")
        with open("data.json", 'r') as data:
            data = json.load(data)
        
        with open('data.json','w') as wdata:
            if element:
                data["connection"] = False
                json.dump(data,wdata,indent=4)
                return False
            else:
                data["connection"] = True
                json.dump(data,wdata,indent=4)
                return True


    def report():
        source =  page.locator("#gamesWindowTextArea p")
        players_source = page.locator("#playersListOnline p")

        with open("data.json","r") as df:
            dfile = json.load(df)

        data = {
            "searching" : False,
            "lobbies" : [],
            "connection" : False
        }

        data["connection"] = dfile["connection"]

        for i in range(players_source.count()):
            player_status = players_source.nth(i).locator(".lobbyLabel").text_content()
            if player_status.replace(" ","") == "(searching)":
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
        if  check_connection() == True:
            report()
        else:
            page.reload()
        time.sleep(2)

    browser.close
