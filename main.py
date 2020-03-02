import hashlib
import requests
import json

BLOCKSIZE = 65536

fapi = open("apikey.txt", "r")


apiKey = fapi.readline()
print(apiKey)

inputFile = "dandandan.txt"



hasher = hashlib.sha1()

with open(inputFile, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)


hashCode = hasher.hexdigest()

#   PART 2: erform a hash lookup against metadefender.opswat.com and see if their are previously cached results for the file
headers = {
    'apikey': apiKey,
}

r = requests.get('https://api.metadefender.com/v4/hash/'+hashCode, headers=headers)


if r.status_code == 200:
    print("File has been found on metadefender.opswat.com")
    fileFound = 1
    json_response = r.json()
    with open('part1.json', 'w') as f:
        json.dump(json_response, f, indent=4)
elif r.status_code == 404:
    print("File has not been found on metadefender.opswat.com")
    fileFound = 0
elif r.status_code == 400:
    print('Bad Request.')











# PART 3: IF RESULTS HAVE BEEN FOUND SKIP TO PART 6
if fileFound == 0:

    # PART 4: IF RESULTS NOT FOUND THEN UPLOAD THE FILE AND RECEIVE data_id
    headers = {
        'apikey': apiKey,
        'filename': inputFile,
        'content-type': 'application/octet-stream',
    }

    print("Uploading file to metadefender.opswat.com")

    afile = open(inputFile)
    r = requests.post('https://api.metadefender.com/v4/file', data=afile, headers=headers)
    #print (r.status_code)


    if r.status_code == 200:
        print('Success!')
    elif r.status_code == 404:
        print('Not Found.')
    elif r.status_code == 400:
        print('Bad Request.')


    json_response = r.json()
    # HERE IS THE DATA ID
    data_id = json_response['data_id']
    print("data_id: " + data_id)



    headers2 = {
        'apikey': apiKey,
    }

    print("Retrieving results from metadefender.opswat.com")


    r = requests.get('https://api.metadefender.com/v4/file/'+data_id, headers=headers2)
    json_response = r.json()
    per = json_response['scan_results']['progress_percentage']

    while (per != 100):
        r = requests.get('https://api.metadefender.com/v4/file/'+data_id, headers=headers2)
        json_response = r.json()  
        per = json_response['scan_results']['progress_percentage']


    


    if r.status_code == 200:
        print('Success!')
    elif r.status_code == 404:
        print('Not Found.')
    elif r.status_code == 400:
        print('Bad Request.')

    json_response = r.json()
    with open('part3.json', 'w') as f:
        json.dump(json_response, f, indent=4)


# Print results

results = json_response['scan_results']['scan_details']

print("\nfilename: " + json_response['file_info']['display_name'])
print("overall_status: " + json_response['scan_results']['scan_all_result_a'] + "\n")

for engine in results:
    print("engine: " + engine)
    values = results.get(engine)
    print ("threat_found: " + values.get('threat_found'))
    print ("scan_result: " + str(values.get('scan_result_i')))
    print ("def_time: " + values.get('def_time') + "\n")
    