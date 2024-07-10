Code is divided into different folders
1. DataCleaning
    - First we extract the text from reports (findings + impressions)
    - To check grammar and correct the spellings we create the dictionary of words from corpus.text
    - Then we correct the dictionary mannualyy, since dictionary is created from corpus and it contains spelling mistakes or writting mistakes
    - We use simspell library to correct the errors in writiing
2. AutoKGConstruction
    - To extract the triples we are using radiology dictionary that we have created using RadLex lexicon and keywords from corpus
    - We use rule-based approach to extract the triples, dictionary matching based, pattern based and supersense tagging based approch.
3. InformationExtraction
    - Information Extraction module is similar as defined in AutoKGConstruction
    - This model is used in tool where radiologists gives input and we want to extract the keywords.
