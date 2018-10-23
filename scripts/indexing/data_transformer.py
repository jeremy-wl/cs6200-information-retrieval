import os
import re


def extract_terms_from_html(html):
    noises_regex = ['(<script.*?>[\s\S]*?</script>)',
                    '(<style.*?>[\s\S]*?</style>)',
                    '(<.+?>)|(</[\s\S]*?>)',
                    '(<!--[\s\S]*?-->)',
                    '(&\w{2,};)',  # remove HTML Character Entities
                    '(&#\d{2,};)',
                    '([^\w\d])',  # replace non-word/digit characters with space
                    ]
    for regexp in noises_regex:
        html = re.sub(regexp, ' ', html)
    terms = re.split(r'[ \n]', html)
    return [x.lower() for x in terms if x]  # remove empty strings & convert to lowercase


def transform_data(folder_name, num_files_to_process):
    doc_name_to_terms = {}

    file_names = os.listdir(folder_name)
    file_names.sort()

    for i in range(0, num_files_to_process):
        file_name = file_names[i]
        html_content = open("{}/{}".format(folder_name, file_name), 'r').read()
        terms = extract_terms_from_html(html_content)
        doc_name_to_terms[file_name] = terms

    return doc_name_to_terms
