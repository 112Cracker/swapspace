from exchange.models import Category

# flush old categories
categories = Category.objects.all()
if categories.count() > 0:
    Category.objects.all().delete()

# load main categories
toys = Category(name="Toys")
toys.save()

electronics = Category(name="Electronics")
electronics.save()

games = Category(name="Games")
games.save()

petSupplies = Category(name="Pet Supplies")
petSupplies.save()

books = Category(name="Books")
books.save()

media = Category(name="Media")
media.save()

appliances = Category(name="Appliances")
appliances.save()

furniture = Category(name="Furniture")
furniture.save()

sports = Category(name="Sports")
sports.save()

womenStyle = Category(name="Women's Style")
womenStyle.save()

menStyle = Category(name="Men's Style")
menStyle.save()


