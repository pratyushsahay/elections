import requests
import string
import csv
from bs4 import BeautifulSoup


def write_mayor_election_data_to_csv(URL):
    # Set up a fake user agent bc the site does not allow GET requests w/o one
    headers = {'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    soup = get_html_content(URL, headers)

    rowsArray = []
    rows = []
    for tr in soup.find_all('table')[0].find_all('tr'):
        for td in tr.find_all("td"):
            rows.append(td.text.strip().encode("utf-8"))
        rowsArray.append(rows)
        rows = []

    rowsArrayFormatted = []
    rowFormatted = []
    for row in rowsArray:
        for val in row:
            printable = set(string.printable)
            non_ascii_removed_string = ''.join(filter(lambda x: x in printable, val.decode("utf-8")))
            rowFormatted.append(non_ascii_removed_string.replace(',',''))
        rowsArrayFormatted.append(rowFormatted)
        rowFormatted = []   

    # Write the data to csv
    with open("data/mayorelections2020.csv", "w+") as mayorelections2020:
        csvWriter = csv.writer(mayorelections2020, delimiter=',')
        csvWriter.writerows(rowsArrayFormatted)


def write_upcoming_election_data_to_csv(URL):
    soup = get_html_content(URL, None)

    rowsArray = []
    rows = []
    for tr in soup.find_all('table')[5].find_all('tr'):
        for th in tr.find_all("th"):
            rows.append(th.text.strip())
        for td in tr.find_all("td"):
            rows.append(td.text.strip())
        rowsArray.append(rows)
        rows = []

    # Write the data to csv
    with open("data/upcomingelections.csv", "w+") as upcomingelections:
        csvWriter = csv.writer(upcomingelections, delimiter=',')
        csvWriter.writerows(rowsArray)


def get_html_content(URL, headers):
    html_content = ''
    if headers is None:
        html_content = requests.get(URL).text
    else:
        html_content = requests.get(URL, headers=headers).text
    
    return BeautifulSoup(html_content, 'html.parser')


def main():
    write_mayor_election_data_to_csv('https://www.usmayors.org/elections/election-results-2/')
    write_upcoming_election_data_to_csv('https://en.wikipedia.org/wiki/Elections_in_the_United_States')


if __name__ == '__main__':
    main()
