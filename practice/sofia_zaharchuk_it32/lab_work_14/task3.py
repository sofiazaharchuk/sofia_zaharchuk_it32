import qrcode

NAME, SURNAME, GROUP = "Sofiia", "Zakharchuk", "IT-32"
EMAIL = "sofia.zaharchuk12@gmail.com"

print(f"{NAME} {SURNAME}, {GROUP}")

text = f"{NAME} {SURNAME}, {GROUP}, {EMAIL}"
image = qrcode.make(text)
image.save("contact.png")
print("saved: contact.png")
