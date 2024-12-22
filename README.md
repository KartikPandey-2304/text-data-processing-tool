# text-data-processing-tool
# Project Title: Sentence Filtering and Tokenization

## Overview
This project contains Python script for processing a dataset of sentences in CSV files. The  script extracts unique words from the sentences, and filters sentences based on a list of target words. The results are saved in separate CSV files.

## Features
- Tokenization of sentences and extraction of unique words.
- Filtering sentences that contain specific target words.
- Saving the filtered data and remaining sentences to CSV files.

## Prerequisites
- Python 3.x
- The following Python libraries:
  - `nltk`
  - `csv`
  - `re`
  - `tqdm`

Install the necessary libraries using `pip`:
```bash
pip install nltk tqdm
