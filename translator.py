from googletrans import Translator

tr = Translator()

text = input(" Enter text to translate: \n")

lang = input(" Enter language code : (en / fa ...)\n")



translation = tr.translate(text, dest=lang)


print("\n \n")
print(translation.text)


