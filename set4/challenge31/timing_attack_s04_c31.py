import requests


hmac_guess = 'A'*40
j = 0
time_elapsed = {}
for j in range(40):
    time_elapsed = {}
    for k in range(1):
        for i in range(47,123):
            hmac_guess = list(hmac_guess)
            hmac_guess[j] = chr(i)
            hmac_guess = ''.join(hmac_guess)
            payload = {'file': 'hello.txt', 'signature': hmac_guess}
            r = requests.get("http://localhost:8080/test", params = payload)
            ms_delay = r.elapsed.total_seconds()*1000
            if k == 0: 
                time_elapsed[chr(i)] = (ms_delay)
            else:
                time_elapsed[chr(i)] += (ms_delay)
    hmac_at_j = max(time_elapsed, key=time_elapsed.get)
    hmac_guess = list(hmac_guess)
    hmac_guess[j] = hmac_at_j
    hmac_guess = ''.join(hmac_guess)
    j = j + 1
print(hmac_guess)


