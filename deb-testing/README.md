Build with:

```
docker build -t am151 .
```

Test with:
```
docker run -i -t --rm -v (pwd)/seed:/seed -p 5000:80 -p 5050:8000 am151 /run.sh
```

Default user/password is test/test

