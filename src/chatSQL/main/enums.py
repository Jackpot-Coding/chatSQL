from enum import Enum

# genereate the enums for the error in the generation of the prompt

class PromptGenStatus(Enum):
    SUCCESS = 0
    DATABASE_NOT_FOUND = -1
    SENTENCE_UNINTERPRETABLE = -2
    SENTENCE_IRRELEVANT = -3