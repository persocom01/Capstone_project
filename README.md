# Capstone_project

## Installation



## Known issues

Python's locale.getpreferredencoding() returns cp1252 in windows. This may cause problems with information from certain web apis. To rectify this problem, type:

```
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
```
