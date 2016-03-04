import collections
import re
import urllib.request

class WebCrawler:

    # reg ex pattern for absolute path of links
    RegExPat = re.compile(r'<a\shref\s*=\s*"(https?.*?)"', re.M)

    RegExTitlePat = re.compile(r'<a\shref\s*=\s*"[https].+?".*?>(.*?)<.*?', re.M | re.S)

    #RegExTitlePat = re.compile(r'<a\shref\s*=\s*"[https].+?".*>(.+?)</a>', re.MULTILINE)

    htmlFile = open("html.txt", 'w')

    '''
    ' Constructs a WebCrawler - contains # of links found, frequency of words in link text,
    ' and links to pages.
    '''
    def __init__(self):
        self.page_to_links_dict = collections.OrderedDict()
        self.word_to_freq_dict = collections.OrderedDict()
        self.page_tracker = list()
        self.pages_processed = 0


    def crawl(self, url_list):
        idx_count = 0
        print(url_list)
        while idx_count < len(url_list):
            url = url_list[idx_count]
            #print("shit")
            #if not self.page_to_links_dict.__contains__(url):
            try:
                page = urllib.request.urlopen(url)
                links_on_page = []
                titles_of_links = []
                for line in page:
                    WebCrawler.htmlFile.write(str(line))
                    tmp_link_list = re.findall(WebCrawler.RegExPat, str(line))
                    tmp_txt_list = re.findall(WebCrawler.RegExTitlePat, str(line))
                        #print("hi")
                    if tmp_link_list:
                        links_on_page.extend(tmp_link_list)
                    if tmp_txt_list:
                        titles_of_links.extend(tmp_txt_list)
                unique_links_list = list(set(links_on_page))
                self.page_to_links_dict.update({url: unique_links_list})
            except urllib.error.URLError:
                self.page_to_links_dict.update({url: None})
            except urllib.error.HTTPError:
                self.page_to_links_dict.update({url: None})
            except urllib.error.ContentTooShortError():
                self.page_to_links_dict.update({url: None})
            idx_count += 1
            self.page_tracker.append(url)
            #else:
                #idx_count += 1
        #print(len(linksonpage))
        #print(len(linktitles))
        #print(linksonpage)


    '''
    ' This function is used to remove links from list and add
    ' them to a dictionary
    '''
    #def buildcrawlspace(self, currenturl, listoflinks):
        #for index in listoflinks:



    '''
    ' This function is used to place words from url titles into a dictionary.
    ' If the word exists in dictionary then the frequency is updated; otherwise
    ' it is added to dictionary and frequency is set to 1
    '''
    def addwordfreq(self, word):
        if word in self.word_to_freq_dict:
            self.word_to_freq_dict[word] += 1
        else:
            self.word_to_freq_dict.update({word: 1})


#crawl1 = WebCrawler("http://www.cosc.canterbury.ac.nz/mukundan/dsal/MSort.html")
#crawl3 = WebCrawler("http://einstein.biz/")
#crawler = WebCrawler()
#crawler.crawl("https://www.google.com")
#crawler.crawl("http://www.cosc.canterbury.ac.nz/mukundan/dsal/MSort.html")
#crawler.crawl("https://github.com")
#crawler.crawl("http://einstein.biz/")
#print(crawler.page_to_links_dict)
#print(crawler.total_links_found)


if __name__ == "__main__":
    main_urls = []
    main_urls.extend(open("url.txt", 'r').read().splitlines())
    crawler = WebCrawler()
    crawler.crawl(main_urls)
    while crawler.page_tracker:
        page = crawler.page_tracker.pop(-len(crawler.page_tracker) + 1)
        print("The page being processed: { }", page)
        crawler.crawl(crawler.page_to_links_dict.get(page))
        crawler.pages_processed += 1
        print("Pages processed: { }", crawler.pages_processed)
        print()


    print(crawler.page_to_links_dict)
    print(crawler.page_tracker)
    print(crawler.pages_processed)

