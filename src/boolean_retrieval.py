# retrevie the terms in the inverted index and intersect the postings
# using get_posting

from nltk import pos_tag, re_show
from src.tokenizer import Tokenizer


class booleanRetrieval:
    def __init__(self, inverted_index):
        self.tokenizer = Tokenizer()
        self.inverted_index = inverted_index
        self.operators = ["AND", "OR"]

    def _intersection(self, list1, list2) -> list:
        i = 0
        j = 0
        result = []

        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                result.append(list1[i])
                i += 1
                j += 1
            elif list1[i] < list2[j]:
                i += 1
            else:
                j += 1

        return result

    def _union(self, list1, list2) -> list:
        i = j = 0
        result = []

        while i < len(list1) and j < len(list2):
            if list1[i] == list2[j]:
                result.append(list1[i])
                i += 1
                j += 1
            elif list1[i] < list2[j]:
                result.append(list1[i])
                i += 1
            elif list1[i] > list2[j]:
                result.append(list2[j])
                j += 1

        result.extend(list1[i:])
        result.extend(list2[j:])

        return result

    def _NOT(self, list1) -> list:
        docIDs = self.inverted_index.get_docIDs()
        i = 0
        j = 0
        result = []
        print(f"the length of docsID is {len(docIDs)}")
        print(f"the length of list is {len(list1)}")
        while i < len(list1) and j < len(docIDs):
            if list1[i] == docIDs[j]:
                i += 1
                j += 1
            elif list1[i] < docIDs[j]:
                i += 1
            elif list1[i] > docIDs[j]:
                result.append(docIDs[j])
                j += 1

        result.extend(docIDs[j:])

        return result

    def boolean_search(self, query):
        # returns ["deep","and","learning"
        query = query.split()
        operator = None
        negation = False
        postings = []
        result = None

        for token in query:
            if token in self.operators:
                operator = token
                print(f"this is operator is  {operator}")
                continue
            else:
                if token == "NOT":
                    negation = True
                    continue
                token = token.lower()
                postings = list(self.inverted_index.get_posting_list(token))
                print(f"for {token}-> postings :{postings}")

            if result is None:
                result = postings
            else:
                if negation:
                    print("###################### NOT  ###########################\n")
                    print(f"the result is : {postings}\n")
                    postings = self._NOT(postings)
                    print(f"the result after  is : {postings}\n")
                    print(
                        "###################### END-NOT  ###########################\n"
                    )
                    negation = False
                if operator == "AND":
                    print("###################### AND  ###########################\n")
                    print(f"the result is : {result}\n")
                    result = self._intersection(result, postings)

                    print(f"the result after  is : {result}\n")
                    operator = None
                    print(
                        "###################### END-AND  ###########################\n"
                    )

                if operator == "OR":
                    print(f"the result is : {result}")
                    result = self._union(result, postings)
                    print(f"the result after  is : {result}")

                    operator = None

        return result
