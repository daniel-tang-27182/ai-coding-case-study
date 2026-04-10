from enum import Enum

class AttrName(Enum):
    NAME = "name"
    COLOR = "color"
    DRINK = "drink"
    PET = "pet"
    HOBBY = "hobby"
    MUSICAL_INSTRUMENT = "musical instrument"
    FLOWER = "flower"
    DESSERT = "dessert"
    CITY = "city"
    BOOK = "book"
    VEHICLE = "vehicle"
    OCCUPATION = "occupation"
    SPORT = "sport"
    FRUIT = "fruit"
    GEMSTONE = "gemstone"
    COUNTRY = "country"
    MOVIE_GENRE = "movie genre"
    WEATHER = "weather"
    SHOE_TYPE = "shoe type"
    BODY_PART = "body part"
    PROGRAMMING_LANGUAGE = "programming language"

attributes_values = {
    AttrName.NAME: ["Emily", "Jacob", "Sarah", "Michael", "Lauren", "Daniel", "Jessica", "Ryan", "Megan", "Andrew",
                  "Olivia", "Ethan", "Sophia", "Matthew", "Ava", "Christopher", "Isabella", "James", "Mia", "William"],
    AttrName.COLOR: ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", "Brown", "Black", "White",
                   "Teal", "Maroon", "Navy", "Olive", "Cyan", "Magenta", "Lavender", "Beige", "Turquoise", "Silver"],
    AttrName.DRINK: ["Coffee", "Tea", "Lemonade", "Wine", "Water", "Beer", "Cider", "Juice", "Soda", "Milk",
                   "Hot Chocolate", "Smoothie", "Whiskey", "Vodka", "Iced Tea", "Coconut Water", "Ginger Ale", "Milkshake", "Cocktail", "Herbal Tea"],
    AttrName.PET: ["Dog", "Cat", "Parrot", "Rabbit", "Fish", "Hamster", "Turtle", "Snake", "Ferret", "Lizard",
                 "Guinea Pig", "Canary", "Chinchilla", "Hermit Crab", "Rat", "Mouse", "Gerbil", "Hedgehog", "Sugar Glider", "Iguana"],
    AttrName.HOBBY: ["Painting", "Reading", "Gardening", "Hiking", "Cooking", "Photography", "Knitting", "Cycling", "Dancing", "Writing",
                   "Singing", "Chess", "Yoga", "Pottery", "Bird Watching", "Calligraphy", "Origami", "Scrapbooking", "Juggling", "Magic Tricks"],
    AttrName.MUSICAL_INSTRUMENT: ["Guitar", "Piano", "Violin", "Drums", "Flute", "Trumpet", "Cello", "Saxophone", "Clarinet", "Harp",
                               "Trombone", "Oboe", "Ukulele", "Banjo", "Accordion", "Xylophone", "Harmonica", "Mandolin", "Bagpipes", "Didgeridoo"],
    AttrName.FLOWER: ["Rose", "Tulip", "Lily", "Daisy", "Orchid", "Sunflower", "Carnation", "Peony", "Violet", "Marigold",
                   "Daffodil", "Poppy", "Iris", "Lavender", "Dahlia", "Hydrangea", "Zinnia", "Snapdragon", "Foxglove", "Bleeding Heart"],
    AttrName.DESSERT: ["Cake", "Pie", "Ice Cream", "Pudding", "Brownie", "Cookie", "Tart", "Cupcake", "Cheesecake", "Donut",
                    "Tiramisu", "Macaron", "Mousse", "Cannoli", "Baklava", "Churro", "Creme Brulee", "Eclair", "Gelato", "Souffle"],
    AttrName.CITY: ["New York", "Los Angeles", "Chicago", "Houston", "Seattle", "Boston", "Miami", "Denver", "San Francisco", "Atlanta",
                "Honolulu", "Austin", "Nashville", "New Orleans", "Las Vegas", "Portland", "Philadelphia", "San Diego", "Phoenix", "Detroit"],
    AttrName.BOOK: ["Moby Dick", "The Great Gatsby", "Pride and Prejudice", "1984", "The Hobbit", "To Kill a Mockingbird", "The Catcher in the Rye", "Little Women", "Jane Eyre", "Frankenstein",
                  "Wuthering Heights", "Brave New World", "Crime and Punishment", "War and Peace", "Anna Karenina", "The Odyssey", "Don Quixote", "The Iliad", "The Aeneid", "The Divine Comedy"],
    AttrName.VEHICLE: ["Car", "Bicycle", "Motorcycle", "Boat", "Airplane", "Train", "Bus", "Scooter", "Truck", "Helicopter",
                    "RV", "Jet Ski", "Segway", "Golf Cart", "Bullet Train", "Cable Car", "Hot Air Balloon", "Snowmobile", "Hovercraft", "Spaceship"],
    AttrName.OCCUPATION: ["Doctor", "Teacher", "Engineer", "Artist", "Chef", "Scientist", "Writer", "Musician", "Athlete", "Actor",
                       "Pilot", "Architect", "Designer", "Photographer", "Journalist", "Dentist", "Veterinarian", "Lawyer", "Accountant", "Firefighter"],
    AttrName.SPORT: ["Soccer", "Basketball", "Tennis", "Swimming", "Golf", "Baseball", "Volleyball", "Rugby", "Cricket", "Hockey",
                   "Badminton", "Table Tennis", "Archery", "Fencing", "Gymnastics", "Boxing", "Wrestling", "Surfing", "Skiing", "Snowboarding"],
    AttrName.FRUIT: ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew", "Kiwi", "Lemon",
                   "Mango", "Nectarine", "Orange", "Peach", "Pear", "Pineapple", "Plum", "Pomegranate", "Raspberry", "Strawberry"],
    AttrName.GEMSTONE: ["Diamond", "Ruby", "Emerald", "Sapphire", "Amethyst", "Topaz", "Opal", "Pearl", "Jade", "Garnet",
                     "Aquamarine", "Citrine", "Peridot", "Tanzanite", "Tourmaline", "Zircon", "Moonstone", "Alexandrite", "Lapis Lazuli", "Turquoise"],
    AttrName.COUNTRY: ["Canada", "Japan", "Brazil", "Italy", "Australia", "India", "South Africa", "Norway", "Thailand", "Mexico",
                    "Spain", "France", "Germany", "China", "Russia", "Egypt", "Argentina", "New Zealand", "Greece", "Sweden"],
    AttrName.MOVIE_GENRE: ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller", "Documentary", "Fantasy", "Mystery",
                         "Adventure", "Animation", "Crime", "Family", "History", "Musical", "War", "Western", "Noir", "Satire"],
    AttrName.WEATHER: ["Sunny", "Rainy", "Cloudy", "Snowy", "Windy", "Foggy", "Stormy", "Hail", "Thunder", "Clear",
                     "Overcast", "Drizzle", "Sleet", "Blizzard", "Hurricane", "Tornado", "Misty", "Humid", "Freezing Rain", "Sandstorm"],
    AttrName.SHOE_TYPE: ["Sneakers", "Boots", "Sandals", "Loafers", "High Heels", "Oxfords", "Flip Flops", "Slippers", "Clogs", "Espadrilles",
                       "Moccasins", "Brogues", "Ballerinas", "Wedges", "Mary Janes", "Galoshes", "Crocodile", "Jelly Shoes", "Wellingtons", "Stilettos"],
    AttrName.BODY_PART: ["Head", "Shoulders", "Knees", "Toes", "Fingers", "Elbows", "Ankles", "Wrists", "Hips", "Chest",
                      "Neck", "Back", "Stomach", "Thighs", "Calves", "Forehead", "Cheeks", "Chin", "Lips", "Ears"],
    AttrName.PROGRAMMING_LANGUAGE: ["Python", "JavaScript", "Java", "C", "C++", "C#", "PHP", "TypeScript", "Swift", "Go",
                      "Rust", "Kotlin", "Ruby", "Dart", "Scala", "Perl", "R", "Haskell", "Lua", "Julia"]
}