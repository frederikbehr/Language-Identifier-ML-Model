import csv
import random
from dataclasses import dataclass


def is_not_num(value):
  try:
    float(value)
    return False
  except ValueError:
    return True


@dataclass
class Language:
  language: str
  words: list[str]

  def add_words(self, new_words: list[str]):
    for word in new_words:
      if self.can_add(word):
        self.words.append(word)

  def can_add(self, word):
    if word not in self.words and len(word) > 4:
      return True
    else:
      return False

  def get_random_word(self):
    if len(self.words) <= 2:
      return "Empty"
    else:
      return random.choice(self.words)

  def write_to_csv(self, rows):
    with open("./dataset.csv", 'a', newline='') as file:
      writer = csv.writer(file)
      count = 0
      for word in self.words:
        if count is rows:
          break
        writer.writerow([word.strip(), self.language])
        count = count + 1

  def remove_by_length(self, min_length, max_length):
    result = []
    for word in self.words:
      if min_length <= len(word) <= max_length:
        result.append(word)
    self.words = result

  def __repr__(self):
    return (self.language
            + " with size="
            + str(len(self.words))
            + ", random selection="
            + str(self.get_random_word()))
