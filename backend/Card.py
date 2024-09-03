# library i need import

from random import randint
from datetime import datetime

class Card():

    def Create_carte(self):
        """

        :return: dict
        :rtype: dict
        """
        card_format= ""
        cvv = ""
        while len(card_format) <12:
            card_format += str(randint(1,9))
        while len(cvv) < 3:
            cvv += str(randint(1,9))

        card_number = f"1001{card_format}"

        expires = f"{datetime.now().year+4}/{datetime.now().month}"
        card = {"card":card_number,"expire_month":(datetime.now().month),"expire_year":(datetime.now().year+4),"cvv": cvv}

        return card
