from models import Product, Producers
from extensions import db

items = [
    Product(name="Organic Carrots", description="Fresh seasonal carrots from local growers.", price=1.80, stock=24, producer=Producers.bale_farm),
    Product(name="Free Range Eggs (6)", description="Half-dozen free range eggs.", price=2.95, stock=18, producer=Producers.featherdown_farm),
    Product(name="Whole Milk 1L", description="Locally sourced whole milk.", price=1.65, stock=20, producer=Producers.ketil_farm),
    Product(name="Sourdough Loaf", description="Fresh baked artisan sourdough.", price=3.50, stock=12, producer=Producers.yang_farm),
    Product(name="Seasonal Potatoes 2kg", description="Washed local potatoes.", price=4.20, stock=15, producer=Producers.bale_farm),
    Product(name="Spinach Bundle", description="Fresh spinach leaves.", price=1.45, stock=10, producer=Producers.yang_farm),
    Product(name="Strawberries 250g", description="Sweet seasonal strawberries.", price=3.95, stock=8, producer=Producers.featherdown_farm),
    Product(name="Local Honey 340g", description="Raw local honey jar.", price=5.75, stock=9, producer=Producers.ketil_farm),
]

db.session.add_all(items)
db.session.commit()

print("Products seeded.")