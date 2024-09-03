# class i need import
from .database import DataBaseUsage
# library i need usage
from datetime import datetime
import sys
from pycountry import countries
from simple_chalk.src.utils.join import join
from random import choices, randint
from inquirer import Text, prompt, List,Checkbox
from re import match
from simple_chalk import chalk
from random import choice
from string import punctuation ,ascii_letters ,digits
from uuid import uuid4






class SignUp:
    def __init__(self) -> None:
        self.db =  DataBaseUsage()


    def Sign_up(self)-> None:
        type_signup = [
        List('type',
                        message=f"What choice do you need?",
                        choices=["Customer","Employee",],
                    ),
        ]
        type_login = prompt(type_signup)
        info = [
            Text('FullName', message="Please enter full name",validate=lambda _, x: match(r'^[a-zA-Z ]+$', x)),
            Text('Email', message="Please enter your email",validate=lambda _, x: match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', x),default="example@gmail.com"),
            Text('Password', message="Please enter password",validate=lambda _, x: match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', x),default=self.RandomPassword()),
            List('country',
                            message=f"What your country?",
                            choices=sorted([country.name for country in countries if country.name != "Israel"]),
                        ),

                    ]

        info = prompt(info)
        if type_login['type'] == "Employee":
            grade = [
                        List('grade',
                                message=f"What your Grade?",
                                choices=[i for i in range(1,4)],
                            ),

                        ]
            grade = prompt(grade)
            data_up = {"Grade":grade["grade"],"ID":self.Gen_ID(),"RecoveryCodes":self.Gen_recovery(5)}
        else:
            data_up = {"Balance":0,"Cart":{},"Transfer":{},"Withdraw":{},"Deposite":{},"ID":self.Gen_ID(),"RecoveryCodes":self.Gen_recovery(4)}
        data = {**info,**data_up}

        print(chalk.red("Please save your recovery codes:"))
        for i,code in enumerate(data["RecoveryCodes"],1):
            print(chalk.cyan(f"{i}. {code} "))
        self.db.UploadData(collection=type_login['type'],data=data,document=data["ID"])
        print(f"{chalk.green("Registered successfuly you can now login")} {chalk.yellow(f"ID: {data["ID"]}")}!")


    def RandomPassword(self)-> str:
        return "".join([choice(ascii_letters + digits) for _ in range(10)])
    def Gen_ID(self):
        return uuid4().hex[:8]

    def Gen_recovery(self,number_code:int)-> list:
        return [str(uuid4()) for _ in range(number_code)]




class LognIn:
    def __init__(self) -> None:
        self.data = {}
        self.db = DataBaseUsage()


    def Logn_in(self) -> None:
        type_login = [
        List('type',
                        message=f"What choice do you need?",
                        choices=["Customer","Employee"],
                    ),
        ]
        type_login = prompt(type_login)

        info = [
        Text('ID', message="Please enter ID"),
        Text('Password', message="Please enter password"),

                    ]

        info = prompt(info)
        check = self.db.SearchData(id=info["ID"],password=info["Password"],collection=type_login["type"])

        if check:
            return check
        print(chalk.red("Please check your ID or Password"))
        return False
