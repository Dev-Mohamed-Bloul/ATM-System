# class i need import
from backend.database import DataBaseUsage
from backend.effect import Effect
# library i need import
from inquirer import Text, prompt, List,Checkbox
from simple_chalk import chalk
from re import match
from abc import ABC, abstractmethod
from datetime import datetime



class Atm:
    def __init__(self) -> None:
        self.db = DataBaseUsage()
        self.effect = Effect()
        self.data = {}

    def Add_card(self):
        """
        Add card to ATM
        :return: None
        """

        info = [
            Text('Card Number', message="Please Enter Card Number",validate=lambda _, x: match(r'^[0-9]{12,19}$', x),default="1001...."),
            Text('CVV', message="Please Enter CVV",validate=lambda _, x: match(r"^[0-9]{3,4}$", x),default="1234")
                    ]

        info = prompt(info)
        check = self.db.SearchCard(info['Card Number'],info['CVV'])
        if check:
                self.data = check
                self.effect.Clear()
                print(f"{chalk.green("Hello")} {chalk.yellow(self.data["FullName"])} {chalk.green("In ATM")} {self.data["country"]}!")

                while True:
                    option_ATM = [
                            List('type',
                                            message=f"What choice do you need?",
                                            choices=[
                                                    "Deposite",
                                                    "Transfer",
                                                    "Withdraw",
                                                    "Balance Inquiry",
                                                    "Mobile recharge",
                                                    "History Transaction",
                                                    "Quit"
                                            ]
                                        ),
                            ]

                    option_ATM = prompt(option_ATM)

                    if option_ATM["type"] == "Deposite":
                        cash = [Text('Amount', message="Please enter amount",validate=lambda _, x: match(r'^(?=.*[1-9])\d*\.?\d+$', x))]
                        cash =prompt(cash)
                        transaction = Deposite(float(cash["Amount"]))
                    elif option_ATM["type"] == "Transfer":
                        info = [
                            Text('Amount', message="Please enter amount",validate=lambda _, x: match(r'^(?=.*[1-9])\d*\.?\d+$', x)),
                            Text('ID', message="Please enter ID")
                        ]
                        info =prompt(info)
                        transaction = Transfer(float(info["Amount"]))
                        transaction.process_transaction(data=self.data,id=info["ID"])
                        continue
                    elif option_ATM["type"] == "Withdraw":
                        cash = [Text('Amount', message="Please enter amount",validate=lambda _, x: match(r'^(?=.*[1-9])\d*\.?\d+$', x))]
                        cash =prompt(cash)
                        transaction = Withdraw(float(cash["Amount"]))
                    elif option_ATM["type"] == "Balance Inquiry":
                        transaction = BalanceInquiry()
                    elif option_ATM["type"] == "History Transaction":
                        transaction = History()

                    elif option_ATM["type"] == "Mobile recharge":
                        info = [
                            Text('Amount', message="Please enter amount",validate=lambda _, x: match(r'^(?=.*[1-9])\d*\.?\d+$', x)),
                            Text('Phone Number', message="Please phone number",validate=lambda _, x: match(r'^(?:(?:\+|00)([1-9]\d{0,2})|0)(?:\s?|-?)([1-9]\d{0,3})(?:\s?|-?)(\d{4,})$', x),default="+")]
                        info = prompt(info)
                        transaction = Withdraw(float(info["Amount"]))
                        transaction.process_transaction(data=self.data,id=info["Phone Number"])
                        continue
                    else:
                        self.db.UpdataData(self.data["ID"],self.data)
                        self.effect.Clear()
                        return
                    transaction.process_transaction(self.data)
                    continue
        self.effect.Clear()
        print(chalk.red("Please check your informatino card!!"))








class Transaction(ABC):
    def __init__(self,transaction_type:str, amount) -> None:
        self.date:str = str(datetime.now())
        self.amount = amount
        self.type = transaction_type
        self.db= DataBaseUsage()
        self.effect = Effect()
    @abstractmethod
    def process_transaction(self,data:dict,id=None):
        """
        :param data: dict
        :param id: str
        :return: None

        """
        pass

class Transfer(Transaction):
    """
    :param amount: float
    :return: None
    """
    def __init__(self,amount=None) -> None:
        super().__init__("Transfer",amount)
        self.amount

    def process_transaction(self,data,id=None):

        """
        :param data: dict
        :param id: str
        :return: None

        """
        if data["Balance"] >= self.amount:
            if data["ID"] != id and (rec := self.db.SearchData(id=id,atm=True)):
                rec["Balance"] = (rec["Balance"]  + self.amount)
                information_transaction = {self.date:f"Deposite fee of {self.amount}$ from ({id})"}
                rec["Deposite"] = {**rec["Deposite"],**information_transaction}
                self.db.UpdataData(id=id,data=rec)
                data["Balance"] = data["Balance"] - self.amount
                information_transaction = {self.date:f"{self.type} fee of {self.amount}$ to ({id})"}
                data[self.type] = {**data[self.type],**information_transaction}
                print(chalk.green("Compeleted Transfer"))
                return data
            print(chalk.red("Please check your ID!!"))
            return
        print(chalk.red("Please check your balance!!"))


class Withdraw(Transaction):
    def __init__(self,amount=None) -> None:
        super().__init__("Withdraw",amount)
        self.amount

    def process_transaction(self,data,id=None):
        if data["Balance"] >= self.amount:
                data["Balance"] = data["Balance"] - self.amount
                information_transaction = {self.date:f"{self.type} fee of {self.amount}$"}
                data[self.type] = {**data[self.type],**information_transaction}
                self.effect.Bar(text="We're working on process transaction withdraw",range=100,time=0.03)
                print(chalk.green("Please witdraw your card and don't forget your money"))
                return data
        print(chalk.red("Please check your balance!!"))

class BalanceInquiry(Transaction):
    def __init__(self,amount=None) -> None:
        super().__init__("Balance",amount)
        self.amount

    def process_transaction(self,data,id=None):
        print(chalk.green(f"Your current balance is: {chalk.yellow(data["Balance"])}$"))

class Deposite(Transaction):
    def __init__(self,amount=None) -> None:
        super().__init__("Deposite",amount)
        self.amount

    def process_transaction(self,data,id=None):
                data["Balance"] = data["Balance"] + self.amount
                information_transaction = {self.date:f"{self.type} fee of {self.amount}$"}
                data[self.type] = {**data[self.type],**information_transaction}
                self.effect.Bar(text="We're working on process transaction deposite",range=100,time=0.03)
                print(chalk.green("Please witdraw your card"))
                return data

class History(Transaction):
    def __init__(self,amount=None) -> None:
        super().__init__("History",amount)
        self.amount

    def process_transaction(self,data,id=None):
        option_HIS = [
                List('type',
                                message=f"What choice do you need?",
                                choices=[
                                        "Deposite",
                                        "Transfer",
                                        "Withdraw",
                                ]
                            ),
                ]
        option_HIS = prompt(option_HIS)
        if len(data[option_HIS["type"]]) == 0:
            print(chalk.red("Don't have any operations yet!! "))
            return
        for date, info in data[option_HIS["type"]].items():
            print(f"{chalk.green(date)} :{chalk.yellow(info)} ")
