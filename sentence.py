from fs.osfs import OSFS

from language import Language

# Data stored here
languages = []

min_length = 10
max_length = 50


def process_file(path):
  with open(path, "r") as f:
    result = []
    lines = f.readlines()
    for line in lines:
      result.extend(preprocess(line))
    return result


def preprocess(line):
  # Removing comma, punctuation and separating words from lines
  sentences = line.split(".")
  processed_sentences = []
  for sentence in sentences:
    if max_length >= len(sentence) >= min_length:
      sentence = sentence.strip()
      sentence = sentence.lower()
      sentence = sentence.replace(",", "")
      sentence = sentence.replace(".", "")
      sentence = sentence.replace(":", "")
      sentence = sentence.replace(";", "")
      sentence = sentence.replace("_", "")
      sentence = sentence.replace("$", "")
      sentence = sentence.replace("§", "")
      sentence = sentence.replace("%", "")
      sentence = sentence.replace("/", "")
      sentence = sentence.replace("|", "")
      sentence = sentence.replace("*", "")
      sentence = sentence.replace("®", "")
      sentence = sentence.replace("“", "")
      sentence = sentence.replace("—", "")
      sentence = sentence.replace("[", "")
      sentence = sentence.replace("]", "")
      sentence = sentence.replace("1", "")
      sentence = sentence.replace("2", "")
      sentence = sentence.replace("3", "")
      sentence = sentence.replace("4", "")
      sentence = sentence.replace("5", "")
      sentence = sentence.replace("6", "")
      sentence = sentence.replace("7", "")
      sentence = sentence.replace("8", "")
      sentence = sentence.replace("9", "")
      sentence = sentence.replace("0", "")
      sentence = sentence.replace("!", "")
      sentence = sentence.replace("+", "")
      sentence = sentence.replace("-", "")
      sentence = sentence.replace(")", "")
      sentence = sentence.replace("(", "")
      sentence = sentence.replace("[", "")
      sentence = sentence.replace("]", "")
      sentence = sentence.replace('"', "")
      sentence = sentence.replace('»', "")
      sentence = sentence.replace('«', "")
      sentence = sentence.replace('', "")
      sentence = sentence.replace('=', "")
      sentence = sentence.replace('"', "")
      sentence = sentence.replace('harry', "")
      sentence = sentence.replace('potter', "")
      sentence = sentence.replace('hagrid', "")
      sentence = sentence.replace('hermione', "")
      sentence = sentence.replace('dumbledore', "")
      sentence = sentence.replace('ron', "")
      sentence = sentence.replace('weasley', "")
      sentence = sentence.replace('„', "")
      sentence = sentence.replace('  ', " ")
      sentence = sentence.replace('   ', " ")
      sentence = sentence.replace('    ', " ")
      sentence = sentence.replace('     ', " ")
      sentence = sentence.replace('      ', " ")
      sentence = sentence.replace('       ', " ")
      sentence = sentence.replace('        ', " ")
      if sentence not in processed_sentences:
        processed_sentences.append(sentence)
  return processed_sentences


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

# Filter by length
for language in languages:
  language.remove_by_length(min_length=min_length, max_length=max_length)

# Get smallest size
smallestValue = 100000
for language in languages:
  if len(language.words) < smallestValue:
    smallestValue = len(language.words)
print(smallestValue)

print("Writing to csv")
for language in languages:
  print(language)
  language.write_to_csv(smallestValue)

print("Application finished.")