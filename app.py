from bs4 import BeautifulSoup
import os
from selenium import webdriver   
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def home():
    if request.args.get('a'):
        url = f"https://www.withtally.com/voter/{request.args.get('a')}/governance/gitcoin"
    else:
        return "Enter Address in the URL"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-sh-usage')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    # executable_path param is not needed if you updated PATH
    browser = webdriver.Chrome(options=options, executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    browser.get(url)

    page = browser.page_source
    soup = BeautifulSoup(page, features="html.parser")
    filter=soup.find_all("p")
    #for i in range(0,  len(filter)):
    #    print(f"{i}-{filter[i].get_text()}")
    #print(filter)
    #browser.close()
    browser.quit()
    data = {
        'address':filter[3].text,
        'name': filter[4].text, 
        'Last_participation_date': filter[5].text,
        'Total_participation_rate': filter[6].text,
        'Total_votes': filter[8].text,
        'Total_ballots': filter[9].text,
        'Total_tokens': filter[10].text,
        'Voting_weight': filter[11].text,
        'Own_votes': filter[16].text
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)