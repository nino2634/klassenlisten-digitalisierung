# -*- coding: cp1252 -*-

import sys
import src.app.configurator_modules.change_password as password_manger
import src.app.configurator_modules.errorfix as error_fixer

def main_menu():
    while True:
        print("\nBitte waehlen Sie eine Aktion zum Ausfuehren:")
        print("1. Passwort aendern")
        print("2. Einstellungen")
        print("3. Fehlersuche")
        print("4. App zuruecksetzen")
        print("5. Beenden")
        
        choice = input("Geben Sie Ihre Wahl ein (1-4): ").strip()
        
        if choice == "1":
            password_manger.change_password()  # assuming your script has a callable function `run()`
        elif choice == "2":
            #errorcheck.run()
            pass
        elif choice == "3":
            error_fixer.fix()
        elif choice == "4":
            error_fixer.hard_reset()
        elif choice == "5":
            print("Programm wird beendet.")
            sys.exit(0)
        else:
            print("Ungueltige Wahl. Bitte erneut versuchen.")

main_menu()