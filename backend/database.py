
# library i need import
import firebase_admin
from firebase_admin import credentials,firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from tqdm import tqdm

cred = credentials.Certificate("file config connection firebase_admin here")
firebase_admin.initialize_app(cred,{'database url'})
db = firestore.client()


class DataBaseUsage:
    def UploadData(self,document:str, data:dict, collection:str="Customer")-> bool:
        """
        this function is used to upload data to the database
        :return: True if the data is uploaded successfully, False otherwise
        """

        try:
            db.collection(collection).document(document).set(data)
            return True
        except:
            return False


    def SearchData(self,id:str, password:str="", collection:str="Customer",atm=False):
        """
        :param id: the id of the user
        :param password: the password of the user
        :param collection: the collection that the data is stored in the database (default is Customer)
        :param atm: if the user is an atm or not (default is False)
        :return: the data of the user if the user is found, False otherwise
        """


        try:
            collection = db.collection(collection)
            status = collection.where(filter=FieldFilter("ID", "==", id)).get()
            convert_data = [data.to_dict()  for data in status ]
            if (atm and convert_data) or (convert_data and password == convert_data[0]["Password"] and password):
                return convert_data[0]
            return []
        except:
            return False

    def UpdataData(self,id:str,data= {}, collection:str="Customer")-> bool:
        """

        :param id: the id of the user
        :param data: the data that will be updated
        :param collection: the collection that the data is stored in the database (default is Customer)
        :return: True if the data is updated successfully, False otherwise

        """


        try:
            db.collection(collection).document(id).update(data)
            return True
        except:
            return False
            # print(chalk.red("There is no connection to the server"))
    def SearchCard(self,card:str,cvv:str):
        """

        :param card: the card number
        :param cvv: the cvv number
        :return: the data of the user if the user is found, False otherwise

        """

        try:
            collection = db.collection("Customer")
            docs = collection.stream()
            for doc in docs:
                cards = doc.to_dict().get("Cart")
                for _, info in cards.items():
                    if info["card"] == card and info["cvv"] == cvv :
                        return doc.to_dict()
            return False
        except:
            return False


    def RomoveData(self,id:str, collection:str="Customer")-> bool:

        """

        :param id: the id of the user
        :param collection: the collection that the data is stored in the database (default is Customer)
        :return: True if the data is removed successfully, False otherwise

        """
        try:
            db.collection(collection).document(id).delete()
            return True
        except:
            return False
