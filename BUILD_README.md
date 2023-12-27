## Building SpiderMan Dataset

Following must help you to build SpiderMan from the original Spider data.

### 1. Download the Spider.zip

You can execute the following command to download `Spider.zip` into the `./source` directory.

```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1TqleXec_OykOYFREKKtschzY29dUcVAQ' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1TqleXec_OykOYFREKKtschzY29dUcVAQ" -O ./source/spider.zip && rm -rf /tmp/cookies.txt
```

You can also download `spider.zip` manually from [here](https://drive.google.com/uc?export=download&id=1TqleXec_OykOYFREKKtschzY29dUcVAQ), into the `./source` directory.

### 2. Build dataset

Execute the following to recreate the dataset from the zip downloaded in step 1.

```
python scripts/build_dataset.py
```
