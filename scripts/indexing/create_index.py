import os
import json
import data_transformer as transformer


term_dict = {}  # term => [term_id, freq_in_docs]
doc_id_dict = {}  # doc_id => [doc_name, num_of_terms]


# process terms in n files in folder, and build term_dict & doc_id_dict & inverted_lists
def process_terms(doc_name_to_terms):
    doc_id, term_id = 0, 0

    inverted_lists = []
    for doc_name, terms in doc_name_to_terms.items():
        for term in terms:
            inverted_lists.append([term, doc_id])
            if term not in term_dict:
                term_dict[term] = [term_id, 1]
                term_id += 1

        doc_id_dict[doc_id] = [doc_name, len(terms)]
        doc_id += 1

    inverted_lists.sort(key=lambda x: x[0])
    return inverted_lists


# build inverted_index from inverted_lists
def build_inverted_index(inverted_lists):
    prev_term, prev_doc_id = inverted_lists[0][0], inverted_lists[0][1]
    freq_in_doc = 1
    inverted_index = {term_dict[prev_term][0]: {}}

    for i in range(1, len(inverted_lists)):
        term, doc_id = inverted_lists[i][0], inverted_lists[i][1]
        term_id = term_dict[term][0]

        if term_id not in inverted_index:
            inverted_index[term_id] = {}
        if term == prev_term:
            if doc_id == prev_doc_id:
                freq_in_doc += 1
            else:
                inverted_index[term_id][prev_doc_id] = freq_in_doc
                prev_doc_id = doc_id
                freq_in_doc = 1
                term_dict[prev_term][1] += 1
        else:
            term_id, prev_term_id = term_dict[term][0], term_dict[prev_term][0]
            inverted_index[prev_term_id][prev_doc_id] = freq_in_doc
            prev_term, prev_doc_id = term, doc_id
            freq_in_doc = 1
    term_dict[prev_term][1] += 1
    inverted_index[term_dict[prev_term][0]][prev_doc_id] = freq_in_doc
    return inverted_index


# write term_dict, doc_id_dict, inverted_index to separate files
def write_to_files(inverted_index):
    dir_path = 'outputs/index'
    os.makedirs(dir_path, exist_ok=True)
    with open('{}/TermIDFile.csv'.format(dir_path), 'w+') as file_term_id:
        file_term_id.write('term_id,term,freq')
        # term => [term_id, freq_in_docs]
        for term, val in term_dict.items():
            term_id, freq_in_docs = val[0], val[1]
            file_term_id.write("\n{},{},{}".format(term_id, term, freq_in_docs))

    with open('{}/DocumentIDFile.csv'.format(dir_path), 'w+') as file_doc_id:
        file_doc_id.write('doc_id,doc_name,num_terms')
        # doc_id_dict = {}  # doc_id => [doc_name, num_of_terms]
        for doc_id, val in doc_id_dict.items():
            doc_name, num_terms = val[0], val[1]
            file_doc_id.write("\n{},{},{}".format(doc_id, doc_name, num_terms))

    with open('{}/InvertedIndex.json'.format(dir_path), 'w+') as file_inverted_index:
        json.dump(inverted_index, file_inverted_index, sort_keys=True)
    # [print(k, v) for k, v in inverted_index.items()]


# create inverted index with the three steps below
def create_index(doc_name_to_terms):
    inverted_lists = process_terms(doc_name_to_terms)
    inverted_index = build_inverted_index(inverted_lists)
    write_to_files(inverted_index)


if __name__ == '__main__':
    folder_path, num_files = '~/Projects/CS6200/Assignments/outputs/html', 900
    doc_name_to_terms = transformer.transform_data(os.path.expanduser(folder_path), num_files)

    create_index(doc_name_to_terms)
