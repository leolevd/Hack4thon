import json
import string

# Custom counter class (avoiding dependencies like collections.Counter)
class Counter:
    @staticmethod
    def count_words(string: str):
        words_count = {}
        for word in string.split():
            if word in words_count:
                words_count[word] += 1
            else:
                words_count[word] = 1
        return words_count


# Removes zero-width and invisible Unicode characters from text
def zero_width_cleaner(s: str):
    zero_width_chars = [
        '\u200B',  # Zero Width Space
        '\u200C',  # Zero Width Non-Joiner
        '\u200D',  # Zero Width Joiner
        '\u2060',  # Word Joiner
        '\uFEFF',  # Byte Order Mark
    ]
    for e in zero_width_chars:
        s = s.replace(e, "")
    return s


# Load the dataset (expected to have "spam" and "ham" keys)
with open("collection.json") as f:
    data = json.load(f)

# Extract spam and ham samples
spam_texts = data["spam"]
ham_texts = data["ham"]

# Initialize word frequency dictionaries
ham_dict = {}
spam_dict = {}

# Count words for ham messages
for h in ham_texts:
    wordscount = Counter.count_words(zero_width_cleaner(h.lower()))
    for w in wordscount:
        if w in ham_dict:
            ham_dict[w] += wordscount[w]
        else:
            ham_dict[w] = wordscount[w]

# Count words for spam messages
for s in spam_texts:
    wordscount = Counter.count_words(s.lower())
    for w in wordscount:
        if w in spam_dict:
            spam_dict[w] += wordscount[w]
        else:
            spam_dict[w] = wordscount[w]

# Remove rarely used words and round frequencies
correct_ham_dict = {k: round(v) for k, v in ham_dict.items() if v > 1}
correct_spam_dict = {k: round(v) for k, v in spam_dict.items() if v > 1}


# Compares words in text with ham/spam dictionaries and gives weighted points
def collection_filter(string: str, ham_pic: dict, spam_pic: dict):
    counts = Counter.count_words(zero_width_cleaner(string.lower()))
    SPAM_POINTS = 0
    HAM_POINTS = 0
    for i in counts:
        if i in ham_pic and not i in spam_pic:
            HAM_POINTS += 1.5
        elif i in spam_pic and not i in ham_pic:
            SPAM_POINTS += 2.0
        elif i in ham_pic and i in spam_pic:
            if ham_pic[i] > spam_pic[i]:
                HAM_POINTS += 1.5
            else:
                SPAM_POINTS += 2.0
        else:
            pass
    return "SPAM" if SPAM_POINTS >= HAM_POINTS else "HAM"


# Detects suspicious keywords often used in spam
def susWords_filter(sentence: str):
    return "SPAM" if any([w in zero_width_cleaner(sentence.lower()) for w in [
        "won", "$", "@", "http", "+", "claim", "free", "click",
        "dollar", ".com", ".xyz", ".io", ".ly"
    ]]) else "HAM"


# Checks if the text uses too many capital letters
def CAPS_check(sentence: str):
    CAPS_count = 0
    for l in sentence:
        if l in string.ascii_uppercase:
            CAPS_count += 1
    return "SPAM" if CAPS_count * 10 >= len(sentence) else "HAM"


# Detects hidden Unicode zero-width characters (used for obfuscation)
def zero_width_analyser(s: str):
    zero_width_chars = [
        '\u200B',
        '\u200C',
        '\u200D',
        '\u2060',
        '\uFEFF',
    ]
    return "SPAM" if (any([i in s for i in zero_width_chars])) else "HAM"


# Main spam filter combining all detection methods
def spam_filter(*args):
    result1 = 1 if (collection_filter(args[0], args[1], args[2]) == "SPAM") else -1
    result2 = 0.5 if (susWords_filter(args[0]) == "SPAM") else -0.5
    result3 = 0.5 if (CAPS_check(args[0]) == "SPAM") else -0.5
    result4 = 1 if (zero_width_analyser(args[0]) == "SPAM") else 0
    # If the total suspicion score is positive, mark as spam
    return "SPAM" if sum([result1, result2, result3, result4]) >= 0 else "HAM"


# Basic tests to verify filter behavior
try:
    assert spam_filter("You won a free car!", ham_dict, spam_dict) == "SPAM"
    assert spam_filter("You won 20 million dollars! Call 8743 to claim!", ham_dict, spam_dict) == "SPAM"
    assert spam_filter("You won a car! Call us: +74 5389 45983", ham_dict, spam_dict) == "SPAM"
    assert spam_filter("Hi! How are you?", ham_dict, spam_dict) == "HAM"
    assert spam_filter("Bro, let's go out at noon", ham_dict, spam_dict) == "HAM"
    assert spam_filter("mb better tomorrow?", ham_dict, spam_dict) == "HAM"
    assert spam_filter("Hello Marjung. Your visa application was sucsessfully submited", ham_dict, spam_dict) == "HAM"
except AssertionError:
    raise ValueError("Tests failed")
