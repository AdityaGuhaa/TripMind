from app.tools.place_finder import PlaceFinder

finder = PlaceFinder()

places = finder.find_places("Goa", "cafes")

print("\nTop places found:\n")

for place in places:
    print(place)