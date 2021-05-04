# hz-rc-archive
Archive GCCRC in Hangzhou.

## Usage
Export to json line format
```commandline
scrapy crawl hzrc -O hzrc.jl -L WARNING
```

Run with persistence in MongoDB
```commandline
set MONGO_GCCRC_USER=<collection username>
set MONGO_GCCRC_PASSWORD=<collection password>
scrapy crawl hzrc
```
