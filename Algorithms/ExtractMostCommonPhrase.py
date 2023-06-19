from collections import Counter
import re


def extractMostCommonPhrase(sentences):
    phrase_counts = Counter()

    for sentence in sentences:
        # Extract multi-word phrases using regular expressions
        phrases = re.findall(r'\b\w+(?:\s+\w+){1,}\b', sentence.lower())

        # Count the occurrences of each phrase
        phrase_counts.update(phrases)

    # Find the most common phrase
    most_common_phrase = phrase_counts.most_common(
        1)[0][0]
    return str(most_common_phrase).title()
