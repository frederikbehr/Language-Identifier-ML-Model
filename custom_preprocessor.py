from unidecode import unidecode
import re


def remove_special_characters(text):
  characters_to_remove = ",.:;_$§%|*/®“'—[]”!+-()\"»«=\"„¡¿?"
  text = re.sub(r'[{}]'.format(re.escape(characters_to_remove)), '', text)
  return text


def remove_names(text):
  names_to_remove = ['harry', 'potter', 'hagrid', 'hermione', 'dumbledore', 'ron', 'weasley', 'columbus',
                     'christophorus', 'poul', 'paul', 'atreides', 'image', 'matilda', 'hermionel', 'neville',
                     'sport', 'filch', 'voldemort', 'draco', 'malfoy', 'lucius', 'garri', 'Narcissa', 'minerva',
                     'mcgonngall', "privet drive"]
  pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, names_to_remove)))
  return re.sub(pattern, '', text, flags=re.IGNORECASE)


def remove_numbers(text):
  text = text.translate(str.maketrans('', '', '1234567890'))
  return text


def remove_spaces(text):
  text = re.sub(r'\s+', ' ', text)
  return text


def change_characters(text):
  return unidecode(text)


def equalize_length(text):
  max_length = 48
  words = text.split(" ")
  words = words * 4
  result = text
  for word in words:
    if len(result) + len(word) < max_length:
      result = " ".join([result, word])
    else:
      return result
  return result


def preprocess(text):
  text = text.strip()
  text = text.lower()
  text = remove_numbers(text)
  text = remove_spaces(text)
  text = remove_special_characters(text)
  text = change_characters(text)
  text = remove_special_characters(text)
  text = remove_names(text)
  result = equalize_length(text)
  return result
