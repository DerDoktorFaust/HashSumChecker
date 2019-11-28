# HashSumChecker

Version 2.0
Rather than computing MD5, SHA1, and SHA 256 hashes with console commands, the hashlib module is used to compute the file directly.

User can now drag and drop a highlighted hash code into its respective field rather than copying and pasting (though this still works of course)

Error checking has been revamped and now if any field is left blank or if the file cannot be found, an exception is thrown and the program continues to function.


Version 1.0

Allows user to browse for a file or drag and drop a file, paste the provided hashsum, calculate the hashsum of the file, 
and then compares it to the provided hash sum.

Uses PyQt5 for the GUI and does shell commands to compute hash sums. Works on MacOS, tested on MacOS Catalina (10.15)
