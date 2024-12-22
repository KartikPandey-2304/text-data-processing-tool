import nltk
import csv
import re
from tqdm import tqdm

# Download necessary NLTK data
nltk.download('punkt')

def load_csv_file(file_path: str):
    """
    Loads data from a CSV file and returns it as a list of rows.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of rows from the CSV file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [row for row in reader if row]  # Filter out empty rows
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except IndexError:
        print(f"Error: {file_path} is empty or not properly formatted.")
    return []

def extract_unique_words_from_csv(input_file: str, output_file: str):
    """
    Extracts unique words from sentences in a CSV file and saves them to another CSV file.

    Args:
        input_file (str): Path to the input CSV file containing sentences.
        output_file (str): Path to the output CSV file where unique words will be saved.
    """
    unique_words = set()

    # Read the dataset and tokenize sentences
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            sentence = row[0]  # Assuming sentences are in the first column
            words = nltk.word_tokenize(sentence)
            unique_words.update(words)  # Add the words to the set

    # Sort the unique words alphabetically
    sorted_words = sorted(unique_words)

    # Save the unique words to an output file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word in sorted_words:
            writer.writerow([word])

    print(f"Unique words saved to {output_file}")

def filter_sentences_by_target_words(target_file: str, sentence_file: str, output_filtered_file: str, output_remaining_file: str):
    """
    Filters sentences in a CSV based on target words, and saves the filtered and remaining data.

    Args:
        target_file (str): Path to the CSV file containing target words.
        sentence_file (str): Path to the CSV file containing sentences to filter.
        output_filtered_file (str): Path to save the filtered data.
        output_remaining_file (str): Path to save the remaining data.
    """
    target_words = load_csv_file(target_file)
    if not target_words:
        return

    sentences_data = load_csv_file(sentence_file)
    if not sentences_data:
        return

    filtered_data = []
    sentences_to_remove = []

    for i, row in enumerate(tqdm(sentences_data, desc="Processing Sentences")):
        sentence = row[0]  # Assuming sentence is in the first column
        for target_word in target_words:
            if re.search(r'\b{}\b'.format(target_word), sentence.lower()):
                filtered_data.append(row)
                sentences_to_remove.append(i)
                break  # Exit once a match is found

    if filtered_data:
        # Save filtered data
        with open(output_filtered_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(filtered_data)
        print(f"Filtered data saved in {output_filtered_file}.")

        # Save remaining data
        with open(output_remaining_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i, row in enumerate(sentences_data):
                if i not in sentences_to_remove:
                    writer.writerow(row)
        print(f"Remaining data saved in {output_remaining_file}.")
    else:
        print("No data found matching the criteria.")

    # Save the original dataset
    with open(sentence_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(sentences_data)
    print(f"Original dataset saved in {sentence_file}.")

if __name__ == "__main__":
    # File paths
    input_sentence_file = 'sentences_data.csv'
    target_file = 'target_words.csv'
    output_unique_words_file = 'unique_words.csv'
    output_filtered_file = 'filtered_sentences.csv'
    output_remaining_file = 'remaining_sentences.csv'

    # Extract and save unique words from the dataset
    extract_unique_words_from_csv(input_sentence_file, output_unique_words_file)

    # Filter sentences based on target words and save the results
    filter_sentences_by_target_words(target_file, input_sentence_file, output_filtered_file, output_remaining_file)
