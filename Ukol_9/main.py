import argparse
import sys
from models import Product
from storage import Storage
from datetime import datetime
from functools import wraps

# Dekorátor pro logování akcí do souboru history.log
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Spustíme původní funkci a uložíme výsledek
        vysledek = func(*args, **kwargs)
        
        cas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        operace = func.__name__
        # args[1:] vynechá 'self' u metod třídy
        data = args[1:] if len(args) > 1 else ""

        with open("history.log", "a", encoding="utf-8") as f:
            f.write(f"[{cas}] Operace: {operace} | Data: {data}\n")

        return vysledek
    return wrapper

class InventoryManager:
    def __init__(self, storage: Storage):
        self.storage = storage
        # Načteme existující produkty ze souboru
        self.products = self.storage.load_products()

    @log_action
    def add_product(self, name: str, price: float, quantity: int):
        # Vytvoření instance produktu
        new_product = Product(name, price, quantity)
        # Přidání do seznamu
        self.products.append(new_product)
        # Uložení aktualizovaného seznamu do úložiště
        self.storage.save_products(self.products)
        print(f"Produkt '{name}' byl úspěšně přidán do skladu.")

    def list_products(self):
        if not self.products:
            print("Sklad je prázdný.")
            return

        print("\n--- Seznam produktů ---")
        for i, p in enumerate(self.products, 1):
            # Předpokládám, že Product má __str__ nebo metodu pro zobrazení
            print(f"{i}. {p.name} | Cena: {p.price} | Množství: {p.quantity}")
        
        print(f"--- Celková hodnota skladu: {self.total_value()} ---\n")

    def search_products(self, query: str):
        query = query.lower()
        results = [p for p in self.products if query in p.name.lower()]
        
        if not results:
            print(f"Žádné produkty neodpovídají dotazu: '{query}'")
        else:
            print(f"\nVýsledky hledání pro '{query}':")
            for p in results:
                print(f"- {p.name} ({p.quantity} ks)")

    def total_value(self):
        # Spočítá sumu (cena * množství) pro všechny produkty
        return sum(p.price * p.quantity for p in self.products)

def main():
    parser = argparse.ArgumentParser(description="Systém správy skladu")
    subparsers = parser.add_subparsers(dest="command")

    # Příkaz 'add'
    add_parser = subparsers.add_parser("add", help="Přidat produkt")
    add_parser.add_argument("--name", required=True, help="Název produktu")
    add_parser.add_argument("--price", required=True, type=float, help="Cena")
    add_parser.add_argument("--qty", required=True, type=int, help="Množství")

    # Příkaz 'list'
    subparsers.add_parser("list", help="Vypsat produkty")
    
    # Příkaz 'search'
    search_parser = subparsers.add_parser("search", help="Hledat produkt")
    search_parser.add_argument("--query", required=True, help="Hledaný text")

    # Příkaz 'value'
    subparsers.add_parser("value", help="Zobrazit celkovou hodnotu skladu")

    args = parser.parse_args()
    
    storage = Storage()
    manager = InventoryManager(storage)

    if args.command == "add":
        manager.add_product(args.name, args.price, args.qty)
    elif args.command == "list":
        manager.list_products()
    elif args.command == "search":
        manager.search_products(args.query)
    elif args.command == "value":
        print(f"Celková hodnota skladu je: {manager.total_value()}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()