from InquirerPy import prompt

from src.tools.nettools import net


def main():
    choices = [
        {
            "type": "list",
            "name": "tool choice",
            "message": "Please select the weapon class:",
            "choices": ["Network Tools", "Web Exploit Tools", "Help"],
        },
        {
            "type": "confirm",
            "name": "confirm",
            "message": "Confirm?",
            "default": True,
            "instruction": "Be sure my child !"
        },
    ]

    results = prompt(choices)
    # print(results)
    
    if results["tool choice"] == "Help":
        print("Under Construction.")
    elif results["tool choice"] == "Network Tools":
        net.net()

if __name__ == "__main__":
    main()