from fs.osfs import OSFS

from language import Language
from custom_preprocessor import preprocess

# Data stored here
languages = []
target_languages = []

min_length = 8
max_length = 30


def process_file(path):
  with open(path, "r") as f:
    result = []
    lines = f.readlines()
    for line in lines:
      result.extend(process_text(line))
    return result


def process_text(line):
  # Removing comma, punctuation and separating words from lines
  sentences = line.split(".")
  processed_sentences = []
  for sentence in sentences:
    words = sentence.split(" ")
    if len(sentence) > min_length:
      processed_sentences.extend(split_into_lists(preprocess(" ".join(words[:3]))))
  return processed_sentences


def split_into_lists(text):
  words = text.split()
  result = []
  i = 0
  while i < len(words):
    sublist = [words[i]]
    if i + 1 < len(words):
      sublist.append(words[i + 1])
      if i + 2 < len(words):
        sublist.append(words[i + 2])
    result.append(" ".join(sublist))
    i += len(sublist)
  return result


# Check the data
with OSFS('./data_families') as fs:
  # Find directories
  directories = fs.listdir('.')
  for index, directory in enumerate(directories):
    # Each directory / data per language
    # Get words and add to class object
    if len(target_languages) == 0 or directory in target_languages:
      print(f"Starting {directory} ({index + 1} / {len(directories)})")
      languages.append(Language(directory, []))
      files = fs.listdir(directory)
      for i, file in enumerate(files):
        # Getting data from each file
        print(f"    {file} ({i + 1} / {len(files)})")
        data = process_file("./data_families/" + directory + "/" + file)
        languages[-1].add_words(data)


# Clear dataset.csv, so it won't contain duplicates
print("Removing previous data set...")
with open("./dataset.csv", 'w', newline='') as file:
  file.truncate(0)

# Set column labels
print("Inserting titles...")
with open("./dataset.csv", 'w') as file:
  file.write("Word,Language\n")

# Shuffling data
print("Shuffling data sets...")
for language in languages:
  language.shuffle()

# Filter by length
print("Equalizing the lengths of data...")
for language in languages:
  language.remove_by_length(min_length=min_length, max_length=max_length)

# Get smallest size
print("Finding smallest data set")
smallestValue = 100000
for language in languages:
  if len(language.words) < smallestValue:
    smallestValue = len(language.words)

print("Writing to csv")
for language in languages:
  print(language)
  language.write_to_csv(smallestValue)

print("Application finished.")