from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(level=logging.DEBUG,filename="scrapper.log",format="%(levelname)s : %(filename)s : %(message)s : %(asctime)s")

class Website():
    def __init__(self,searchstring):
        try:
            searchstring.replace(" ","")
            self._flipkart_url="https://www.flipkart.com/search?q="+ searchstring
            logging.info("url for product successfully created")
        except Exception as e:
            logging.error("Failed to create product url",e)
    def search_result_scrapper(self):
        try:
            logging.info("Generating url for product")
            self.uclient=uReq(self._flipkart_url)
            self.flipkart_page=self.uclient.read()
            self.uclient.close()
            self.flipkart_html=bs(self.flipkart_page,"html.parser")
            logging.info("Generating url for product successfully")
            return self.flipkart_html
        except Exception as e:
            logging.error("Error generating url for product ",e)

class Product_Scrapper(Website):
    def __init__(self,searchstring=None):
        super().__init__(searchstring)
        self.searchStr=searchstring
    
    def individual_products(self):
        try:
            self.a=super(Product,self).search_result_scrapper()
            self.bigboxes = self.a.findAll("div", {"class": "_1AtVbE col-12-12"})
            del self.bigboxes[0:3]
            self.box = self.bigboxes[0]
            self.productLink = "https://www.flipkart.com" + self.box.div.div.div.a['href']
            self.prodRes = requests.get(self.productLink)
            self.prodRes.encoding='utf-8'
            self.prod_html = bs(self.prodRes.text, "html.parser")
            print(self.prod_html)
            self.commentboxes = self.prod_html.find_all('div', {'class': "_16PBlm"})
            return self.commentboxes
        except Exception as e:
            logging.error("Error parsing",e)
            return "Error occurred during parsing"
    
    def savingComments(self):
        try:
            self.filename = self.searchStr + ".csv"
            self.fw = open(self.filename, "w")
            self.headers = "Product, Customer Name, Rating, Heading, Comment \n"
            self.fw.write(self.headers)
            self.reviews = []
            for commentbox in self.individual_products():
                try:
                    #name.encode(encoding='utf-8')
                    self.name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    self.name = 'No Name'

                try:
                    #rating.encode(encoding='utf-8')
                    self.rating = commentbox.div.div.div.div.text


                except:
                    self.rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    self.commentHead = commentbox.div.div.div.p.text

                except:
                    self.commentHead = 'No Comment Heading'
                try:
                    self.comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    self.custComment = self.comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": self.searchString, "Name": self.name, "Rating": self.rating, "CommentHead": self.commentHead,
                          "Comment": self.custComment}
                self.reviews.append(self.mydict)
                return self.reviews
        except Exception as e:
            logging.error("Exception while creating dictionary: ",e)
            
