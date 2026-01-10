import sys
import os
import gzip
import xml.etree.ElementTree as ET

import pdb


def get_full_text(element, namespaces):
    """
    Recursively extracts all text content from an XML element and its children,
    adding spaces to maintain readability.
    """
    if element is None:
        return ""
    
    parts = []
    
    # Text directly under the element
    if element.text:
        parts.append(element.text.strip())
        
    # Iterate through all children to get their text and tail
    for child in element:
        parts.append(get_full_text(child, namespaces))
        if child.tail:
            parts.append(child.tail.strip())
            
    # Join parts with a single space and clean up any extra spaces
    return " ".join(parts).strip()

def extract_dailymed_data(input_dir, output_dir):
    """
    Processes all XML files in a directory to extract and save
    section data to separate TXT files.
    
    Args:
        input_dir (str): The directory containing the XML files.
        output_dir (str): The directory to save the output TXT files.
    """
    if not os.path.exists(input_dir):
        print(f"Error: The input directory '{input_dir}' does not exist.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting to process files in '{input_dir}'...")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.xml'):
            file_path = os.path.join(input_dir, filename)
            
            output_file = os.path.join(output_dir, f'{filename[:-4]}.txt')
            
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                namespaces = {
                    prefix: uri for event, (prefix, uri) in ET.iterparse(file_path, events=['start-ns'])
                }
                
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    for section in root.findall('.//section', namespaces):
                        title_elem = section.find('./title', namespaces)
                        text_elem = section.find('./text', namespaces)
                        
                        title_text = get_full_text(title_elem, namespaces)
                        text_text = get_full_text(text_elem, namespaces)
                        
                        if title_text or text_text:
                            if title_text:
                                outfile.write(f"{title_text}\n")
                            if text_text:
                                outfile.write(f"{text_text}\n")
                                                        
                print(f"  -> Processed {filename} and saved to {output_file}")
            
            except ET.ParseError as e:
                print(f"  - Error parsing {filename}: {e}")
            except Exception as e:
                print(f"  - An unexpected error occurred with {filename}: {e}")

    print(f"\nCompleted. All extracted data saved to '{output_dir}'")

# python3 prep_data_dailymed.py test          testTXT

# python3 prep_data_dailymed.py otc01         otc01TXT
# python3 prep_data_dailymed.py otc02         otc02TXT
# python3 prep_data_dailymed.py otc03         otc03TXT
# python3 prep_data_dailymed.py otc04         otc04TXT
# python3 prep_data_dailymed.py otc05         otc05TXT
# python3 prep_data_dailymed.py otc06         otc06TXT
# python3 prep_data_dailymed.py otc07         otc07TXT
# python3 prep_data_dailymed.py otc08         otc08TXT
# python3 prep_data_dailymed.py otc09         otc09TXT
# python3 prep_data_dailymed.py otc10         otc10TXT
# python3 prep_data_dailymed.py otc11         otc11TXT

# python3 prep_data_dailymed.py prescription1 prescription1TXT
# python3 prep_data_dailymed.py prescription2 prescription2TXT
# python3 prep_data_dailymed.py prescription3 prescription3TXT
# python3 prep_data_dailymed.py prescription4 prescription4TXT
# python3 prep_data_dailymed.py prescription5 prescription5TXT


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{sys.argv[0]} [input_dir] [output_dir]", file=sys.stderr)
        sys.exit(1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_dir):
        print(f"Error: The input_dir '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    extract_dailymed_data(input_dir, output_dir)