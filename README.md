# TCP Simulation

- `Python version >=3.10`

To run this code: 

```shell
python3 server.py -l False -b False -p 0 -r 0
python3 router.py -s True -d 1 -q 5
python3 client.py
```

The options and definition for each argument can be found by using `--help` command.