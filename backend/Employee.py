# class i need import

from backend.database import DataBaseUsage
from backend.Card import Card
from backend.effect import Effect
from backend.ATM import Transaction
from backend.Customer import Customer

# library i need import
from inquirer import Text, prompt, List,Checkbox
from enum import Enum
from simple_chalk import chalk
from re import match
from datetime import datetime
from pycountry import countries
class Grade(Enum):
    GRADE1=["Research a client","Deposite With ID" ,"Logout"]
    GRADE2=["Research a employee"]
    GRADE3=["Remove account","Add cash to ATM"]


class Employee:
    def __init__(self) -> None:
        self.effect  = Effect()
        self.grade = EmpGrade3()

    def Grade_choice(self,data:dict) -> None:

            while True:

                choices_emp = [
                List('type',
                                message=f"What choice do you need?",
                                choices=Grade.GRADE3.value +Grade.GRADE2.value +Grade.GRADE1.value
                            ),
                ]
                active =prompt(choices_emp)
                if active["type"] =="Research a client":
                    self.grade.Search_client()
                    continue
                elif active["type"] =="Deposite With ID":
                        self.grade.Deposite()
                        continue
                elif active["type"] =="Research a employee" and (data["Grade"]== 3 or data["Grade"]== 2):
                            self.grade.Search_emp()
                            continue
                elif active["type"] =="Remove account" and (data["Grade"]== 3):
                        self.grade.Remove_account()
                        continue
                elif active["type"] =="Add cash to ATM" and (data["Grade"]== 3):
                        self.grade.Add_cash_atm()
                        continue
                elif active["type"] =="Logout":
                    self.effect.Clear()
                    return
                print(chalk.red('You can\'t access this feature try to review the support!'))





class EmpGrade1:
    def __init__(self) -> None:
        self.db = DataBaseUsage()
        self.customer = Customer()
        self.effect = Effect()
        self.date:str = str(datetime.now())
    def Search_client(self):
        id = [Text('ID', message="Please enter ID")]
        id = prompt(id)
        if (search:= self.db.SearchData(id=id["ID"],atm=True)):
            self.customer.Show_information(search,hide=True)
            return

        print(chalk.red("Not Found"))

    def Deposite(self):
        id = [Text('ID', message="Please enter ID")]
        id = prompt(id)
        if (data_client:= self.db.SearchData(id=id["ID"],atm=True)):
            amount = [Text('amount', message="Please enter amount",validate=lambda _, x: match(r'^(?=.*[1-9])\d*\.?\d+$', x))]
            amount = prompt(amount)
            data_client["Balance"] = data_client["Balance"] + float(amount["amount"])
            information_transaction = {self.date:f"Deposite fee of {amount["amount"]}$"}
            data_client["Deposite"] = {**data_client["Deposite"],**information_transaction}
            self.effect.Bar(text="We're working on process transaction deposite",range=100,time=0.03)
            print(data_client)
            self.db.UpdataData(id=id["ID"],data=data_client)
            return
        print(chalk.red("Please check your ID"))


class EmpGrade2(EmpGrade1):
    def Search_emp(self):
        id = [Text('ID', message="Please enter ID")]
        id = prompt(id)
        if (data_emp:= self.db.SearchData(id=id["ID"],atm=True,collection="Employee")):
            self.customer.Show_information(hide=True,data=data_emp)
            return
        print(chalk.red("Not found!"))

class EmpGrade3(EmpGrade2):
    def Remove_account(self):
        id = [Text('ID', message="Please enter ID")]
        id = prompt(id)
        if (data:= self.db.SearchData(id=id["ID"],atm=True,collection="Employee")) or (data:= self.db.SearchData(id=id["ID"],atm=True,collection="Customer")):
            check = data.keys()
            if "Grade" in check:
                self.db.RomoveData(id=id["ID"],collection="Employee")
            else:
                self.db.RomoveData(id=id["ID"],collection="Customer")
            self.effect.Bar("Delete in progress")
            return
        print(chalk.red("Not found!"))
    def Add_cash_atm(self):
        info = [
            Text('amount', message="Please enter amount",validate=lambda _, x: match(r'^(?=.*[1-9])\d*\.?\d+$', x)),
            List('country',
                            message=f"Location ATM",
                            choices=sorted([country.name for country in countries if country.name != "Israel"]),
                        ),
                    ]

        info = prompt(info)
        self.effect.Bar("Processing your request please wait")
        search = self.db.SearchData(id=info["country"],atm=True,collection="ATM")

        search["Cash"]= search["Cash"] + float(info["amount"])
        self.db.UpdataData(id=info["country"],data= search,collection="ATM")
