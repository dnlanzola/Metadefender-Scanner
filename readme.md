# **Opswat Metadefender**
The purpose of this program is to scan a file against OPSWAT's MetaDefender API.

### Description
This program allows the user to type in the name of the file that is going to be scanned. The program calculates the hash of the file (SHA1) and perform a hash lookup against metadefender.opswat.com. Then, it will report wether the file has been previously uploaded or not. If the file has been previously uploaded it will proceed to display the results. In the case where the file has not been previously uploaded it will be uploaded to the server. Then, it will obtain the data ID from the file to retrieve the results.

### Environment
Developed using Python 3.7.1 in Visual Studio Code.

### Instructions to run this program:
* Use the provided file "apikey.txt" to provide your own API Key, simply paste your API key in the file.
* Open terminal Linux/MacOS.
* Type: "./metadefender.sh".
* The program will ask you to type the name of the file you want to scan.
* Results will be displayed in screen.