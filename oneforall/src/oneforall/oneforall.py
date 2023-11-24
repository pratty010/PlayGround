from InquirerPy import prompt

from src.tools.nettools import net
from src.tools.webtools import web

def main():
    """
    Main function to initiate the flow for the oneforall tool.
    Provides a list/set of tools that are available to the user.
    """

    # Choices for the exploit tool set
    choices = [
        {
            "type": "list",
            "name": "tool choice",
            "message": "Please select the weapon class:",
            "choices": ["0n3 F0r 411", "N37w0rk T00l5", "W3b Exp10it T00l5", "H3lp"],
        },
        {
            "type": "confirm",
            "name": "confirm",
            "message": "Confirm?",
            "default": True,
            "long_instruction": "Be sure my child !"
        },
    ]

    # Collecting results from user using inquirer prompt
    results = prompt(choices)
    # print(results)
    
    # Invoke the tool set based on the choice
    if results["tool choice"] == "0n3 F0r 411":
        print("It will be a masterpiece.")
    elif results["tool choice"] == "N37w0rk T00l5":
        net.net()
    elif results["tool choice"] == "W3b Exp10it T00l5":
        web.web()
    elif results["tool choice"] == "H3lp":
        print("Under Construction. Check out the README.md file.")


# Invoking main function
if __name__ == "__main__":
    main()