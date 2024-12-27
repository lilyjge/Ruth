import re

def swap_perspectives(input_text):
    # Define all replacements in a single pass
    replacement_map = {
        'i': 'you', 'me': 'you', 'my': 'your', 'myself': 'yourself', 'mine': 'yours', 'am': 'are', 
        'you': 'I', 'your': 'my', 'yourself': 'myself', 'yours': 'mine'
    }

    # Create a regex pattern that matches all keys
    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in replacement_map.keys()) + r')\b', flags=re.IGNORECASE)

    # Function to perform replacement with case preservation
    def replace(match):
        word = match.group(0)
        replacement = replacement_map[word.lower()]  # Look up replacement in lowercase
        # Preserve case
        return replacement
            
    # Apply the regex and replacement function
    return pattern.sub(replace, input_text)

# Example usage
# text = "I thought you were my friend, but you helped yourself to my cake!"
# converted_text = swap_perspectives(text)
# print(converted_text)
