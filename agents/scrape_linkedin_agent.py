# Importations nécessaires


def scrape_linkedin(linkedin_url:str):
    json_cache = 'json_cache.json'
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    api_key = os.getenv('PROXYCURL_API')
    header_dic = {'Authorization': 'Bearer ' + api_key}
    params = {
        'linkedin_profile_url': linkedin_url,
        'use_cache': 'if-present',
    }

    ## Try to fetch data from local cache
    try:
        with open(json_cache, 'r') as f:
            cached_data = json.load(f)
            for entry in cached_data:
                if entry['linkedin_url'] == linkedin_url:
                    print('Fetched data from Local Cache')
                    return entry['response']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'No local cache found...({e})')
        cached_data = []
    
    # If data not found in cache, make an API call
    print('Fetching new json data... (updating local cache)')
    response = requests.get(api_endpoint,
                        params=params,
                        headers=header_dic)
    
    new_data = {
        'linkedin_url': linkedin_url,
        'response': response.json()
    }
    cached_data.append(new_data)
    
    # Update the local cache with new data
    with open(json_cache, 'w') as f:
        json.dump(cached_data, f,  indent=4)
    
    output = summarize(new_data['response'],'linkedin')

    return output

# Create the research function

