# Plot histogram of the cyclictest output

## Run cyclictest and convert output to csv

```
# Example for machine with 4 cores:
$ sudo cyclictest -l5000000 -m -S -p90 -i200 -h400 -q > output.txt
```

## Plot the result

```
$ python3 plot-histogram.py -h
$ python3 plot-histogram.py <histogram.csv> --title "Plot title" --save --filename "filename.png"
```

## Images

[image1]: ./img/histogram.png " "
[image2]: ./img/histogram-rt.png " "

<img src="./img/histogram.png" alt="Histogram" width="800"/>
<img src="./img/histogram-rt.png" alt="Histogram RT" width="800"/>


