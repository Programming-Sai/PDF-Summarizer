# PDF-Summarizer

Summarise a given pdf to possibly extract only highlighted text and images

## Pipeline

1. will first extract Text, headings, images and then Highlighted texts.
2. Then would piece each section to the right position by running the highlighted text, and headings through the main extracted text and looking for a match.
3. if one or multiple is found the sentence or paragraph is set aside for further processing
