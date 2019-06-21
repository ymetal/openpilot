Dependencies
--------

**Mac**

```
./get_sdk_mac.sh
```

**Debian / Ubuntu**

```
./get_sdk.sh
```


Programming
----

**Panda**

```
make
```

<<<<<<< HEAD
**NEO**

```
make -f Makefile.legacy
```

=======
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
Troubleshooting
----

If your panda will not flash and is quickly blinking a single Green LED, use:
```
make recover
```


[dfu-util](http://github.com/dsigma/dfu-util.git) for flashing
