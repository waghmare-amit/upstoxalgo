from .imports_and_instrument_token import *

def upstox_login(creds):
    client_id = creds["auth"]["client_id"]
    client_pass = creds["auth"]["client_pass"]
    client_pin = creds["auth"]["client_pin"]
    api_key = creds["auth"]["api_key"]
    api_secret = creds["auth"]["api_secret"]
    redirect_uri = creds["auth"]["redirect_uri"]

    login_url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={api_key}&redirect_uri={redirect_uri}"

    print(f"Visit this url: {login_url}. Then, paste the code from the redirected browser.")

    try:
        auth_code = input("Paste the code from the redirected browser here: ").strip()
    except Exception as e:
        print(f"Error reading input: {e}")
        return creds
    
    url = "https://api.upstox.com/v2/login/authorization/token"
    
    #Request headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    #Request data
    data = {
        'code': auth_code,
        'client_id': api_key,
        'client_secret': api_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    #Make the POST request
    response = requests.post(url, headers=headers, data=data)
    
    #Check the response 
    if response.status_code == 200:
        #Request was successful
        print("Access Token:", response.json().get('access_token'))
        creds["auth"]["access_token"] = response.json().get('access_token')
        creds["api"]["headers"] = {
                                    'accept': 'application/json',
                                    'Api-Version': '2.0',
                                    'Authorization': f'Bearer {creds["auth"]["access_token"]}'
                                }
        print("Logged in : " + creds["auth"]["client_id"])
    else:
        #Request failed
        print("Error:", response.status_code, response.text)
        print("Unable to Log in : " + creds["auth"]["client_id"])

    creds["api"]["last_updated"] = str(datetime.datetime.now().strftime('%H:%M:%S'))
    creds["api"]["last_function"] = "login"
    return creds
    
def upstox_auth(creds):
    response = None
    try:
        headers = creds.get("api", {}).get("headers", None)
        if not headers:
            raise KeyError("Missing 'headers' in creds['api'] — call upstox_login() first")
        
        url = "https://api.upstox.com/v2/user/profile"
        
        #Make the GET request
        response = requests.get(url, headers = headers)
        
        #Check the response
        if response.status_code == 200:
            #Request was successful
            json_data = response.json()
            if json_data.get("status") == "success":
                print("Authentication Successful: " + creds["auth"]["client_id"])
                return creds
            else:
                #Request failed
                print("Auth API returned error status")
                raise KeyError("Auth API returned error status")
        else:
            print("Authentication Failed: " + creds["auth"]["client_id"])
            raise KeyError
            
    except(ValueError, KeyError) as e:
        logging.critical("Auth API Failed:" + str(e))
        if response:
            try:
                logging.critical("Status Code: %s", response.status_code)
                logging.critical("Response Text: %s", response.text)
                logging.critical("Curlify Request: %s", curlify.to_curl(response.request))
            except Exception as curl_err:
                logging.critical("Curlify failed: %s", curl_err)
        print("Retrying login for: " + creds["auth"]["client_id"])
        return upstox_login(creds)

def upstox_margin(creds):
    response = None
    json_data = None
    try:
        url = "https://api.upstox.com/v2/user/get-funds-and-margin"
        
        #Make the GET request
        response = requests.get(url, headers = creds["api"]["headers"])
        
        #Check the response
        if response.status_code == 200:
            #Request was successful
            json_data = response.json()
            if json_data["status"] == "success":
                creds["api"]["margin"] = json_data["data"]
            else:
                #Request failed
                print("Status Failed")
                raise KeyError
        else:
            url = "https://api.upstox.com/v2/user/profile"
            response = requests.get(url, headers = creds["api"]["headers"])
            if response.status_code != 200:
                print(f"Failed to retrieve data. Status Code: {response.status_code}")
                raise KeyError
            else:
                #Upstox is down in Margin API but rest everything is working.
                return creds
                
    except(ValueError, KeyError):
        logging.critical("Errors in Margin Module: " + creds["auth"]["client_id"])
        logging.critical(json_data)
        logging.critical("Curlify Data...")
        logging.critical(curlify.to_curl(response.request))
        print(response)

    creds["api"]["last_updated"] = str(datetime.datetime.now().strftime('%H:%M:%S'))
    creds["api"]["last_function"] = "margin"
    return creds

def upstox_positions(creds):
    response = None
    json_data = None
    try:
        url = "https://api.upstox.com/v2/portfolio/short-term-positions"
        
        #Make the GET request
        response = requests.get(url, headers = creds["api"]["headers"])
        
        #Check the response
        if response.status_code == 200:
            #Request was successful
            json_data = response.json()
            if json_data["status"] == "success":
                creds["api"]["positions"] = json_data["data"]
            else:
                #Request failed
                print("Status Failed")
                raise KeyError
        else:
            url = "https://api.upstox.com/v2/user/profile"
            response = requests.get(url, headers = creds["api"]["headers"])
            if response.status_code != 200:
                print(f"Failed to retrieve data. Status Code: {response.status_code}")
                raise KeyError
            else:
                #Upstox is down in Position API but rest everything is working.
                return creds
                
    except(ValueError, KeyError):
        logging.critical("Errors in Position Module: " + creds["auth"]["client_id"])
        logging.critical(json_data)
        logging.critical("Curlify Data...")
        logging.critical(curlify.to_curl(response.request))
        print(response)

    creds["api"]["last_updated"] = str(datetime.datetime.now().strftime('%H:%M:%S'))
    creds["api"]["last_function"] = "postions"
    return creds
