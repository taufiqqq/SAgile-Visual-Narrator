import spacy
from spacy.matcher import Matcher

class Parser:
    def __init__(self, US) -> None:
        self.US = US
        self.US_Parsed = None
        self.indicator_Role = [
            [{"LOWER": "as"}, {"LOWER": "an"}],
            [{"LOWER": "as"}, {"LOWER": "a"}],
        ]
        self.indicator_Means = [
            [{"LOWER": "i"}, {"LOWER": "am"}, {"LOWER": "able"}, {"LOWER": "to"}],
            [{"LOWER": "i"}, {"LOWER": "can"}],
            [{"LOWER": "i"}, {"LOWER": "want"}, {"LOWER": "to"}],
            [{"LOWER": "i"}, {"LOWER": "want"}],
        ]
        self.indicator_Ends = [
            [{"LOWER": "so"}, {"LOWER": "that"}, {"LOWER": "i"}, {"LOWER": "can"}]
        ]

    def start_parse(self) -> None:
        # load language model and create a matcher
        nlp = spacy.load('en_core_web_sm')
        matcher = Matcher(nlp.vocab)

        # add patterns to detect role means ends
        matcher.add("ROLE", self.indicator_Role)
        matcher.add("MEANS", self.indicator_Means)
        matcher.add("ENDS", self.indicator_Ends)
        
        userStories = []
        # for each user story, split into role, means, ends
        for line in self.US:
            currStory = line.strip()
            doc = nlp(currStory)

            role_start, role_end = None, None
            means_start, means_end = None, None
            ends_start = None

            # find matches
            matches = matcher(doc)
            # for each matches, check what is matched (role, means, or ends)
            # the pattern for the matches can be set in indicator.py
            # when matched, set the end index as the start of that part of the user story
            for match_id, start, end in matches:
                if doc[start:end][0].text.lower() == "as" and role_start is None: # matched role
                    # set role starting index
                    role_start, role_end = end, None
                elif doc[start:end][0].text.lower() == "i" and means_start is None: # matched means
                    # set means starting index
                    means_start, means_end = end, None
                    # set role ending index
                    role_end = start
                elif doc[start:end][0].text.lower() == "so" and ends_start is None: # matched ends
                    # set ends starting index
                    ends_start = end
                    # set means ending index
                    means_end = start
                
            # error prevention
            # if some indexes are still None after above loop, set the parts as empty string
            if role_start is not None and role_end is not None:
                role = doc[role_start:role_end].text.strip(',.')
            else:
                role = ''
                
            if means_start is not None and means_end is not None: 
                means = doc[means_start:means_end].text.strip(',.')
            elif means_start is not None and means_end is None: # if no ends is found
                means = doc[means_start:].text.strip(',.')
            else:
                means = ''
                
            if ends_start is not None:
                ends = doc[ends_start:].text.strip(',.')
            else:
                ends = ''
            
            # append the split user story to a list
            userStories.append({
                'role': role,
                'means': means,
                'ends': ends
            })
        
        self.US_Parsed = userStories
        
    def get_parsed(self) -> list:
        return self.US_Parsed
            