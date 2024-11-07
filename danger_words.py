def GetDangerWords():
    words_file = open("concerning_words.txt")
    danger_words = []
    for word in words_file:
        danger_words.append(word.rstrip())
    return danger_words
