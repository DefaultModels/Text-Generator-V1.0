import re
import tqdm
from random import choice, random

data = {}

def crunch(file):
		words = []
		with open(file, "r") as f:
				text = re.findall(r"\w+(?:'\w+)?|[^\s\w]+", f.read())

				for word in tqdm.tqdm(text, desc="Memorizing text.txt..."):
						words.append(word.lower())

				for word in tqdm.tqdm(text, desc="Creating dicts..."):
						data[str(word)] = {"next": {}, "previous": []}

				count = 0
				for word in tqdm.tqdm(text, desc="Crunching..."):
						try:
								if count < len(words):
										next_word = words[count + 1]
										if next_word not in data[str(word)]["next"]:
												data[str(word)]["next"][next_word] = 0
										data[str(word)]["next"][next_word] += 1

								if count > 0:
										data[str(word)]["previous"].append(words[count - 1])
						except:
								pass
						count += 1
		print()
		return data


def generate_sentence(data, force_dot=False):
		sentence = []
		current_word = choice(list(data.keys()))
		sentence.append(current_word)

		while True:
				if random() < 0.6:
						next_word = max(data[current_word]["next"].items(), key=lambda item: item[1])[0]
				else:
						next_word = choice(list(data[current_word]["next"].keys()))

				if force_dot and next_word == ".":
						force_dot = False
				else:
						if not data[current_word]["next"]:
								break

				sentence.append(next_word)
				current_word = next_word

				if next_word == ".":
						break

		return " ".join(sentence)


print(generate_sentence(crunch("text.txt"), force_dot=True))
