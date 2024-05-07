from fs.osfs import OSFS

from language import Language

# Data stored here
languages = []


def process_file(path):
  with open(path, "r") as f:
    result = []
    lines = f.readlines()
    for line in lines:
      result.extend(preprocess(line))
    return result


def preprocess(line):
  # Removing comma, punctuation and separating words from lines
  words = line.split(" ")
  processed_words = []
  for word in words:
    word = word.strip()
    word = word.replace(",", "")
    word = word.replace(".", "")
    word = word.replace(":", "")
    word = word.replace(";", "")
    word = word.replace("_", "")
    word = word.replace("", "")
    if word not in processed_words:
      processed_words.append(word)
  return processed_words


# 44579
# 43764
# Check the data

with OSFS('./data') as fs:
  # Find directories
  directories = fs.listdir('.')
  for index, directory in enumerate(directories):
    # Each directory / data per language
    # Get words and add to class object

    print(f"Starting {directory} ({index+1} / {len(directories)})")
    languages.append(Language(directory, []))
    files = fs.listdir(directory)
    for i, file in enumerate(files):
      # Getting data from each file
      print(f"    {file} ({i+1} / {len(files)})")
      data = process_file("./data/" + directory + "/" + file)
      languages[-1].add_words(data)

# Clear dataset.csv, so it won't contain duplicates
with open("./dataset.csv", 'w', newline='') as file:
  file.truncate(0)

# Set column labels
with open("./dataset.csv", 'w') as file:
  file.write("Word,Language\n")

for language in languages:
  print(language)
  print("Writing to csv")
  language.write_to_csv()

print("Application finished.")