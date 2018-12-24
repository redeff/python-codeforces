# Utility to do codeforces submissions from the commandline
## Note
All commands sould be ran under the pipenv environment, which can be accessed though `pipenv shell`
## Logging and submitting
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

## Downloading testcases
All testcases are stored in the following path:
```
<cwd>/<contest>/<problem>/<testcase-number>.<in/out>
```
To download the testcases corresponding to a problem, use the syntax:
```
./main.py do <contest> <problem>
```
To download the testcases corresponding to a contest, use the syntax:
```
./main.py do <contest>
```
Executing this command will also open a browser tab with all the problems

### Example usage
```
cd ~/codeforces
./main.py 1082 B
./main.py 1085

```
You will end up with a directory structure similar to the following:
```
~/codeforces
	/1082
		/B
			0.in
			0.out
			1.in
			1.out
	/1085
		/A
			0.in
			0.out
		/B
			0.in
			0.out
			1.in
			1.out
			2.in
			2.out
		/C
			0.in
			0.out
			1.in
			1.out
		.
		.
		.
```
