# cloudminingstatus
reports status of nicehash.com and miners-zone.net (open-ethereum-pool)

### how
```bash
git clone https://github.com/drandreaskrueger/cloudminingstatus.git
cd cloudminingstatus
python2 cloudminingstatus.py 
```
It will go into an endless loop (prints every 5 minutes), until you press "Ctrl-C" 

### your credentials
You must fill in your personal credentials, ideally in a copy:

```bash
cp credentials.py credentials_ME.py
edit credentials_ME.py
```

### dependencies
* python 2.7
* python `requests` (install e.g. via `pip`)

```bash
apt-get install python-pip
pip install requests
```

### limitations & extensions
At the moment this works with 
* cloudhasher http://nicehash.com
* pool http://soil.miners-zone.net (open-ethereum-pool)

When you adapt it to your situation, please make a pull request, so that I can include your pool/cloudminer settings. 

Or pay and ask me to do it for you.

### donationware
[BTC] 1M3HHX8h772LZ8MWMRBetT5RNVWqjC6iK1
