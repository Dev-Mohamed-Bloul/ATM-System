# library i need import

from tqdm import trange
from simple_chalk import chalk
from os import system, name
from time import sleep

from terminaltexteffects.effects import effect_spotlights

from terminaltexteffects.effects import effect_print



class Effect:
    def __init__(self) -> None:
        self.logo = """

        █████╗ ████████╗███╗   ███╗
        ██╔══██╗╚══██╔══╝████╗ ████║
        ███████║   ██║   ██╔████╔██║
        ██╔══██║   ██║   ██║╚██╔╝██║
        ██║  ██║   ██║   ██║ ╚═╝ ██║
        ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝


        """
        self.card_logo = """
        ┌─────────────────────────────────────┐
        │ ╔═════════════════════════╗         │
        │ ║                         ║         │
        │ ║     CODEZILLA CARD      ║         │
        │ ║                         ║         │
        │ ╚═════════════════════════╝         │
        │                                     │
        │ 1234-5678-9012-3456                 │
        │                                     │
        │ Name
        │ CVV: 123
        │ Expires: 08/25
        └─────────────────────────────────────┘

        """


    def Bar(self,text:str,range:int=60,data=None,time:float=0.01) -> list:
        return [sleep(time) for _ in trange(range,desc=chalk.green(text))]
    def Clear(self)-> None:
            system("cls") if name =="nt" else system("clear")
    def Logo(self):
            effect = effect_spotlights.Spotlights(self.logo)
            with effect.terminal_output() as terminal:
                for frame in effect:
                    terminal.print(frame)



    def show_card(self,card_info:dict,name)-> None:

        i = 0
        j = 4
        card=[]
        for _ in range(4):
            card.append(card_info["card"][i:j])
            i = j
            j += 4
        card = "-".join(card)
        card_show = self.card_logo
        card_show =card_show.replace("Name",name)
        card_show =card_show.replace("1234-5678-9012-3456",card)
        card_show =card_show.replace("08/25",f"{card_info["expire_year"]}/{card_info["expire_month"]}")
        card_show =card_show.replace("123",card_info["cvv"])
        effect = effect_print.Print(card_show)
        with effect.terminal_output() as terminal:
                for frame in effect:
                    terminal.print(frame)
