import requests
import csv
import os
from concurrent.futures import ThreadPoolExecutor

def downloading_content(url, filename) :
    try:

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, 'wb') as file:

            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Error while downloading from '{url}' : '{e}'\n")

def main():

    try:

        csv_file_url = 'https://raw.githubusercontent.com/prasertcbs/basic-dataset/refs/heads/master/Country_Flags.csv'
        filename = 'flags_data.csv'
        flags_folder = 'Flags'
        downloading_content(csv_file_url, filename)

        data = []
        try:

            with open(filename, 'r', newline='') as csvfile:
                
                render = csv.DictReader(csvfile)
                for row in render:
                    data.append(row)
                
                print(data)
        
        except FileNotFoundError:
            print("The csv file could not be found")

        if not os.path.exists(flags_folder):
                
            os.makedirs(flags_folder)
            print(f"Created folder '{flags_folder}'")

        download_tasks = []
        for row in data:

            image_filename = row.get('Images File Name')
            image_url = row.get('ImageURL')

            if image_filename and image_url:
                filepath = os.path.join(flags_folder, image_filename)
                download_tasks.append((image_url, filepath))

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(lambda args: downloading_content(*args), download_tasks)

        successful_downloads = sum(1 for result in results if result)
        print(f"Successfully downloaded {successful_downloads}/{len(download_tasks)} files")

    except Exception as e:
        print(f"Error occured while running the program '{e}'\n")

main()