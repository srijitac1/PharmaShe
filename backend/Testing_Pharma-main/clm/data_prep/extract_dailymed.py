import sys
import os
import zipfile
import shutil

'''
dm_spl_release_human_rx_part5.zip
--> prescription/20250424_58ce42c6-10bd-4bb4-bf89-eae8ed82c339.zip
                 ...
    prescription/20250902_f47d15a8-f534-4ef2-bc3d-26a05d541220.zip
    --> b7107c00-c7a7-4493-b0ae-a4fd7bf70856.xml  
        LBL USPUN1072.jpg
        Liuid 02.jpg
        Norco_COA_o2.jpg

dm_spl_release_human_otc_part11.zip
--> otc/20250831_0028f88d-a9fe-4cfa-a6c6-168f9689b5f6.zip
       ...
    otc/20250902_eafc00ce-12e7-921f-e053-2995a90a241a.zip
    --> ./3d2f1fb9-8aca-8409-e063-6394a90aabba.xml
        ./Neutrogena_1.jpg
'''

def process_nested_zip_for_xml(zip_path, output_dir):
    """
    Processes a main ZIP file containing nested ZIPs, extracts only XML files,
    and saves them to a 'prescription' or 'otc' directory.

    Args:
        zip_path (str): The path to the main ZIP file.
    """
    print(f"Starting to process: {zip_path}")

    try:
        # Step 1: Extract the contents of the main ZIP file to the temporary directory
        with zipfile.ZipFile(zip_path, 'r') as main_zip:
            print("Extracting main ZIP file...")
            main_zip.extractall('.')
            print("Main ZIP file extracted.")

        # Step 2: Traverse the temporary directory to find nested ZIP files
        for root, _, files in os.walk(output_dir):
            for file_name in files:
                if file_name.endswith('.zip'):
                    nested_zip_path = os.path.join(root, file_name)
                    print(f"\nProcessing nested ZIP: {nested_zip_path}")
                    
                    try:
                        # Step 3: Extract only XML files from the nested ZIP
                        with zipfile.ZipFile(nested_zip_path, 'r') as nested_zip:
                            for member in nested_zip.namelist():
                                if member.lower().endswith('.xml'):
                                    # Create the full path for the XML file in the output directory
                                    xml_file_name = os.path.basename(member)
                                    output_path = os.path.join(output_dir, xml_file_name)
                                    
                                    print(f"  -> Extracting {xml_file_name} to {output_dir}")
                                    
                                    # Extract the XML file
                                    with nested_zip.open(member, 'r') as source_xml, open(output_path, 'wb') as dest_xml:
                                        shutil.copyfileobj(source_xml, dest_xml)
                                    print(f"  -> Successfully saved {xml_file_name}")

                    except zipfile.BadZipFile:
                        print(f"  - Error: The file {nested_zip_path} is not a valid ZIP file. Skipping.")
                    except Exception as e:
                        print(f"  - An unexpected error occurred while processing {nested_zip_path}: {e}")
                    finally:
                        print(f"Deleting nested zip file: {nested_zip_path}")
                        os.remove(nested_zip_path)
                        
    except zipfile.BadZipFile:
        print(f"Error: The file {zip_path} is not a valid ZIP file. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Step 4: Clean up the_main and nested zip_files
        print(f"Deleting original zip file: {zip_path}")
        os.remove(zip_path)
        #os.utime(zip_path, None)  # touch zip_path


# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} [dailymed.ZIP]", file=sys.stderr)
        sys.exit(1)

    zip_file = sys.argv[1]
    output_dir = None
    if zip_file.startswith('dm_spl_release_human_rx'):
        output_dir = 'prescription'
    elif zip_file.startswith('dm_spl_release_human_otc'):
        output_dir = 'otc'
    
    if os.path.exists(zip_file) and output_dir is not None:
        process_nested_zip_for_xml(zip_file, output_dir)
    else:
        print(f"Valid file not found: {zip_file}", file=sys.stderr)
        sys.exit(1)
