from inquirer import Text, prompt, List,Checkbox
from pycountry import countries

symbol = [
      List('symbol',
                    message=f"What symbol do you need?",
                    choices=[country.name for country in countries if country.name != "isreal"],
                ),
    ]
prompt(symbol)
