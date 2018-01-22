# radeonpower

This utility allows to set the radeon driver to keep a specific GPU frequency. 

I've observed that setting manually the frequency of my Radeon GPU would be overwritten over time and resets to automatic frequency mode. This in my case generates too much noise, so this utility allows to keep the frequency at a specific level.

# Usage

## List available frequencies

```
$ ./bin/radeonpower.py list 
manual
0: 300Mhz
1: 608Mhz
2: 928Mhz
3: 1098Mhz *
4: 1167Mhz
5: 1214Mhz
6: 1260Mhz
7: 1291Mhz
```

## Set frequency

```
% sudo ./bin/radeonpower.py set 3
```
