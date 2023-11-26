import requests
import re
import threading
import logging
from Category import cats
from mongo import collection

class Fetcher:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="logs.log"
    )


    def __init__(self):

        self.cats = cats
        self.catcount = len(self.cats)

        self.busycat = [0] * self.catcount #list(var) keeps the log of category being fetched by threads in main function. 0/1 = False/True
        self.IDs = {} #dic(var) stores all fetched data.
    def fetch_arxiv_data(self, url, cat):
        try:
            logging.info(f"Requesting {cat} ")
            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.text

                # Regular expression to find and print lines containing "arXiv:xxx.xxx"
                # Only saves ID "xxx.xxx"
                arxiv_lines = re.findall(r"arXiv:\s*(.*?)</a>", page_content)
                return arxiv_lines
            else:
                logging.error(f"Error: Unable to fetch data. Status code: {str(response.status_code)}")

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

    def save_id(self):
        logging.info("running save_id(), Saving arXiv id's to Database.")
        transaction = collection.insert_one(self.IDs)
        docid = transaction.inserted_id
        logging.info(f"""Saved to Database: DataDB 
                        Document ID: {str(docid)}\n
+------------------------------------------------------------------------------+
                     """)
        print("Fetcher is done Working!")



    def fetchloop(self, threadID):
        for index, cat in enumerate(self.cats):
            logging.info(f"{threadID} started working on{cat}")
            if self.busycat[index] == 1:
                logging.info(f"{cat} is already in Process, moving to next category.")

                continue
            else:
                self.busycat[index] = 1
                url = f"https://arxiv.org/list/{cat}/pastweek?skip=0&show=50"
                self.IDs[cat] = self.fetch_arxiv_data(url, cat)


if __name__ == "__main__":

    f=Fetcher()
    
    t1 = threading.Thread(target=f.fetchloop, args=('t1',))
    t2 = threading.Thread(target=f.fetchloop, args=('t2',))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    

    f.save_id()
