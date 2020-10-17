from random import randint

class MarkovLyrics:
    def __init__(self):
        """
        self.chain = {
            "baby": ["plays", "crawls", "sleeps", "plays", "plays'],
            "plays": ["toy", "food"]
            }
        """
        self.chain = {}
        self.initial_words = []

    def populate_markov_chain(self, lyrics):
        for line in lyrics:
            words = line.split(" ")
            # add the first word of the line to the list of initial words
            if words[0] != "NEWLINE" and words[0] not in self.initial_words:
                self.initial_words.append(words[0])
            for i in range(len(words)-1):
                word = words[i]
                # add the first word of the new line to the list of initial words
                if word == "NEWLINE" and words[i+1] not in self.initial_words:
                    self.initial_words.append(words[i+1])
                # extend the chain
                if word in self.chain:
                    next_word = words[i+1]
                    self.chain[word].append(next_word)
                # add a new chain
                else:
                    next_word = words[i+1]
                    self.chain[word] = [next_word]
        # print(self.chain)
    def generate_lyrics(self, length=500):
        # pick a random word from the list of initial words
        n = len(self.initial_words)
        start_index = randint(0, n-1)
        keys = list(self.chain.keys())
        current_word = keys[start_index].title()

        lyrics = current_word + " "
        for _ in range(length):
            # when reaching the end of a sentence
            if current_word not in self.chain:
                lyrics += "\n"
                next_index = randint(0, n-1)
                current_word = keys[next_index]
            # if it is not the end of a sentence
            else:
                next_words = self.chain[current_word]
                next_index = randint(0, len(next_words)-1)
                next_word = next_words[next_index]
                lyrics += next_word + " "
                current_word = next_word
        return lyrics


""" test
data = ["I am Victiny", "I am a student", "I like to code", "I play basketball"]
m = MarkovLyrics()
m.populate_markov_chain(data)
print(m.chain)
print(m.generate_lyrics())
"""