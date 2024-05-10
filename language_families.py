from fs.osfs import OSFS
from language import Language
from custom_preprocessor import preprocess

# Data stored here
languages = []
target_languages = []

min_length = 8
max_length = 30


def get_files():
  # Check the data_languages
  with OSFS('./data_families') as fs:
    # Find directories
    directories = fs.listdir('.')
    for index, directory in enumerate(directories):
      # Each directory / data_languages per language
      # Get words and add to class object
      if len(target_languages) == 0 or directory in target_languages:
        print(f"Starting {directory} ({index + 1} / {len(directories)})")
        languages.append(Language(directory, []))
        files = fs.listdir(directory)
        for i, file in enumerate(files):
          # Getting data_languages from each file
          print(f"    {file} ({i + 1} / {len(files)})")
          data = process_file("./data_families/" + directory + "/" + file)
          languages[-1].add_words(data)


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


def handle_data():
  # Clear dataset.csv, so it won't contain duplicates
  print("Removing previous data_languages set...")
  with open("./dataset.csv", 'w', newline='') as file:
    file.truncate(0)

  # Set column labels
  print("Inserting titles...")
  with open("./dataset.csv", 'w') as file:
    file.write("Word,Language\n")

  # Shuffling data_languages
  print("Shuffling data_languages sets...")
  for language in languages:
    language.shuffle()

  # Filter by length
  print("Equalizing the lengths of data_languages...")
  for language in languages:
    language.remove_by_length(min_length=min_length, max_length=max_length)

  # Get smallest size
  print("Finding smallest data_languages set")
  smallestValue = 100000
  for language in languages:
    if len(language.words) < smallestValue:
      smallestValue = len(language.words)

  print("Writing to csv")
  for language in languages:
    print(language)
    language.write_to_csv(smallestValue)

  print("Application finished.")


def generate_data():
  get_files()
  handle_data()
