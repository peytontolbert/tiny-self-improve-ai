# Self-Improving Swarm Tools Documentation

Total tools: 47

## String Tools

### capitalize_words

```python
def capitalize_words(text: str) -> str:
    """
    Capitalize the first letter of each word in a given string.

    Args:
        text (str): The input string to transform.

    Returns:
        str: A new string with the first letter of each word capitalized.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("python programming")
        'Python Programming'
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Split the text into words, capitalize each word, and join them back
    capitalized_text = ' '.join(word.capitalize() for word in text.split())

    return capitalized_text

```

### count_word_occurrences

```python
def count_word_occurrences(text: str) -> dict[str, int]:
    """
    Count the occurrences of each word in a given string.

    Args:
        text (str): The input string to analyze.

    Returns:
        dict[str, int]: A dictionary with words as keys and their occurrence counts as values.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> count_word_occurrences("hello world hello")
        {'hello': 2, 'world': 1}
        >>> count_word_occurrences("Python is great and Python is fun")
        {'python': 2, 'is': 2, 'great': 1, 'and': 1, 'fun': 1}
    """
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Convert text to lowercase and split into words
    words = text.lower().split()

    # Use a dictionary to count occurrences of each word
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    # Log the word count result
    logging.debug(f"Word occurrences: {word_count}")

    return word_count

```

### debug_dict_structure

```python
def debug_dict_structure(data: dict) -> dict[str, any]:
    """
    Analyze the structure of a dictionary, providing details about its keys and values, including types and nested levels.

    This function inspects a dictionary and returns a dictionary containing information about the types of keys and values,
    the depth of nesting, and the count of each type of key and value.

    Args:
        data (dict): The dictionary to analyze.

    Returns:
        dict[str, any]: A dictionary with keys 'key_types', 'value_types', 'max_depth', 'key_type_counts', and 'value_type_counts'
                        providing details about the dictionary structure.

    Raises:
        ValueError: If the input is not a dictionary.

    Example:
        >>> debug_dict_structure({'a': 1, 'b': "text", 'c': {'d': 2}})
        {'key_types': ['str'], 'value_types': ['int', 'str', 'dict'], 'max_depth': 2, 'key_type_counts': {'str': 3}, 'value_type_counts': {'int': 2, 'str': 1, 'dict': 1}}
    """
    import logging
    from collections import defaultdict

    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary.")

    def analyze_structure(d: dict, depth: int = 0) -> tuple[set, set, int, defaultdict, defaultdict]:
        key_types = set()
        value_types = set()
        max_depth = depth
        key_type_counts = defaultdict(int)
        value_type_counts = defaultdict(int)

        for key, value in d.items():
            key_type = type(key).__name__
            value_type = type(value).__name__
            key_types.add(key_type)
            value_types.add(value_type)
            key_type_counts[key_type] += 1
            value_type_counts[value_type] += 1

            if isinstance(value, dict):
                sub_key_types, sub_value_types, sub_depth, sub_key_counts, sub_value_counts = analyze_structure(value, depth + 1)
                key_types.update(sub_key_types)
                value_types.update(sub_value_types)
                max_depth = max(max_depth, sub_depth)
                for k, v in sub_key_counts.items():
                    key_type_counts[k] += v
                for k, v in sub_value_counts.items():
                    value_type_counts[k] += v

        return key_types, value_types, max_depth, key_type_counts, value_type_counts

    key_types, value_types, max_depth, key_type_counts, value_type_counts = analyze_structure(data)

    result = {
        'key_types': list(key_types),
        'value_types': list(value_types),
        'max_depth': max_depth,
        'key_type_counts': dict(key_type_counts),
        'value_type_counts': dict(value_type_counts)
    }

    logging.debug(f"dictionary structure analysis: {result}")

    return result

```

### debug_list_structure

```python
def debug_list_structure(data: list) -> dict[str, any]:
    """
    Analyze the structure of a list, providing details about its elements, including types and nested levels.

    This function inspects a list and returns a dictionary containing information about the types of elements,
    the depth of nesting, and the count of each type of element.

    Args:
        data (list): The list to analyze.

    Returns:
        dict[str, any]: A dictionary with keys 'element_types', 'max_depth', and 'type_counts' providing
                        details about the list structure.

    Raises:
        ValueError: If the input is not a list.

    Example:
        >>> debug_list_structure([1, "text", [2, 3], {"key": "value"}])
        {'element_types': ['int', 'str', 'list', 'dict'], 'max_depth': 2, 'type_counts': {'int': 1, 'str': 1, 'list': 1, 'dict': 1}}
    """
    import logging
    from collections import defaultdict

    if not isinstance(data, list):
        raise ValueError("Input must be a list.")

    def analyze_structure(lst: list, depth: int = 0) -> tuple[set, int, defaultdict]:
        element_types = set()
        max_depth = depth
        type_counts = defaultdict(int)

        for element in lst:
            element_type = type(element).__name__
            element_types.add(element_type)
            type_counts[element_type] += 1

            if isinstance(element, list):
                sub_types, sub_depth, sub_counts = analyze_structure(element, depth + 1)
                element_types.update(sub_types)
                max_depth = max(max_depth, sub_depth)
                for key, value in sub_counts.items():
                    type_counts[key] += value

        return element_types, max_depth, type_counts

    element_types, max_depth, type_counts = analyze_structure(data)

    result = {
        'element_types': list(element_types),
        'max_depth': max_depth,
        'type_counts': dict(type_counts)
    }

    logging.debug(f"list structure analysis: {result}")

    return result

```

### find_longest_word

```python
def find_longest_word(text: str) -> str:
    """
    Find the longest word in a given string.

    This function scans through the input string and returns the longest word found.
    If there are multiple words with the same maximum length, the first one encountered is returned.

    Args:
        text (str): The input string to analyze.

    Returns:
        str: The longest word in the input string.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> find_longest_word("The quick brown fox jumps over the lazy dog")
        'jumps'
        >>> find_longest_word("Python programming is fun")
        'programming'
    """
    import logging
    import re

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Use regex to find words in the text
    words = re.findall(r'\b\w+\b', text)

    if not words:
        return ""

    # Find the longest word
    longest_word = max(words, key=len)

    # Log the longest word found
    logging.debug(f"Text: '{text}', Longest word: '{longest_word}'")

    return longest_word

```

### hash_password

```python
def hash_password(password: str, salt: str = None) -> dict[str, str]:
    """
    Hash a password using SHA-256 with an optional salt.

    This function takes a password and an optional salt, hashes the password using the SHA-256 algorithm,
    and returns the hashed password along with the salt used. If no salt is provided, a random salt is generated.

    Args:
        password (str): The password to be hashed.
        salt (str, optional): An optional salt to use for hashing. If not provided, a random salt is generated.

    Returns:
        dict[str, str]: A dictionary containing the 'salt' and the 'hashed_password'.

    Raises:
        ValueError: If the password is not a string or if the salt is provided and is not a string.

    Example:
        >>> hash_password("my_secure_password")
        {'salt': 'randomly_generated_salt', 'hashed_password': 'hashed_value'}
        >>> hash_password("my_secure_password", "custom_salt")
        {'salt': 'custom_salt', 'hashed_password': 'hashed_value'}
    """
    import hashlib
    import os
    import logging

    if not isinstance(password, str):
        raise ValueError("Password must be a string.")
    if salt is not None and not isinstance(salt, str):
        raise ValueError("Salt must be a string if provided.")

    # Generate a random salt if not provided
    if salt is None:
        salt = os.urandom(16).hex()

    # Create the hash using SHA-256
    hash_obj = hashlib.sha256()
    hash_obj.update((salt + password).encode('utf-8'))
    hashed_password = hash_obj.hexdigest()

    result = {'salt': salt, 'hashed_password': hashed_password}

    logging.debug(f"Password hashing: salt={salt}, hashed_password={hashed_password}")

    return result

```

### normalize_text

```python
def normalize_text(text: str) -> str:
    """
    Normalize a given string by converting it to lowercase and removing extra spaces.

    Args:
        text (str): The input string to normalize.

    Returns:
        str: A normalized string with all characters in lowercase and extra spaces removed.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> normalize_text("  Hello,   WORLD!  ")
        'hello, world!'
        >>> normalize_text("Python   Programming")
        'python programming'
    """
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Convert text to lowercase
    lower_text = text.lower()

    # Remove extra spaces
    normalized_text = ' '.join(lower_text.split())

    # Log the normalization process
    logging.debug(f"Original text: '{text}', Normalized text: '{normalized_text}'")

    return normalized_text

```

### optimize_string_list

```python
def optimize_string_list(strings: list[str]) -> list[str]:
    """
    Optimize a list of strings by removing duplicates and sorting them alphabetically.

    This function takes a list of strings, removes any duplicate entries, and returns a new list
    with the strings sorted in alphabetical order. The function ensures that each string appears
    only once in the resulting list.

    Args:
        strings (list[str]): A list of strings to be optimized.

    Returns:
        list[str]: A new list containing the unique strings sorted alphabetically.

    Raises:
        ValueError: If the input is not a list of strings.

    Example:
        >>> optimize_string_list(["apple", "banana", "apple", "cherry"])
        ['apple', 'banana', 'cherry']
        >>> optimize_string_list(["dog", "cat", "bird", "cat"])
        ['bird', 'cat', 'dog']
    """
    import logging

    if isinstance(strings, str):
        strings = [strings]
    elif not isinstance(strings, list):
        raise ValueError("Input must be a list of strings or a single string.")
    if not all(isinstance(s, str) for s in strings):
        raise ValueError("All elements in the list must be strings.")

    # Remove duplicates by converting to a set, then sort the result
    optimized_list = sorted(set(strings))

    logging.debug(f"Original list: {strings}, Optimized list: {optimized_list}")

    return optimized_list
```

## Math Tools

### calculate_average

```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list[float]): A list of numbers to calculate the average.

    Returns:
        float: The average of the numbers in the list.

    Raises:
        ValueError: If the input is not a list of numbers or if the list is empty.

    Example:
        >>> calculate_average([1.0, 2.0, 3.0, 4.0, 5.0])
        3.0
        >>> calculate_average([10, 20, 30])
        20.0
    """
    import logging

    if not isinstance(numbers, list):
        if isinstance(numbers, (int, float)):
            numbers = [numbers]
        else:
            raise ValueError("Input must be a list of numbers or a single number.")
    
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be numbers (int or float).")

    total = sum(numbers)
    count = len(numbers)
    average = total / count

    logging.debug(f"Calculated average: {average}")

    return average
```

### calculate_median

```python
def calculate_median(numbers: list[float]) -> float:
    """
    Calculate the median of a list of numbers.

    The median is the middle value in a list of numbers. If the list has an even number of elements,
    the median is the average of the two middle numbers.

    Args:
        numbers (list[float]): A list of numbers to calculate the median.

    Returns:
        float: The median of the numbers in the list.

    Raises:
        ValueError: If the input is not a list of numbers or if the list is empty.

    Example:
        >>> calculate_median([1, 3, 3, 6, 7, 8, 9])
        6.0
        >>> calculate_median([1, 2, 3, 4, 5, 6, 8, 9])
        4.5
    """
    import logging

    if not isinstance(numbers, list):
        numbers = [numbers]
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be numbers (int or float).")

    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2

    if n % 2 == 0:
        median = (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2.0
    else:
        median = sorted_numbers[mid]

    logging.debug(f"Sorted numbers: {sorted_numbers}, Median: {median}")

    return median
```

### calculate_mode

```python
def calculate_mode(numbers: list[float]) -> list[float]:
    """
    Calculate the mode(s) of a list of numbers.

    The mode is the number that appears most frequently in a list. If multiple numbers have the same highest frequency,
    all of them are returned.

    Args:
        numbers (list[float]): A list of numbers to calculate the mode.

    Returns:
        list[float]: A list containing the mode(s) of the numbers in the list.

    Raises:
        ValueError: If the input is not a list of numbers or if the list is empty.

    Example:
        >>> calculate_mode([1, 2, 2, 3, 4, 4, 4, 5])
        [4]
        >>> calculate_mode([1, 1, 2, 2, 3])
        [1, 2]
    """
    import logging
    from collections import Counter

    if not isinstance(numbers, list):
        numbers = [numbers]
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be numbers (int or float).")

    # Count the frequency of each number
    frequency = Counter(numbers)
    max_count = max(frequency.values())
    modes = [num for num, count in frequency.items() if count == max_count]

    logging.debug(f"Number frequencies: {frequency}, Modes: {modes}")

    return modes
```

### calculate_standard_deviation

```python
def calculate_standard_deviation(numbers: list[float]) -> float:
    """
    Calculate the standard deviation of a list of numbers.

    The standard deviation is a measure of the amount of variation or dispersion in a set of values.
    A low standard deviation indicates that the values tend to be close to the mean of the set,
    while a high standard deviation indicates that the values are spread out over a wider range.

    Args:
        numbers (list[float]): A list of numbers to calculate the standard deviation.

    Returns:
        float: The standard deviation of the numbers in the list.

    Raises:
        ValueError: If the input is not a list of numbers or if the list is empty.

    Example:
        >>> calculate_standard_deviation([1.0, 2.0, 3.0, 4.0, 5.0])
        1.4142135623730951
        >>> calculate_standard_deviation([10, 12, 23, 23, 16, 23, 21, 16])
        4.898979485566356
    """
    import logging
    import math

    if not isinstance(numbers, list):
        numbers = [numbers]
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be numbers (int or float).")

    mean = sum(numbers) / len(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    standard_deviation = math.sqrt(variance)

    logging.debug(f"Numbers: {numbers}, Mean: {mean}, Variance: {variance}, Standard Deviation: {standard_deviation}")

    return standard_deviation

```

### filter_even_numbers

```python
def filter_even_numbers(numbers: list[int]) -> list[int]:
    """
    Filter even numbers from a list of integers.

    Args:
        numbers (list[int]): A list of integers to filter.

    Returns:
        list[int]: A list containing only the even integers from the input list.

    Raises:
        ValueError: If the input is not a list of integers.

    Example:
        >>> filter_even_numbers([1, 2, 3, 4, 5, 6])
        [2, 4, 6]
    """
    if not isinstance(numbers, list):
        raise ValueError("Input must be a list of integers.")
    if not all(isinstance(num, int) for num in numbers):
        raise ValueError("All elements in the list must be integers.")

    even_numbers = [num for num in numbers if num % 2 == 0]
    return even_numbers

```

### validate_phone_number_format

```python
def validate_phone_number_format(phone_number: str) -> bool:
    """
    Validate the format of a phone number.

    This function checks if the phone number follows a standard format, such as
    (XXX) XXX-XXXX or XXX-XXX-XXXX, where X is a digit.

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        bool: True if the phone number format is valid, False otherwise.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> validate_phone_number_format("(123) 456-7890")
        True
        >>> validate_phone_number_format("123-456-7890")
        True
        >>> validate_phone_number_format("1234567890")
        False
    """
    import re
    import logging

    if not isinstance(phone_number, str):
        raise ValueError("The phone number must be a string.")

    # Define a regular expression for validating phone numbers
    phone_regex = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'

    # Check if the phone number matches the regex pattern
    is_valid = re.match(phone_regex, phone_number) is not None

    # Log the result
    logging.debug(f"Phone number validation for '{phone_number}': {is_valid}")

    return is_valid

```

## File Tools

### read_file_lines

```python
def read_file_lines(file_path: str) -> list[str]:
    """
    Read all lines from a file and return them as a list of strings.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list[str]: A list containing each line of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
        PermissionError: If there is no permission to read the file.
        ValueError: If the file path is not a string.

    Example:
        >>> read_file_lines('example.txt')
        ['First line\n', 'Second line\n', 'Third line\n']
    """
    import os

    if not isinstance(file_path, str):
        raise ValueError("The file path must be a string.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"No permission to read the file at {file_path}.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines

```

## Data Tools

### create_frequency_dict

```python
def create_frequency_dict(elements: list) -> dict:
    """
    Create a frequency dictionary from a list of elements.

    This function takes a list of elements and returns a dictionary where the keys are the unique elements
    from the list and the values are the counts of how many times each element appears in the list.

    Args:
        elements (list): A list of elements to analyze.

    Returns:
        dict: A dictionary with elements as keys and their frequency counts as values.

    Raises:
        ValueError: If the input is not a list.

    Example:
        >>> create_frequency_dict([1, 2, 2, 3, 3, 3, 4])
        {1: 1, 2: 2, 3: 3, 4: 1}
        >>> create_frequency_dict(['apple', 'banana', 'apple', 'cherry'])
        {'apple': 2, 'banana': 1, 'cherry': 1}
    """
    import logging
    from collections import defaultdict

    if not isinstance(elements, list):
        raise ValueError("Input must be a list.")

    frequency_dict = defaultdict(int)

    for element in elements:
        frequency_dict[element] += 1

    result = dict(frequency_dict)

    logging.debug(f"Elements: {elements}, Frequency dictionary: {result}")

    return result

```

### find_duplicates

```python
def find_duplicates(elements: list[int]) -> list[int]:
    """
    Identify duplicate elements in a list of integers.

    This function scans through a list of integers and returns a list of elements
    that appear more than once. The returned list contains each duplicate element
    only once, regardless of how many times it appears in the input list.

    Args:
        elements (list[int]): A list of integers to check for duplicates.

    Returns:
        list[int]: A list containing the duplicate integers found in the input list.

    Raises:
        ValueError: If the input is not a list of integers.

    Example:
        >>> find_duplicates([1, 2, 3, 2, 4, 5, 5, 6])
        [2, 5]
        >>> find_duplicates([10, 20, 30, 40])
        []
    """
    import logging
    from collections import Counter

    if not isinstance(elements, list):
        elements = [elements]
    if not all(isinstance(x, int) for x in elements):
        raise ValueError("All elements in the list must be integers.")

    logging.debug(f"Analyzing list for duplicates: {elements}")

    # Count the occurrences of each element
    element_count = Counter(elements)

    # Extract elements that appear more than once
    duplicates = [element for element, count in element_count.items() if count > 1]

    logging.debug(f"Duplicate elements found: {duplicates}")

    return duplicates
```

### find_longest_common_prefix

```python
def find_longest_common_prefix(strings: list[str]) -> str:
    """
    Find the longest common prefix among a list of strings.

    This function identifies the longest prefix that is common to all strings in the input list.
    If no common prefix exists, it returns an empty string.

    Args:
        strings (list[str]): A list of strings to evaluate.

    Returns:
        str: The longest common prefix shared by all strings in the list.

    Raises:
        ValueError: If the input is not a list of strings or if the list is empty.

    Example:
        >>> find_longest_common_prefix(["flower", "flow", "flight"])
        'fl'
        >>> find_longest_common_prefix(["dog", "racecar", "car"])
        ''
    """
    import logging

    if isinstance(strings, str):
        strings = [strings]
    elif not isinstance(strings, list):
        raise ValueError("Input must be a list of strings.")
    if not strings:
        raise ValueError("The list of strings cannot be empty.")
    if not all(isinstance(s, str) for s in strings):
        raise ValueError("All elements in the list must be strings.")

    logging.debug(f"Finding longest common prefix for strings: {strings}")

    if len(strings) == 1:
        return strings[0]

    # Sort the list to bring similar prefixes together
    strings.sort()

    # Compare the first and last strings in the sorted list
    first, last = strings[0], strings[-1]
    common_prefix = []

    for i in range(min(len(first), len(last))):
        if first[i] == last[i]:
            common_prefix.append(first[i])
        else:
            break

    result = ''.join(common_prefix)
    logging.debug(f"Longest common prefix: '{result}'")

    return result
```

### find_max_min_difference

```python
def find_max_min_difference(numbers: list[float]) -> float:
    """
    Calculate the difference between the maximum and minimum values in a list of numbers.

    Args:
        numbers (list[float]): A list of numbers to evaluate.

    Returns:
        float: The difference between the maximum and minimum numbers in the list.

    Raises:
        ValueError: If the input is not a list of numbers or if the list is empty.

    Example:
        >>> find_max_min_difference([10.0, 20.0, 30.0, 40.0])
        30.0
        >>> find_max_min_difference([5, 3, 8, 1])
        7.0
    """
    import logging

    if isinstance(numbers, (int, float)):
        numbers = [numbers]
    
    if not isinstance(numbers, list):
        raise ValueError("Input must be a list of numbers.")
    
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be numbers (int or float).")

    max_value = max(numbers)
    min_value = min(numbers)
    difference = max_value - min_value

    logging.debug(f"Max value: {max_value}, Min value: {min_value}, Difference: {difference}")

    return difference
```

### find_palindromes

```python
def find_palindromes(text: str) -> list[str]:
    """
    Identify all palindromic words in a given string.

    This function scans through the input string and returns a list of words
    that are palindromes. A palindrome is a word that reads the same backward
    as forward, ignoring case.

    Args:
        text (str): The input string to analyze.

    Returns:
        list[str]: A list containing all palindromic words found in the input string.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> find_palindromes("Anna went to see civic duty in the noon")
        ['Anna', 'civic', 'noon']
        >>> find_palindromes("Hello world")
        []
    """
    import logging
    import re

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Use regex to find words in the text
    words = re.findall(r'\b\w+\b', text)

    # Identify palindromes
    palindromes = [word for word in words if word.lower() == word[::-1].lower()]

    # Log the found palindromes
    logging.debug(f"Text: '{text}', Palindromes: {palindromes}")

    return palindromes

```

### find_unique_elements

```python
def find_unique_elements(elements: list) -> list:
    """
    Find unique elements in a list.

    Args:
        elements (list): A list of elements to evaluate.

    Returns:
        list: A list containing only the unique elements from the input list.

    Raises:
        ValueError: If the input is not a list.

    Example:
        >>> find_unique_elements([1, 2, 2, 3, 4, 4, 5])
        [1, 3, 5]
        >>> find_unique_elements(['apple', 'banana', 'apple', 'cherry'])
        ['banana', 'cherry']
    """
    import logging

    if not isinstance(elements, list):
        raise ValueError("Input must be a list.")

    # Use a dictionary to count occurrences of each element
    element_count = {}
    for element in elements:
        if element in element_count:
            element_count[element] += 1
        else:
            element_count[element] = 1

    # Extract elements that occur exactly once
    unique_elements = [element for element, count in element_count.items() if count == 1]

    # Log the result
    logging.debug(f"Unique elements found: {unique_elements}")

    return unique_elements

```

### flatten_nested_list

```python
def flatten_nested_list(nested_list: list) -> list:
    """
    Flatten a nested list into a single list of elements.

    This function takes a list that may contain nested lists and flattens it into a single list
    containing all the elements in a depth-first manner.

    Args:
        nested_list (list): A list that may contain nested lists of elements.

    Returns:
        list: A flattened list containing all elements from the nested list.

    Raises:
        ValueError: If the input is not a list.

    Example:
        >>> flatten_nested_list([1, [2, [3, 4], 5], 6])
        [1, 2, 3, 4, 5, 6]
        >>> flatten_nested_list([[1, 2], [3, 4], 5])
        [1, 2, 3, 4, 5]
    """
    import logging

    if not isinstance(nested_list, list):
        raise ValueError("Input must be a list.")

    def _flatten(lst: list) -> list:
        flat_list = []
        for item in lst:
            if isinstance(item, list):
                flat_list.extend(_flatten(item))
            else:
                flat_list.append(item)
        return flat_list

    flattened_list = _flatten(nested_list)

    logging.debug(f"Original nested list: {nested_list}, Flattened list: {flattened_list}")

    return flattened_list

```

### insertion_sort

```python
def insertion_sort(arr: list[int]) -> list[int]:
    """
    Sort a list of integers using the insertion sort algorithm.

    Insertion sort is a simple sorting algorithm that builds the final sorted array one item at a time.
    It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.

    Args:
        arr (list[int]): A list of integers to be sorted.

    Returns:
        list[int]: A new list containing the sorted integers.

    Raises:
        ValueError: If the input is not a list of integers.

    Example:
        >>> insertion_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> insertion_sort([5, 3, 8, 4, 2])
        [2, 3, 4, 5, 8]
    """
    import logging

    if isinstance(arr, int):
        arr = [arr]
    elif not isinstance(arr, list):
        raise ValueError("Input must be a list of integers.")
    if not all(isinstance(x, int) for x in arr):
        raise ValueError("All elements in the list must be integers.")

    logging.debug(f"Initial array: {arr}")

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        logging.debug(f"Array after inserting element {key}: {arr}")

    logging.debug(f"Sorted array: {arr}")

    return arr

```

### merge_sort

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Sort a list of integers using the merge sort algorithm.

    Merge sort is a divide-and-conquer algorithm that splits the list into halves,
    recursively sorts each half, and then merges the sorted halves back together.

    Args:
        arr (list[int]): A list of integers to be sorted.

    Returns:
        list[int]: A new list containing the sorted integers.

    Raises:
        ValueError: If the input is not a list of integers.

    Example:
        >>> merge_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> merge_sort([5, 3, 8, 4, 2])
        [2, 3, 4, 5, 8]
    """
    import logging

    if isinstance(arr, int):
        arr = [arr]
    elif not isinstance(arr, list):
        raise ValueError("Input must be a list of integers.")
    if not all(isinstance(x, int) for x in arr):
        raise ValueError("All elements in the list must be integers.")

    logging.debug(f"Initial array: {arr}")

    def _merge(left: list[int], right: list[int]) -> list[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _merge_sort(lst: list[int]) -> list[int]:
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = _merge_sort(lst[:mid])
        right = _merge_sort(lst[mid:])
        return _merge(left, right)

    sorted_arr = _merge_sort(arr)
    logging.debug(f"Sorted array: {sorted_arr}")

    return sorted_arr

```

### merge_sorted_lists

```python
def merge_sorted_lists(list1: list[int], list2: list[int]) -> list[int]:
    """
    Merge two sorted lists into a single sorted list.

    Args:
        list1 (list[int]): The first sorted list of integers.
        list2 (list[int]): The second sorted list of integers.

    Returns:
        list[int]: A new list containing all elements from both input lists, sorted in ascending order.

    Raises:
        ValueError: If either input is not a list of integers or if the lists are not sorted.

    Example:
        >>> merge_sorted_lists([1, 3, 5], [2, 4, 6])
        [1, 2, 3, 4, 5, 6]
        >>> merge_sorted_lists([1, 2, 3], [])
        [1, 2, 3]
    """
    import logging

    # Convert single integers to lists
    if isinstance(list1, int):
        list1 = [list1]
    if isinstance(list2, int):
        list2 = [list2]

    if not isinstance(list1, list) or not isinstance(list2, list):
        raise ValueError("Both inputs must be lists of integers.")
    if not all(isinstance(x, int) for x in list1) or not all(isinstance(x, int) for x in list2):
        raise ValueError("All elements in both lists must be integers.")
    if list1 != sorted(list1) or list2 != sorted(list2):
        raise ValueError("Both lists must be sorted in ascending order.")

    logging.debug(f"Merging lists: {list1} and {list2}")

    merged_list = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1

    # Append remaining elements
    merged_list.extend(list1[i:])
    merged_list.extend(list2[j:])

    logging.debug(f"Merged list: {merged_list}")

    return merged_list
```

### optimize_list_order

```python
def optimize_list_order(numbers: list[int]) -> list[int]:
    """
    Optimize the order of a list of integers by sorting them in ascending order
    and removing duplicates.

    This function sorts a list of integers in ascending order and removes any duplicate values,
    ensuring that each number appears only once in the resulting list.

    Args:
        numbers (list[int]): A list of integers to be optimized.

    Returns:
        list[int]: A new list containing the sorted integers with duplicates removed.

    Raises:
        ValueError: If the input is not a list of integers.

    Example:
        >>> optimize_list_order([4, 2, 5, 2, 3, 1, 4])
        [1, 2, 3, 4, 5]
        >>> optimize_list_order([10, 9, 8, 8, 7])
        [7, 8, 9, 10]
    """
    import logging

    if isinstance(numbers, int):
        numbers = [numbers]
    elif not isinstance(numbers, list):
        raise ValueError("Input must be a list of integers or a single integer.")
    if not all(isinstance(num, int) for num in numbers):
        raise ValueError("All elements in the list must be integers.")

    # Remove duplicates by converting to a set, then sort the result
    optimized_list = sorted(set(numbers))

    logging.debug(f"Original list: {numbers}, Optimized list: {optimized_list}")

    return optimized_list
```

### quicksort

```python
def quicksort(arr: list[int]) -> list[int]:
    """
    Sort a list of integers using the quicksort algorithm.

    Args:
        arr (list[int]): A list of integers to be sorted.

    Returns:
        list[int]: A new list containing the sorted integers.

    Raises:
        ValueError: If the input is not a list of integers.

    Example:
        >>> quicksort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> quicksort([5, 3, 8, 4, 2])
        [2, 3, 4, 5, 8]
    """
    import logging

    if isinstance(arr, int):
        arr = [arr]
    elif not isinstance(arr, list):
        raise ValueError("Input must be a list of integers.")
    if not all(isinstance(x, int) for x in arr):
        raise ValueError("All elements in the list must be integers.")

    logging.debug(f"Initial array: {arr}")

    def _quicksort(lst: list[int]) -> list[int]:
        if len(lst) <= 1:
            return lst
        pivot = lst[len(lst) // 2]
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
        logging.debug(f"Pivot: {pivot}, Left: {left}, Middle: {middle}, Right: {right}")
        return _quicksort(left) + middle + _quicksort(right)

    sorted_arr = _quicksort(arr)
    logging.debug(f"Sorted array: {sorted_arr}")

    return sorted_arr
```

## Utility Tools

### convert_to_binary

```python
def convert_to_binary(number: int) -> str:
    """
    Convert an integer to its binary representation.

    This function takes an integer and converts it to a binary string prefixed with '0b'.
    It handles both positive and negative integers.

    Args:
        number (int): The integer to convert to binary.

    Returns:
        str: The binary representation of the integer.

    Raises:
        ValueError: If the input is not an integer.

    Example:
        >>> convert_to_binary(10)
        '0b1010'
        >>> convert_to_binary(-5)
        '-0b101'
    """
    import logging

    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")

    binary_representation = bin(number)

    logging.debug(f"Converted integer {number} to binary: {binary_representation}")

    return binary_representation

```

### convert_to_camel_case

```python
def convert_to_camel_case(text: str) -> str:
    """
    Convert a given string to camelCase format.

    This function transforms a string into camelCase, where the first word is in lowercase
    and subsequent words are capitalized without spaces or underscores.

    Args:
        text (str): The input string to convert.

    Returns:
        str: A new string in camelCase format.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> convert_to_camel_case("hello world")
        'helloWorld'
        >>> convert_to_camel_case("python programming language")
        'pythonProgrammingLanguage'
    """
    import re
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Remove any non-alphanumeric characters and split the text into words
    words = re.sub(r'[^a-zA-Z0-9\s]', '', text).split()

    # Convert the first word to lowercase and capitalize the rest
    if not words:
        return ''
    
    camel_case_text = words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    # Log the transformation
    logging.debug(f"Original text: '{text}', CamelCase text: '{camel_case_text}'")

    return camel_case_text

```

### convert_to_hex

```python
def convert_to_hex(number: int) -> str:
    """
    Convert an integer to its hexadecimal representation.

    This function takes an integer and converts it to a hexadecimal string prefixed with '0x'.
    It handles both positive and negative integers.

    Args:
        number (int): The integer to convert to hexadecimal.

    Returns:
        str: The hexadecimal representation of the integer.

    Raises:
        ValueError: If the input is not an integer.

    Example:
        >>> convert_to_hex(255)
        '0xff'
        >>> convert_to_hex(-42)
        '-0x2a'
    """
    import logging

    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")

    hex_representation = hex(number)

    logging.debug(f"Converted integer {number} to hexadecimal: {hex_representation}")

    return hex_representation

```

### convert_to_kebab_case

```python
def convert_to_kebab_case(text: str) -> str:
    """
    Convert a given string to kebab-case format.

    This function transforms a string into kebab-case, where words are
    separated by hyphens and all letters are in lowercase.

    Args:
        text (str): The input string to convert.

    Returns:
        str: A new string in kebab-case format.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> convert_to_kebab_case("Hello World")
        'hello-world'
        >>> convert_to_kebab_case("PythonProgramming")
        'python-programming'
    """
    import re
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)

    # Convert camelCase or PascalCase to kebab-case
    text = re.sub(r'(?<!^)(?=[A-Z])', '-', text).lower()

    # Log the transformation
    logging.debug(f"Original text: '{text}', Kebab-case text: '{text}'")

    return text

```

### convert_to_snake_case

```python
def convert_to_snake_case(text: str) -> str:
    """
    Convert a given string to snake_case format.

    This function transforms a string into snake_case, where words are
    separated by underscores and all letters are in lowercase.

    Args:
        text (str): The input string to convert.

    Returns:
        str: A new string in snake_case format.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> convert_to_snake_case("Hello World")
        'hello_world'
        >>> convert_to_snake_case("PythonProgramming")
        'python_programming'
    """
    import re
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Replace spaces and hyphens with underscores
    text = re.sub(r'[\s-]+', '_', text)

    # Convert camelCase or PascalCase to snake_case
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

    # Log the transformation
    logging.debug(f"Original text: '{text}', Snake_case text: '{text}'")

    return text

```

### format_as_sentence_case

```python
def format_as_sentence_case(text: str) -> str:
    """
    Convert a given string to sentence case, capitalizing the first letter of the first word
    and ensuring the rest of the sentence is in lowercase.

    Args:
        text (str): The input string to be formatted.

    Returns:
        str: A new string with the first letter of the first word capitalized and the rest in lowercase.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> format_as_sentence_case("hello world. THIS IS a TEST.")
        'Hello world. this is a test.'
        >>> format_as_sentence_case("PYTHON programming.")
        'Python programming.'
    """
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Split the text into sentences
    sentences = text.split('. ')
    formatted_sentences = []

    for sentence in sentences:
        if sentence:
            # Capitalize the first letter of the sentence and make the rest lowercase
            formatted_sentence = sentence[0].upper() + sentence[1:].lower()
            formatted_sentences.append(formatted_sentence)

    # Join the sentences back together
    sentence_cased_text = '. '.join(formatted_sentences)

    # Log the transformation
    logging.debug(f"Original text: '{text}', Sentence-cased text: '{sentence_cased_text}'")

    return sentence_cased_text

```

### format_as_title_case

```python
def format_as_title_case(text: str) -> str:
    """
    Convert a given string to title case, capitalizing the first letter of each word
    while ensuring the rest of the letters are in lowercase.

    Args:
        text (str): The input string to be formatted.

    Returns:
        str: A new string with each word's first letter capitalized and the rest in lowercase.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> format_as_title_case("hello world")
        'Hello World'
        >>> format_as_title_case("PYTHON programming")
        'Python Programming'
    """
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Convert the text to title case
    title_cased_text = text.title()

    # Log the transformation
    logging.debug(f"Original text: '{text}', Title-cased text: '{title_cased_text}'")

    return title_cased_text

```

### validate_email_format

```python
import re
import logging

def validate_email_format(email: str) -> bool:
    """
    Validate the format of an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> validate_email_format("example@example.com")
        True
        >>> validate_email_format("invalid-email")
        False
    """
    if not isinstance(email, str):
        raise ValueError("The email must be a string.")

    # Define a regular expression for validating an Email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the regex pattern
    is_valid = re.match(email_regex, email) is not None

    # Log the result
    logging.debug(f"Email validation for '{email}': {is_valid}")

    return is_valid

```

### validate_url_format

```python
def validate_url_format(url: str) -> bool:
    """
    Validate the format of a URL.

    This function checks if the URL follows a standard format, including the scheme (http, https),
    domain, and optional path, query, and fragment components.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL format is valid, False otherwise.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> validate_url_format("https://www.example.com")
        True
        >>> validate_url_format("ftp://example.com")
        False
    """
    import re
    import logging

    if not isinstance(url, str):
        raise ValueError("The URL must be a string.")

    # Define a regular expression for validating URLs
    url_regex = (
        r'^(https?://)'  # http:// or https://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # Domain name
        r'(:\d+)?'  # Optional port
        r'(/[-A-Za-z0-9@:%._\+~#=]*)*'  # Path
        r'(\?[;&A-Za-z0-9%_.~+=-]*)?'  # Query
        r'(#[-A-Za-z0-9_]*)?$'  # Fragment
    )

    # Check if the URL matches the regex pattern
    is_valid = re.match(url_regex, url) is not None

    # Log the result
    logging.debug(f"URL validation for '{url}': {is_valid}")

    return is_valid

```

## Other Tools

### binary_search

```python
def binary_search(sorted_list: list[int], target: int) -> int:
    """
    Perform a binary search on a sorted list to find the index of a target value.

    Args:
        sorted_list (list[int]): A list of integers sorted in ascending order.
        target (int): The integer value to search for in the list.

    Returns:
        int: The index of the target value in the list if found, otherwise -1.

    Raises:
        ValueError: If the input list is not sorted or if the inputs are not of the correct type.

    Example:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
        >>> binary_search([10, 20, 30, 40, 50], 25)
        -1
    """
    import logging

    if not isinstance(sorted_list, list):
        sorted_list = [sorted_list]
    if not all(isinstance(x, int) for x in sorted_list):
        raise ValueError("The sorted_list must be a list of integers.")
    if not isinstance(target, int):
        raise ValueError("The target must be an integer.")
    if sorted_list != sorted(sorted_list):
        raise ValueError("The list must be sorted in ascending order.")

    left, right = 0, len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = sorted_list[mid]

        logging.debug(f"Searching: left={left}, right={right}, mid={mid}, mid_value={mid_value}")

        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### count_sentences

```python
def count_sentences(text: str) -> int:
    """
    Count the number of sentences in a given string.

    This function analyzes the input string and counts the number of sentences based on the presence
    of sentence-ending punctuation marks such as '.', '!', and '?'.

    Args:
        text (str): The input string to analyze.

    Returns:
        int: The number of sentences in the input string.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> count_sentences("Hello world! How are you? I'm fine.")
        3
        >>> count_sentences("This is a single sentence.")
        1
    """
    import logging
    import re

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Use regex to find sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)

    # Filter out any empty strings resulting from split
    sentence_count = len([s for s in sentences if s.strip()])

    # Log the sentence count
    logging.debug(f"Text: '{text}', Sentence count: {sentence_count}")

    return sentence_count

```

### count_vowels_consonants

```python
def count_vowels_consonants(text: str) -> dict[str, int]:
    """
    Count the number of vowels and consonants in a given string.

    This function calculates the number of vowels and consonants in the input string,
    ignoring any non-alphabetic characters.

    Args:
        text (str): The input string to analyze.

    Returns:
        dict[str, int]: A dictionary with keys 'vowels' and 'consonants' representing
                        the count of vowels and consonants, respectively.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> count_vowels_consonants("Hello World!")
        {'vowels': 3, 'consonants': 7}
        >>> count_vowels_consonants("Python 3.8")
        {'vowels': 1, 'consonants': 5}
    """
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    vowels = set("aeiouAEIOU")
    consonants = set("bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ")

    vowel_count = sum(1 for char in text if char in vowels)
    consonant_count = sum(1 for char in text if char in consonants)

    result = {'vowels': vowel_count, 'consonants': consonant_count}

    logging.debug(f"Text: '{text}', Vowels: {vowel_count}, Consonants: {consonant_count}")

    return result

```

### debug_variable_types

```python
def debug_variable_types(variables: dict[str, any]) -> dict[str, str]:
    """
    Debug and return the types of given variables.

    Args:
        variables (dict[str, any]): A dictionary where keys are variable names and values are the variables themselves.

    Returns:
        dict[str, str]: A dictionary with variable names as keys and their types as values.

    Raises:
        ValueError: If the input is not a dictionary or if any key is not a string.

    Example:
        >>> debug_variable_types({'var1': 123, 'var2': 'hello', 'var3': [1, 2, 3]})
        {'var1': 'int', 'var2': 'str', 'var3': 'list'}
    """
    import logging

    if not isinstance(variables, dict):
        if isinstance(variables, (str, int, float, list, tuple, set)):
            variables = {'value': variables}
        else:
            raise ValueError("Input must be a dictionary with variable names as keys.")

    for key in variables:
        if not isinstance(key, str):
            raise ValueError("All keys in the dictionary must be strings representing variable names.")

    types_dict = {var_name: type(var_value).__name__ for var_name, var_value in variables.items()}

    logging.debug(f"Variable types: {types_dict}")

    return types_dict
```

### group_anagrams

```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    """
    Group a list of words into anagrams.

    This function takes a list of words and groups them into lists of anagrams.
    An anagram is a word formed by rearranging the letters of another word.

    Args:
        words (list[str]): A list of words to group into anagrams.

    Returns:
        list[list[str]]: A list of lists, where each sublist contains words that are anagrams of each other.

    Raises:
        ValueError: If the input is not a list of strings.

    Example:
        >>> group_anagrams(["listen", "silent", "enlist", "rat", "tar", "art"])
        [['listen', 'silent', 'enlist'], ['rat', 'tar', 'art']]
        >>> group_anagrams(["hello", "world"])
        [['hello'], ['world']]
    """
    import logging
    from collections import defaultdict

    if not isinstance(words, list):
        words = [words]
    if not all(isinstance(word, str) for word in words):
        raise ValueError("All elements in the list must be strings.")

    logging.debug(f"Grouping anagrams from the list: {words}")

    anagrams = defaultdict(list)
    for word in words:
        # Sort the word to create a key
        sorted_word = ''.join(sorted(word))
        anagrams[sorted_word].append(word)

    grouped_anagrams = list(anagrams.values())

    logging.debug(f"Grouped anagrams: {grouped_anagrams}")

    return grouped_anagrams
```

### jump_search

```python
def jump_search(sorted_list: list[int], target: int) -> int:
    """
    Perform a jump search on a sorted list to find the index of a target value.

    Jump search is an algorithm that searches for a target value in a sorted list by jumping ahead
    by a fixed number of steps (block size) and then performing a linear search within the block.

    Args:
        sorted_list (list[int]): A list of integers sorted in ascending order.
        target (int): The integer value to search for in the list.

    Returns:
        int: The index of the target value in the list if found, otherwise -1.

    Raises:
        ValueError: If the input list is not sorted or if the inputs are not of the correct type.

    Example:
        >>> jump_search([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7)
        6
        >>> jump_search([10, 20, 30, 40, 50], 25)
        -1
    """
    import math
    import logging

    if not isinstance(sorted_list, list):
        sorted_list = [sorted_list]
    if not all(isinstance(x, int) for x in sorted_list):
        raise ValueError("The sorted_list must be a list of integers.")
    if not isinstance(target, int):
        raise ValueError("The target must be an integer.")
    if sorted_list != sorted(sorted_list):
        raise ValueError("The list must be sorted in ascending order.")

    n = len(sorted_list)
    step = int(math.sqrt(n))
    prev = 0

    logging.debug(f"Starting jump search for target {target} in list: {sorted_list}")

    while prev < n and sorted_list[min(step, n) - 1] < target:
        logging.debug(f"Jumping from index {prev} to {min(step, n) - 1}")
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            logging.debug(f"Target {target} not found in the list")
            return -1

    logging.debug(f"Performing linear search in block starting at index {prev}")

    for idx in range(prev, min(step, n)):
        logging.debug(f"Checking index {idx}: value {sorted_list[idx]}")
        if sorted_list[idx] == target:
            logging.debug(f"Target {target} found at index {idx}")
            return idx

    logging.debug(f"Target {target} not found in the list")
    return -1

```

### linear_search

```python
def linear_search(elements: list[int], target: int) -> int:
    """
    Perform a linear search on a list to find the index of a target value.

    This function iterates through the list to find the first occurrence of the target value.
    It returns the index of the target if found, otherwise returns -1.

    Args:
        elements (list[int]): A list of integers to search through.
        target (int): The integer value to search for in the list.

    Returns:
        int: The index of the target value in the list if found, otherwise -1.

    Raises:
        ValueError: If the input list is not a list of integers or if the target is not an integer.

    Example:
        >>> linear_search([10, 20, 30, 40, 50], 30)
        2
        >>> linear_search([5, 3, 8, 1], 7)
        -1
    """
    import logging

    if not isinstance(elements, list):
        elements = [elements]
    if not all(isinstance(x, int) for x in elements):
        raise ValueError("All elements in the list must be integers.")
    if not isinstance(target, int):
        raise ValueError("The target must be an integer.")

    logging.debug(f"Starting linear search for target {target} in list: {elements}")

    for index, value in enumerate(elements):
        logging.debug(f"Checking index {index}: value {value}")
        if value == target:
            logging.debug(f"Target {target} found at index {index}")
            return index

    logging.debug(f"Target {target} not found in the list")
    return -1
```

### remove_punctuation

```python
def remove_punctuation(text: str) -> str:
    """
    Remove all punctuation from a given string.

    Args:
        text (str): The input string from which to remove punctuation.

    Returns:
        str: A new string with all punctuation characters removed.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> remove_punctuation("Hello, world!")
        'Hello world'
        >>> remove_punctuation("Python's great, isn't it?")
        'Pythons great isnt it'
    """
    import string
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Create a translation table that maps punctuation to None
    translator = str.maketrans('', '', string.punctuation)

    # Remove punctuation using the translation table
    cleaned_text = text.translate(translator)

    # Log the cleaned text
    logging.debug(f"Original text: '{text}', Cleaned text: '{cleaned_text}'")

    return cleaned_text

```

### remove_whitespace

```python
def remove_whitespace(text: str) -> str:
    """
    Remove all whitespace characters from a given string.

    Args:
        text (str): The input string from which to remove whitespace.

    Returns:
        str: A new string with all whitespace characters removed.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> remove_whitespace("Hello, world!")
        'Hello,world!'
        >>> remove_whitespace(" Python  programming ")
        'Pythonprogramming'
    """
    import logging

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Remove all whitespace characters
    cleaned_text = ''.join(text.split())

    # Log the cleaned text
    logging.debug(f"Original text: '{text}', Cleaned text: '{cleaned_text}'")

    return cleaned_text

```

### sentiment_analysis

```python
def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of a given text and determine if it is positive, negative, or neutral.

    Args:
        text (str): The input string containing the text to analyze for sentiment.

    Returns:
        str: The sentiment classification of the text, which can be 'positive', 'negative', or 'neutral'.

    Raises:
        ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Step 2: Preprocess the text
    text = text.lower()
    text = remove_punctuation(text)
    
    # Step 3: Tokenize the text
    tokens = text.split()

    # Step 4: Assign sentiment scores
    sentiment_score = 0
    for token in tokens:
        # Example sentiment lexicon (simplified)
        if token in ['good', 'happy', 'joyful']:
            sentiment_score += 1
        elif token in ['bad', 'sad', 'terrible']:
            sentiment_score -= 1

    # Step 5: Aggregate sentiment scores
    if sentiment_score > 0:
        return 'positive'
    elif sentiment_score < 0:
        return 'negative'
    else:
        return 'neutral'

```

### transform_to_pig_latin

```python
def transform_to_pig_latin(text: str) -> str:
    """
    Transform a given string into Pig Latin.

    Pig Latin is a language game where words in English are altered according to a simple set of rules:
    - For words that begin with a consonant, all letters before the initial vowel are placed at the end of the word sequence.
      Then, "ay" is added.
    - For words that begin with a vowel, "way" is added to the end of the word.

    Args:
        text (str): The input string to transform into Pig Latin.

    Returns:
        str: A new string with each word transformed into Pig Latin.

    Raises:
        ValueError: If the input is not a string.

    Example:
        >>> transform_to_pig_latin("hello world")
        'ellohay orldway'
        >>> transform_to_pig_latin("apple")
        'appleway'
    """
    import logging
    import re

    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    def pig_latin_word(word: str) -> str:
        vowels = "aeiouAEIOU"
        if word[0] in vowels:
            return word + "way"
        else:
            match = re.search(r"[aeiouAEIOU]", word)
            if match:
                index = match.start()
                return word[index:] + word[:index] + "ay"
            else:
                return word + "ay"

    words = text.split()
    pig_latin_words = [pig_latin_word(word) for word in words]
    pig_latin_text = ' '.join(pig_latin_words)

    logging.debug(f"Original text: '{text}', Pig Latin text: '{pig_latin_text}'")

    return pig_latin_text

```

