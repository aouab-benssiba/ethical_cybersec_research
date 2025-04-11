# automate recon 

## Introduction
New hackers often overlook the power of automation, but once mastered, it becomes an indispensable part of your workflow. This guide dives into automating reconnaissance (recon) using shell scripting—a critical phase in ethical hacking that uncovers vulnerabilities like:  
- **Sensitive information disclosure**  
- **Open S3 buckets**  
- **Subdomain takeovers**  
- **Buggy application configurations**  

By streamlining recon, you save time and gain a comprehensive view of your target's attack surface.  

---

## Prerequisites
- Basic Linux commands and shell scripting knowledge.  
- Networking fundamentals (client-server architecture).  
- Understanding of protocols (HTTP, FTP, SSH).  

---

## Step 1: Subdomain Enumeration
**Tools Used**:  
1. [Sublist3r](https://github.com/aboul3la/Sublist3r)  
2. [Assetfinder](https://github.com/tomnomnom/assetfinder)  
3. [httprobe](https://github.com/tomnomnom/httprobe)  
4. Manual methods (Google Dorks, GitHub, crt.sh)  

### Script: `enum.sh`
```bash
#!/bin/bash
# Subdomain Enumeration Script
DOMAIN=$1

# Run Sublist3r
sublist3r -d $DOMAIN -v -o domains.txt

# Run Assetfinder
~/go/bin/assetfinder --subs-only $DOMAIN | tee -a domains.txt

# Remove duplicates
sort -u domains.txt -o domains.txt

# Probe for alive domains
echo "\n\n[+] Checking for alive domains...\n"
cat domains.txt | ~/go/bin/httprobe | tee -a alive.txt

# Convert to JSON
cat alive.txt | python -c "import sys; import json; print(json.dumps({'domains':list(sys.stdin)}))" > alive.json
cat domains.txt | python -c "import sys; import json; print(json.dumps({'domains':list(sys.stdin)}))" > domains.json
```
---

```bash
Usage:
chmod +x enum.sh
./enum.sh example.com
```
---

Output Files:

domains.txt / domains.json: Raw subdomains.

alive.txt / alive.json: Verified active subdomains.

---

Step 2: Data Collection
2.1 Store Headers and Response Bodies
Script: response.sh
```bash
#!/bin/bash
mkdir headers responsebody

for domain in $(cat $1); do
    NAME=$(echo $domain | awk -F/ '{print $3}')
    curl -X GET -H "X-Forwarded-For: evil.com" $domain -I > "headers/$NAME"
    curl -s -X GET -H "X-Forwarded-For: evil.com" -L $domain > "responsebody/$NAME"
done
```

---

Usage:
```bash
chmod +x response.sh
./response.sh alive.txt
```

---

2.2 Extract JavaScript Files
Script: jsfiles.sh
```bash

#!/bin/bash
mkdir scripts scriptsresponse

for domain in $(ls responsebody); do
    ENDPOINTS=$(cat "responsebody/$domain" | grep -Eoi "src=\"[^>]+></script>" | cut -d '"' -f 2)
    for endpoint in $ENDPOINTS; do
        if [[ $endpoint == http* ]]; then
            URL=$endpoint
        else
            URL="https://$domain$endpoint"
        fi
        FILENAME=$(basename $endpoint)
        curl -s $URL -L > "scriptsresponse/$domain/$FILENAME"
        echo $URL >> "scripts/$domain"
    done
done
```

---

2.3 Find Hidden Endpoints in JS Files
Tool: relative-url-extractor

Script: endpoints.sh
```bash
#!/bin/bash
mkdir endpoints

for domain in $(ls scriptsresponse); do
    mkdir "endpoints/$domain"
    for file in $(ls "scriptsresponse/$domain"); do
        ruby ~/relative-url-extractor/extract.rb "scriptsresponse/$domain/$file" >> "endpoints/$domain/$file"
    done
done
```

---

2.4 Port Scanning with Nmap
Script: nmap.sh
```bash
#!/bin/bash
mkdir nmapscans

for domain in $(cat $1); do
    nmap -sC -sV $domain | tee "nmapscans/$domain"
done
```

---

Usage:
```bash
./nmap.sh domains.txt
```

2.5 Screenshotting with Aquatone
```bash
cat alive.txt | aquatone -out ~/example.com/screenshots/
```

---

Step 3: Data Processing
Search Script: search.sh
```bash
#!/bin/bash
BOLD="\033[1m"
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

searchhtml() {
    for domain in $(ls responsebody); do
        echo -e "${BOLD}${GREEN}Scanning $domain...${RESET}"
        grep -Hn "$1" "responsebody/$domain"
    done
}

searchheader() {
    for domain in $(ls headers); do
        echo -e "${BOLD}${GREEN}Scanning $domain headers...${RESET}"
        grep -Hn "$1" "headers/$domain"
    done
}

searchjs() {
    for domain in $(ls scriptsresponse); do
        for file in $(ls "scriptsresponse/$domain"); do
            echo -e "${BOLD}${GREEN}Scanning $domain/$file...${RESET}"
            grep -Hn "$1" "scriptsresponse/$domain/$file"
        done
    done
}

searchnmap() {
    for domain in $(ls nmapscans); do
        echo -e "${BOLD}${GREEN}Scanning $domain nmap results...${RESET}"
        grep -Hn "$1" "nmapscans/$domain"
    done
}

# Parse command-line options
case "$1" in
    -j) searchjs "$2" ;;
    -x) searchheader "$2" ;;
    -e) searchhtml "$2" ;;
    -n) searchnmap "$2" ;;
    *) echo "Usage: ./search.sh [-j|-x|-e|-n] [search_term]" ;;
esac
```
Usage:
```bash
./search.sh -j "api-key"      # Search JS files
./search.sh -x "nginx"        # Search headers
./search.sh -e "s3.amazonaws" # Search HTML
./search.sh -n "ssh"          # Search Nmap results
```

---

End Notes
Recon is Iterative: The more data you collect, the more attack vectors you uncover.

Enhance Scripts: Add tools like Amass or Waybackurls for deeper insights.

Automate S3 Checks: Use tools like AWS CLI to test for open buckets.

Fun Fact: While writing this guide, two information disclosure vulnerabilities were discovered using this methodology.
Happy Hunting! 🕵️♂️
