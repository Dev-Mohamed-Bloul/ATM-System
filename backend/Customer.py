# class i need import
from backend.database import DataBaseUsage
from backend.Card import Card
from backend.effect import Effect
# library i need import
from abc import ABC
from inquirer import Text, prompt, List,Checkbox
from re import match
from simple_chalk import chalk

class MainCustomer:
    def __init__(self) -> None:
        self.db = DataBaseUsage()
        self.card = Card()
        self.effect = Effect()
        self.customer = Customer()
        self.data = {}

    def main(self,data):

        """

        :param data: dict
        :return: None

        """
        self.data = data
        while True:

            option = [
            List('type',
                            message=f"What choice do you need?",
                            choices=[
                                    "Show account information",
                                    "Change CVV",
                                    "Create Card",
                                    "Show card information",
                                    "Change password",
                                    "Remove account",
                                    "Logout"
                            ]
                        ),
            ]

            option = prompt(option)
            if option["type"] == "Show account information":
                self.effect.Clear()
                self.customer.Show_information(self.data)
            elif option["type"] == "Change CVV":
                check= self.customer.Change_CVV(self.data)
                if check:
                    self.data = check

            elif option["type"] == "Change password":
                check = self.customer.Reset_password(self.data)
                if check:
                    self.data = check
                    self.db.UpdataData(id=self.data["ID"],data=self.data)
                    print(chalk.yellow("you need login again!!"))
                    return


            elif option["type"] == "Create Card":
                if len(self.data["Cart"]) == 0 or self.data["Balance"] >= 10:
                    card = self.card.Create_carte()
                    self.data["Cart"][str(len(self.data["Cart"])+ 1)] = card
                    if len(self.data["Cart"]) > 1:
                        self.data["Balance"] = self.data["Balance"]-10
                    self.effect.Bar("Card processing please wait",range=120)
                    self.effect.Clear()
                    print(chalk.green(f"{self.data["FullName"]} Your card is ready now for use !"))
                    self.effect.show_card(card,self.data["FullName"])
                else:
                    print(chalk.red("You need 10$ for create another card!"))
            elif option["type"] == "Show card information":
                self.customer.Show_cards(self.data)

            elif option["type"] == "Remove account":
                check = self.customer.Romove_account(data["ID"],data["Password"])
                if check:
                    return


            else:
                self.db.UpdataData(id=self.data["ID"],data=self.data)
                return



class Customer:
    def __init__(self) -> None:
        self.db = DataBaseUsage()
        self.effect = Effect()
    def Show_information(self,data:dict,hide=False)-> None:
        """
        :param data: dict
        :return: None

        """
        for data , info in data.items():


            if data == "Cart":
                print(chalk.green(f'Cart: you have {chalk.yellow(len(info))} card'))

            elif data == "Password":
                print(chalk.green(f'{data} :{chalk.yellow(info[:5])}***** '))
            elif data == "Withdraw" or data == "Transfer" or data == "Deposite":
                print(chalk.green(f'{data} Transaction :{chalk.yellow(len(info))} '))
            elif data == "Balance":
                print(chalk.green(f'{data} :{chalk.yellow(info)}$'))
            elif data == "RecoveryCodes":
                print(chalk.green(f'Recovery Codes :{chalk.yellow("/".join(info))}'))
            else:
                print(chalk.green(f'{data} :{chalk.yellow(info)}'))

    def Show_cards(self,data):

        """
        :param data: dict
        :return: None
        """
        if len(data["Cart"])> 0:
            cards = [
                List('cards',
                            message=f"What card you need?",
                            choices= [f"{i}. {card["card"]} " for i,card in data["Cart"].items() ]
                        ),
            ]
            show = prompt(cards)
            self.effect.show_card(data["Cart"][show["cards"][0]],data["FullName"])
            return
        print(chalk.red('You don\'t have any card !'))
    def Change_CVV(self,data)-> dict:
        """
        :param data: dict
        :return: dict
        """
        if len(data["Cart"])> 0:
            cards = [
                List('cards',
                                    message=f"What card you need?",
                                    choices= [f"{i}. {card["card"]} " for i,card in data["Cart"].items() ]
                                ),
                    ]
            card_change = prompt(cards)
            cvv = data["Cart"][card_change["cards"][0]]["cvv"]
            cvv_check = [
                Text('old', message="Please enter old cvv"),
                Text('new', message="Please enter new cvv"),
                Text('confirm', message="Please confirm your cvv")
            ]
            cvv_check= prompt(cvv_check)
            if cvv_check["new"]== cvv_check["confirm"] and cvv_check["old"] == cvv:
                data["Cart"][card_change["cards"][0]]["cvv"] = cvv_check["new"]
                print(chalk.green("Changed successfully"))
                return data
            print(chalk.red("Mismatched information!!"))
            return {}
        print(chalk.red('You don\'t have any card !'))
    def Romove_account(self,id,password):

        """
        :param id: int
        :param password: str
        :return: bool

        """
        password_check = [Text('confirm', message="Please enter your password")]
        password_check = prompt(password_check)
        if password == password_check['confirm']:
            self.db.RomoveData(id)
            print(chalk.yellow("Successfully deleted"))
            return True
        else:

            print(chalk.red("Please check your password"))
            return False

    def Reset_password(self,data):
        """
        :param data: dict
        :return: dict
        """
        password_check = [
            Text('old', message="Please enter old password"),
            Text('new', message="Please enter new password",validate=lambda _, x: match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', x)),
            Text('confirm', message="Please confirm your password")
        ]
        password_check= prompt(password_check)
        if password_check["new"]== password_check["confirm"] and password_check["old"] == data["Password"]:
            data["Password"] = password_check["new"]
            print(chalk.green("Changed successfully"))
            return data
        print(chalk.red("Mismatched information!!"))
        return {}
