import json

CSV_SEPARATOR = ','


def csv_to_lists(csv_file_path):
    return open(csv_file_path, 'r').read().split('\n')


class UseIndex(object):
    # process the data mapping files and store data in 3 separate dicts as instance variables
    #   - term_dict
    #   - doc_id_dict
    #   - inverted_index
    def __init__(self, term_id_path, doc_id_path, inverted_index_path):
        self.term_dict = {}  # term => [term_id, freq_in_docs]
        self.doc_id_dict = {}  # doc_id => [doc_name, num_of_terms]
        term_rows = csv_to_lists(term_id_path)
        doc_rows = csv_to_lists(doc_id_path)

        for i, term_row in enumerate(term_rows):
            if i == 0:
                continue
            term_id, term, freq = term_row.split(CSV_SEPARATOR)
            self.term_dict[term] = [term_id, freq]

        for i, doc_row in enumerate(doc_rows):
            if i == 0:
                continue
            doc_id, doc_name, num_terms = doc_row.split(CSV_SEPARATOR)
            self.doc_id_dict[doc_id] = [doc_name, num_terms]

        with open(inverted_index_path, 'r') as file_inverted_index:
            self.inverted_index = json.load(file_inverted_index)

    # given a term, returns its corresponding term id
    def get_term_id(self, term):
        term = term.lower()
        return self.term_dict[term][0] if term in self.term_dict else None

    # given a term id, returns its entry in the inverted list
    def get_term_inverted_list(self, term_id):
        return self.inverted_index[term_id]

    # given a term, returns a list of doc_ids containing that term
    def get_doc_ids_containing_term(self, term):
        term = term.lower()
        term_id = self.get_term_id(term)
        if not term_id:
            return []
        doc_occurrences = self.get_term_inverted_list(term_id)
        return [str(occurrence[0]) for occurrence in doc_occurrences]

    def get_doc_name_from_id(self, doc_id):
        return self.doc_id_dict[doc_id][0]

    def search_term_in_docs(self, term):
        term = term.lower()
        doc_ids = self.get_doc_ids_containing_term(term)
        if not doc_ids:
            return []
        return [self.get_doc_name_from_id(doc_id) for doc_id in doc_ids]


if __name__ == '__main__':
    dir_path = 'outputs/index'
    term_id_path, doc_id_path, inverted_index_path = \
        ["{}/{}".format(dir_path, file_name)
         for file_name in ['TermIDFile.csv', 'DocumentIDFile.csv', 'InvertedIndex.json']]
    inverted_index = UseIndex(term_id_path, doc_id_path, inverted_index_path)

    term_to_query = 'asterisk'
    print('Searching for term {} in all docs...\n'.format(term_to_query))
    [print(doc_name) for doc_name in inverted_index.search_term_in_docs(term_to_query)]
