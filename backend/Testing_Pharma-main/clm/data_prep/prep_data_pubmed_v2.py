import sys
import os
import gzip
import xml.etree.ElementTree as ET

'''
#import re

def clean_html_tags(text):
    """Removes simple HTML-like tags from a string."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
'''

def get_full_text_from_element(element):
    """
    Extracts all text content from an XML element, including nested child text.
    
    Args:
        element: An xml.etree.ElementTree element.
    
    Returns:
        str: The full concatenated text.
    """
    text_content = ""
    # Get the text directly from the parent element
    if element.text:
        text_content += element.text.strip()
   
    # Iterate through all children to get their text and tail
    for child in element.iter():
        if child.text:
            text_content += " " + child.text.strip()
        if child.tail:
            text_content += " " + child.tail.strip()
            
    # Clean up any multiple spaces that might have been created
    return " ".join(text_content.split())


def extract_pubmed_articles_to_txt(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.xml.gz'):
            continue

        output_sub_dir = os.path.join(output_dir, filename[:-7])
        #os.makedirs(output_sub_dir, exist_ok=True)
        try:
            os.makedirs(output_sub_dir, exist_ok=False)
        except FileExistsError as e:
            print(f'  -> Skipping {filename}')
            continue

        file_path = os.path.join(input_dir, filename)
        print(f"  -> Processing {filename}")

        try:
            with gzip.open(file_path, 'r') as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for article in root.findall('.//PubmedArticle'):
                    pmid_element = article.find('.//PMID')
                    title_element = article.find('.//ArticleTitle')
                    abstract_element = article.find('.//Abstract') # Find the parent of AbstractText

                    pmid_text = ""
                    if pmid_element is not None:
                        pmid_text = pmid_element.text.strip()
                    
                    # Use the new function to get all text from the elements
                    title_text = ""
                    if title_element is not None:
                        title_text = get_full_text_from_element(title_element)
                    
                    abstract_text = ""
                    # AbstractText can be nested within Abstract, so we use findall
                    if abstract_element is not None:
                        abstract_text_list = abstract_element.findall('.//AbstractText')
                        for abs_text in abstract_text_list:
                            abstract_text += get_full_text_from_element(abs_text) + " "

                    if len(pmid_text) * len(title_text) * len(abstract_text) != 0:
                        output_file = os.path.join(output_sub_dir, f'{pmid_text}.txt')
                        with open(output_file, 'w', encoding='utf-8') as outfile:
                            outfile.write(f"{title_text}\n")
                            outfile.write(f"{abstract_text.strip()}\n")
                        print(f"Extracted data saved to '{output_file}'")
        
        except ET.ParseError as e:
            print(f"  - Error parsing {filename}: {e}")
        except Exception as e:
            print(f"  - An unexpected error occurred with {filename}: {e}")
    
    print(f"\nCompleted.")


# python3 prep_data_pubmed_v2.py test        testTXT
# python3 prep_data_pubmed_v2.py baseline    baselineTXT 
# python3 prep_data_pubmed_v2.py updatefiles updatefilesTXT



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{sys.argv[0]} [input_dir] [output_dir]", file=sys.stderr)
        sys.exit(1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_dir):
        print(f"Error: The input_dir '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    extract_pubmed_articles_to_txt(input_dir, output_dir)