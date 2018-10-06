# Utility to do codeforces submissions from the commandline
## Usage
First, you have to generate the credentials by running
```
./main.py <username> <password>
```
and capturing stdout.
Then that output must be piped into:
```
./main.py submit <contest> <problem> <path/to/solution> [<language-code>]
```
If language code is ommited, the the language code for c++17 will be used.
If language code is "\_", then it will be inferred from the file extension of the solution

### Example usage
```
./main.py myusername hunter2 > credentials.txt
./main.py submit 701 A ~/solutions/a.txt < credentials.txt
./main.py submit 701 B ~/solutions/b.txt < credentials.txt
```
