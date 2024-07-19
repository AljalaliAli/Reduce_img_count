'''The ImageTimestampMatcher.py script is designed to copy image files with matching timestamps from a source folder to a destination folder. The timestamps are matched against a list of timestamps stored in a SQLite database.'''
import os
import shutil
import sqlite3
import re

def get_ts_list(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT TS FROM {table_name}")
    rows = cur.fetchall()
    conn.close()
    ts_list = [row[0] for row in rows]
    return ts_list

## for the old standard image name 
'''def extract_timestamp_from_filename(filename):
    # Regular expression to match the date and time part
    pattern = r'(\d{4})-(\d{2})-(\d{2})_(\d{2})_(\d{2})_(\d{2})'

    match = re.search(pattern, filename)
    if match:
        # Extracting and formatting the timestamp
        timestamp = f"{match.group(1)}-{match.group(2)}-{match.group(3)} {match.group(4)}:{match.group(5)}:{match.group(6)}"
        return timestamp
    else:
        
        return None'''
 
## for the new standard image name 
def extract_timestamp_from_filename(filename):
    # Remove the file extension
    filename_without_extension = filename.split('.')[0]

    # Split the filename into parts
    parts = filename_without_extension.split('_')

    # Extract the date and time parts
    date = parts[2]
    time = parts[3]

    # Format the timestamp
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    formatted_time = f"{time[:2]}:{time[2:4]}:{time[4:]}"
    timestamp = f"{formatted_date} {formatted_time}"

    return timestamp


def copy_matching_images(src_folder, dst_folder, db_path, table_name):
    ts_list = get_ts_list(db_path, table_name)
    print(f"ts_count:{len(ts_list)}")
    i=0
    k=0
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            k+=1
            print(f"....................................................................k= {k} ................................................................................")
            if file.endswith(".tiff"):
                # Extract the timestamp from the image name
                image_ts = extract_timestamp_from_filename(file)
                print(file)
                if image_ts:     
                    # Check if the image timestamp matches any timestamp in the list
                    if image_ts in ts_list:
                        i=i+1
                        print(i)
                        #print(f"img_name={file}")
                       # print(f"image_ts={image_ts}")
                        # Construct the source and destination file paths
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(dst_folder, file)

                        # Ensure the destination directory exists
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        
                        # Copy the image to the destination folder
                        shutil.copy2(src_file, dst_file)

# Example usage
copy_matching_images(
    r"D:\future link\AljalaliAli\OCR Tesseract Feintuning\OCR Test 001\Results\Mues\check the results\NEW_MDE\standard_images_Mues_3_from_20.02.024 to 05.06.2024",
    r"./uniq_data_sets_imgs",
    r"D:\future link\AljalaliAli\OCR Tesseract Feintuning\OCR Test 002\Compare\xyw_ID0008_MID0003_MDE_2024.db", 'MDE_uniqe'
)
