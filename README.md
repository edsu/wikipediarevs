# wikipedia-revision-downloader

If you have a file of Wikipedia article URLs you can get the page revisions for all of them (one JSON file per revision).

For example if you have a file `urls.txt` that looks like:

```
https://en.wikipedia.org/wiki/Jerry_Carl
https://en.wikipedia.org/wiki/Barry_Moore_(Alabama_politician)
https://en.wikipedia.org/wiki/Mike_Rogers_(Alabama_politician)
```

You can run it:

```
python3 download.py urls.txt
```

And you will get a directory structure something like this:

```

revisions/
├── Barry_Moore_(Alabama_politician)
│   ├── 1000074619.json
│   ├── 1001186002.json
│   ├── 1001186057.json
│   ├── 1001186171.json
│   ├── 1001379529.json
│   ├── 1002388537.json
│   ├── 1002388609.json
│   ├── 1002391650.json
│   ├── 1003058740.json
│   ├── 1003090522.json
│   ├── 1003271080.json
│   ├── 1003272307.json
│   ├── 1003272470.json
│   ├── 999778018.json
│   ├── 999786895.json
│   └── 999792418.json
├── Jerry_Carl
│   ├── 1000000534.json
│   ├── 1000006293.json
│   ├── 1001107836.json
│   ├── 1001376846.json
│   ├── 1001972408.json
│   ├── 1002072058.json
│   ├── 1002390935.json
│   ├── 1002454796.json
│   ├── 1003026311.json
│   ├── 1003026363.json
│   ├── 1005066613.json
│   ├── 1005066718.json
│   ├── 1005620620.json
│   ├── 1006075769.json
│   ├── 1006197989.json
│   ├── 1006225109.json
│   ├── 1006225140.json
│   ├── 1006225170.json
│   ├── 1006225219.json
│   ├── 1007327304.json
│   ├── 998146365.json
│   ├── 998150802.json
│   ├── 998274904.json
│   ├── 998357586.json
│   ├── 998948849.json
│   ├── 999092493.json
│   ├── 999432186.json
│   ├── 999612298.json
│   ├── 999615881.json
│   └── 999637958.json
└── Mike_Rogers_(Alabama_politician)
    ├── 1001291034.json
    ├── 1003647559.json
    ├── 1004090538.json
    ├── 1004348997.json
    ├── 1004974353.json
    ├── 1006228113.json
    ├── 1006228248.json
    ├── 1009067146.json
    ├── 1010222940.json
    ├── 1010934696.json
    ├── 1010934713.json
    ├── 1010934776.json
    ├── 1011030142.json
    ├── 1011771252.json
    ├── 1011850746.json
    ├── 1014155244.json
    ├── 1014706553.json
    ├── 1016474751.json
    ├── 1018172988.json
    ├── 1019750184.json
    ├── 1019865675.json
    ├── 994662779.json
    ├── 995068272.json
    ├── 995389014.json
    ├── 998066954.json
    ├── 998067054.json
    ├── 998099472.json
    ├── 998240880.json
    ├── 999612611.json
    └── 999616261.json
```

To understand the meaning of the JSON files you will want to consult the Wikipedia API documentation:

https://en.wikipedia.org/w/api.php?action=help&modules=query%2Brevisions

It is likely you will need to install the requests module if you don't have it already:

```
$ pip install requests
```
