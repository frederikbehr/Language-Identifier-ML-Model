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
    word = word.lower()
    word = word.replace(",", "")
    word = word.replace(".", "")
    word = word.replace(":", "")
    word = word.replace(";", "")
    word = word.replace("_", "")
    word = word.replace("$", "")
    word = word.replace("§", "")
    word = word.replace("%", "")
    word = word.replace("/", "")
    word = word.replace("®", "")
    word = word.replace("“", "")
    word = word.replace("[", "")
    word = word.replace("]", "")
    if word not in processed_words:
      processed_words.append(word)
  return processed_words


# Check the data_languages
with OSFS('./data_languages') as fs:
  # Find directories
  directories = fs.listdir('.')
  for index, directory in enumerate(directories):
    # Each directory / data_languages per language
    # Get words and add to class object

    print(f"Starting {directory} ({index+1} / {len(directories)})")
    languages.append(Language(directory, []))
    files = fs.listdir(directory)
    for i, file in enumerate(files):
      # Getting data_languages from each file
      print(f"    {file} ({i+1} / {len(files)})")
      data = process_file("./data_languages/" + directory + "/" + file)
      languages[-1].add_words(data)

# Clear dataset.csv, so it won't contain duplicates
with open("./dataset.csv", 'w', newline='') as file:
  file.truncate(0)

# Set column labels
with open("./dataset.csv", 'w') as file:
  file.write("Word,Language\n")

# Get smallest size
smallestValue = 100000
for language in languages:
  if len(language.words) < smallestValue:
    smallestValue = len(language.words)
print(smallestValue)

for language in languages:
  print(language)
  print("Writing to csv")
  language.write_to_csv(smallestValue)

print("Application finished.")