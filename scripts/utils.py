from datetime import datetime
import pandas as pd
from binance.client import Client
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("./marcyourmind-01-firebase-adminsdk-mkura-11eed6cf26.json")
initialize_app(cred)
db = firestore.client()

def new_client(name=None):
    """Creates a new Binance client for api access to the account"""
    # print("WARNING - Binance.new_client(name) loads basic account regardless of name given.")
    client = Client()
    # api_key=config[name]['api_key'],
                    # api_secret=config[name]['secret_key'])
    return client



def get_current_data(ticker, interval, lookback=None, start=None, verbose=False, client=None) -> pd.DataFrame:
    """
    Can only handle lookback in days.

    args:
        ticker: string
        lookback: can be number of days to fetch or a string as specified by binance api.
        start: alternative input to lookback. Used when lookback is a Unix timestamp
    """

    if client is None:
        client = new_client()

    if lookback:
        if type(lookback) == int:
            ohlcv = client.get_historical_klines(ticker, interval, f"{lookback} days ago UTC")
        elif type(lookback) == str:
            ohlcv = client.get_historical_klines(ticker, interval, lookback)
    elif start:
        if type(start) == int:
            ohlcv = client.get_historical_klines(ticker, interval, start)
    else:
        raise Exception("Invalid 'lookback' or 'start' parameter given.")
    data = pd.DataFrame(ohlcv, columns=['open time',
                                        'Open',
                                        'High',
                                        'Low',
                                        'Close',
                                        'Volume',
                                        'close time',
                                        'asset volume',
                                        '# trades',
                                        'base buy volume',
                                        'quote buy volume',
                                        'ignore'])

    data = data.drop(columns=['close time', 'asset volume', 'base buy volume', 'quote buy volume', 'ignore', '# trades'])

    data['Open'] = data['Open'].astype(float)
    data['High'] = data['High'].astype(float)
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype(float)
    data['Volume'] = data['Volume'].astype(float)
    data['open time'] = pd.to_datetime(data['open time'], unit='ms')
    if verbose:
        print(data.head(15))
    return data


def createDocument(collection, document=None, data={}):
    db.collection(collection).document(document).set(data)
    

def readDocument(collection, document):
    doc = db.collection(collection).document(document).get()
    return doc.to_dict()

def readCollection(collection):
    docs = db.collection(collection).where('lastClose', '>', 500).stream()
    docs = [doc.to_dict() for doc in docs]
    return docs
        

def updateDocument(collection, document, data):
    doc_ref = db.collection(collection).document(document).update(data)

def deleteDocument(collection, document):
  db.collection(collection).document(document).delete()

def deleteField(collection, document, field):
  doc_ref = db.collection(collection).document(document)
  doc_ref.update({
    field: firestore.DELETE_FIELD
  })
  
def deleteCollection(collection):
    # Get all documents from the collection
    docs = db.collection(collection).stream()

    # Delete each document
    for doc in docs:
        doc.reference.delete()

    print("Collection ", collection, " has been cleared.")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def backup_collection(source_collection, backup_collection):
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Retrieve data from the source collection
    source_data = db.collection(source_collection).get()
    
    # Create a new document in the backup collection with the current date as the document key
    backup_doc_ref = db.collection(backup_collection).document(current_date)
    
    # Store the data from the source collection in the backup document
    for doc in source_data:
        backup_doc_ref.set({
            doc.id: doc.to_dict()
        }, merge=True)  # Use merge=True to merge the data with existing documents
    
    print("Backup completed for", current_date)