import requests
from bs4 import BeautifulSoup as soup
import csv
from datetime import datetime
import re


def page_parser(req_url):
    try:
        req = requests.get(req_url)
        page_soup = soup(req.content, "html.parser")
        return page_soup
    except :
        pass


def main():
    try:
        csv_file_name = datetime.now().strftime("%d%b%Y%H%M%S") + "_news_look_up_.csv"
        with open(csv_file_name, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(["Headline", "Pub_DateTime", "Outlet", "Link"])

            print("input the search for : ")
            input_txt = str(input().strip())

            search_url = "https://newslookup.com/results?p="+str(1)+"&q=" + input_txt + "&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5"

            page_soup = page_parser(search_url)

            try:
                no_of_pages = page_soup.findAll("div", {"class", "col-md-8"})
                total_pages = int(no_of_pages[0].findAll("p")[-1].text.strip().split(" ")[-1])+1
            except:
                total_pages = 2
                pass

            j = 1
            for index in range(1, total_pages):
                try:
                    page_url = "https://newslookup.com/results?p="+str(index)+"&q=" + input_txt + "&dp=5&mt=-1&ps=10&s=&cat=-1&fmt=&groupby=no&site=&dp=5"

                    page_soup = page_parser(page_url)

                    container = page_soup.findAll("div", {"id": "run1"})
                    title_and_link_lst = container[0].findAll("a", {"class": "title"})
                    lst_tag = container[0].findAll("p", {"class": "grp"})

                    for i in range(len(title_and_link_lst)):
                        try:
                            head_line = title_and_link_lst[i].text.strip()

                            link = ''
                            try:
                                link = title_and_link_lst[i]['href']
                            except:
                                pass

                            outlet = ''
                            try:
                                html_tag = u""
                                for tag in title_and_link_lst[i].next_siblings:
                                    if tag == lst_tag[i]:
                                        break
                                    else:
                                        html_tag += str(tag)

                                outlet_lst = re.findall(r'<a class="source" href="(.*?)</a>', html_tag)

                                outlet = outlet + outlet_lst[0].split('">')[1]
                                outlet = outlet +"; " + outlet_lst[1].split('">')[1]
                                outlet = outlet +"; " + outlet_lst[2].split('">')[1]
                            except:
                                pass

                            pub_DateTime = ''
                            try:
                                pub_DateTime = re.findall(r'<span class="stime">(.*?)</span>', html_tag)[0]
                            except:
                                pass

                            csv_writer.writerow([head_line, pub_DateTime, outlet, link])

                            print(str(j) + ". " + head_line)
                            j += 1

                        except:
                            pass
                except:
                    pass
    except:
        pass


if __name__ == '__main__':
    main()