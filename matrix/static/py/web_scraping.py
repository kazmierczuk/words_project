import urllib.request
from bs4 import BeautifulSoup as bs

# BeautifulSoup and requests used to scrape basic definition of a word
class Definition():

    def __init__(self, word):
        htmlfile = None
        self.word = word
        url = "https://www.freedictionary.com/" + word # my online dictionary of choice
        # Chceck if there is a definition
        try:
            htmlfile = urllib.request.urlopen(url)
        # If not but the word is plural, try withhout an 's' at the end
        except:
            if word[-1].upper() == 'S':
                url = url[:-1]
                # Try again, this time if no response from dictionary webside: just pass :)
                try:
                    htmlfile = urllib.request.urlopen(url)
                except:
                    pass

        # Assign definition to this obj or set it to "no def. available"
        if htmlfile:
            soup = bs(htmlfile, 'lxml')
            self.short_def = soup.find(class_="definitions")
            try:
                self.short_def = self.short_def.get_text()
            except AttributeError:
                self.short_def = "No definition available."
        else:
            self.short_def = "No definition available."
