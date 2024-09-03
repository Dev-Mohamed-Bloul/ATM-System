# class i need import
from backend.Account import SignUp,LognIn
from backend.effect import Effect
from backend.database import DataBaseUsage
from backend.ATM import Atm
from backend.Customer import MainCustomer
from backend.Employee import Employee
# library i need usage
from random import choice, choices
from inquirer import Text, prompt, List,Checkbox
from simple_chalk import chalk

class MainMenu:
    def __init__(self) -> None:
        self.signup = SignUp()
        self.login = LognIn()
        self.effect = Effect()
        self.customer = MainCustomer()
        self.atm = Atm()
        self.emp = Employee()



    def Main(self)-> None:

        while True:

            self.effect.Logo()
            choices_user = [
            List('type',
                            message=f"What choice do you need?",
                            choices=["Sign Up","Login","ATM","Quit"]
                        ),
            ]
            choice= prompt(choices_user)
            if choice['type'] == "Sign Up":
                self.effect.Clear()
                self.signup.Sign_up()
            elif choice['type'] == "Login":
                self.effect.Clear()
                data_customer = self.login.Logn_in()
                if data_customer and "Grade" in (key:= data_customer.keys()):
                    self.emp.Grade_choice(data=data_customer)

                elif data_customer:

                    self.effect.Clear()
                    print(f"{chalk.green("Hello again")} {chalk.yellow(data_customer["FullName"])}")
                    self.customer.main(data=data_customer)
            elif choice['type'] == "ATM":
                self.atm.Add_card()
            else:
                self.effect.Bar("In progress please wait")
                return

if __name__ == "__main__":
    test : MainMenu = MainMenu()
    test.Main()
