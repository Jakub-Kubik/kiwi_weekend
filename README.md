# Kiwi.com Python weekend Entry task
Program is CLI application. Program get airports in the United Kingdom and display them on standard output.

The task is on webpage: https://gist.github.com/fholec/ecc9c8a3bb82fdf3eabab66efb7c594b

## Return codes
- `0` - no error
- `2` - program parameters error
- `3` - get airports data error
- `4` - get latitude and longitude from kiwi api error

## Run 
```<python3> ./kiwi_weekend.py <parameters>```

## Examples
- No parameters
```
./kiwi_weekend.py
Aldergrove International Airport, BFS, 
George Best Belfast City Airport, BHD, 
Andover Airport, ADV, 
Anglesey Airport, HLY, 
Bally Kelly Airport, BOL, 
Baltasound Airport, UNT, 
Bembridge Airport, BBP, 
.
.
.
```

- Parameter for printing all information
```
./kiwi_weekend.py --full
Belfast, Aldergrove International Airport, BFS, 54.6575, -6.215833,
Belfast, George Best Belfast City Airport, BHD, 54.618056, -5.8725,
Andover, Andover Airport, ADV, None, None,
Holyhead, Anglesey Airport, HLY, None, None,
Bally Kelly, Bally Kelly Airport, BOL, None, None,
Unst Shetland Is, Baltasound Airport, UNT, None, None,
Bembridge, Bembridge Airport, BBP, None, None,
.
.
.
```

- Combination of other parameters
```
./kiwi_weekend.py --cities --iata --coords
Belfast, BFS, 54.6575, -6.215833, 
Belfast, BHD, 54.618056, -5.8725, 
Andover, ADV, None, None, 
Holyhead, HLY, None, None, 
Bally Kelly, BOL, None, None, 
Unst Shetland Is, UNT, None, None, 
Bembridge, BBP, None, None, 
.
.
.
```

## Author
Jakub Kubik <jakupkubik@gmail.com>
