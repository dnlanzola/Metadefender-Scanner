import hashlib
import requests
import json
import os

BLOCKSIZE = 65536

# READ APIKEY FROM FILE
fapi = open("apikey.txt", "r")
apiKey = fapi.readline()

while (1):
    # READ FILE NAME FROM USER
    inputFile = input("Enter name of file: ")

    # CALCULATE THE HASH OF THE FILE
    if os.path.exists(inputFile):
        hasher = hashlib.sha1()
        with open(inputFile, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        break
    else:
        print("File does not exist")

hashCode = hasher.hexdigest()

#   PART 2: perform a hash lookup against metadefender.opswat.com and see if their are previously cached results for the file
headers = {
    'apikey': apiKey,
}

r = requests.get('https://api.metadefender.com/v4/hash/'+hashCode, headers=headers)


if r.status_code == 200:
    print("File has been found on metadefender.opswat.com")
    fileFound = 1
    json_response = r.json()

elif r.status_code == 404:
    print("File has not been found on metadefender.opswat.com")
    fileFound = 0

elif r.status_code == 400:
    print('Bad Request.')
    quit()


# PART 3: If results have been found skip to part 6
if fileFound == 0:

    # PART 4: If results not found then upload the file and receive data_id
    headers = {
        'apikey': apiKey,
        'filename': inputFile,
        'content-type': 'application/octet-stream',
    }

    print("Uploading file to metadefender.opswat.com")

    afile = open(inputFile)
    r = requests.post('https://api.metadefender.com/v4/file', data=afile, headers=headers)

    if r.status_code == 200:
        print('File has been uploaded to metadefender.opswat.com')
    elif r.status_code == 404:
        print('Not Found.')
    elif r.status_code == 400:
        print('Bad Request.')
        quit()

    json_response = r.json()
    # Retrieving data_id
    data_id = json_response['data_id']

    headers = {
        'apikey': apiKey,
    }

    print("Retrieving results from metadefender.opswat.com")

    # PART 5: Repeatedly pull on the data_id to retrieve results
    per = 0
    while (per != 100):
        r = requests.get('https://api.metadefender.com/v4/file/'+data_id, headers=headers)
        json_response = r.json()  
        per = json_response['scan_results']['progress_percentage']

    if r.status_code == 200:
        print('Results have been retrieved from metadefender.opswat.com')
    elif r.status_code == 404:
        print('Not Found.')
    elif r.status_code == 400:
        print('Bad Request.')
        quit()

    json_response = r.json()
    with open('part3.json', 'w') as f:
        json.dump(json_response, f, indent=4)


# PART 6: Display results
results = json_response['scan_results']['scan_details']

print("\nfilename: " + json_response['file_info']['display_name'])
print("overall_status: " + json_response['scan_results']['scan_all_result_a'] + "\n")

for engine in results:
    print("engine: " + engine)
    values = results.get(engine)
    print ("threat_found: " + values.get('threat_found'))
    print ("scan_result: " + str(values.get('scan_result_i')))
    print ("def_time: " + values.get('def_time') + "\n")