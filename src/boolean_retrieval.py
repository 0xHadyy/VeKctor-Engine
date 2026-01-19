# retrevie the terms in the inverted index and intersect the postings
# using get_posting


class booleanRetrieval:
    def __init__(self, inverted_index):
        self.operators = ["AND", "OR", "NOT"]
        self.inverted_index = inverted_index

    def boolean_search(self, query):
        # returns ["deep","and","learning"
        query = query.split()
        operator = None
        postings = set()
        result = None

        for token in query:
            if token in self.operators:
                operator = token
                print(f"this is token operator : {operator}")
            else:
                # get the postings for the token
                token = token.lower()
                postings = set(self.inverted_index.get_posting_list(token))

                print(f"for {token} -> postings :{postings}\n")

            if result is None:
                result = postings
            if operator == "AND":
                result = result & postings
            if operator == "OR":
                result = result | postings
            if operator == "NOT":
                result = result - postings
            print(f"the result is {result}")
        return result
