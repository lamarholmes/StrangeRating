#Input score per 1-10 episode watched
import sqlite3
import json
import codecs

print("Welcome Stranger Score \nPlease rate Stranger Things Episode score")

conn = sqlite3.connect('EpisodeScore.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Episode (
		id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
		Title TEXT, 
		Episode_Number INTEGER,
		Rating INTEGER,
		Favorite_Character TEXT)
''')

moreScore = True

while moreScore:

	Episode_Title = input("What is the Episode Title: ")
	Episode_Number = int(input("Episode Number: "))
	Episode_Rating = int(input("What do you rate the episode (1-10): "))
	Fav_Character = input("Who was your favorite character: ")

	cur.execute('''INSERT INTO Episode (Title, Episode_Number, Rating, Favorite_Character)
            VALUES ( ?, ?, ?, ? )''', (Episode_Title, Episode_Number, Episode_Rating, Fav_Character ) )

	conn.commit()
	moreInputs = input("Do you have more scores to enter?(Y/N): ")
	while moreInputs != 'Y' and moreInputs != 'N' and moreInputs != 'Yes' and moreInputs != 'No':
		moreInputs = input('Do you have more scores to enter?(Y/N): ')
	if moreInputs == 'N' or moreInputs == 'No':
		moreScore = False

print("Thanks for the ratings")
print("Building Display")

cur.execute('SELECT * FROM Episode')
fhand = codecs.open('ratings.js', 'w', "utf-8")
fhand.write("myData =")
rateArr = []

rows = [x for x in cur]
cols = [x[0] for x in cur.description]

for row in rows:
	rate = {}
	for prop, val in zip(cols, row):
		rate[prop] = val
	rateArr.append(rate)

fhand.write(json.dumps(rateArr))
#fhand.write("\n];\n")
cur.close()
fhand.close()

print("Check page now!")

