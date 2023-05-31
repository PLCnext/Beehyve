import requests
import os
import shutil
import datetime 
import pandas as pd

def create_download_folder():
    # replace phoenix with your windows user name
    path = r'C:\Users\phoenix\Downloads\beehyve_data'
    isExist = os.path.exists(path)
    if isExist:
        shutil.rmtree(path)
    os.makedirs(path)


def get_auth_token() -> str:
    #Send post request
    #Headers:
    header = {
        "Content-Type": "application/json"
    }
    #Payload:
    data =  {
        "username": 'beehyve@phoenixcontact.com',
        "password": 'Beehyve:2023!'
    }
    token_response = requests.post("https://tsd.proficloud.io/epts/token", json=data, headers=header)
    if token_response.ok:
        return token_response.json().get("access_token")
    else:
        return ''

def get_pc_data(access_token, uuid, metrics, fromDate, toDate) -> dict:
        
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    #Dates are ISO-8601!
    metrics = ','.join(metrics)
    #print(metrics)
    url = "https://tsd.proficloud.io/epts/data?uuid={}&timeSeriesName={}&fromDate={}&toDate={}".format(uuid, metrics, fromDate, toDate)

    result = requests.get(url, headers=header)
    if result.ok:
        return result.json()
    else:
        return {}
    


if __name__ == '__main__':

    create_download_folder()

    uuid = '84b02fbb-0eb6-4029-b781-554cd21e8b0e'
    metrics = ['auto~ambient_pressure_1',
                'auto~ambient_pressure_2',
                'auto~contact_temperature_sensor_1',
                'auto~contact_temperature_sensor_2',
                'auto~humidity_1',
                'auto~humidity_2',
                'auto~key_position',
                'auto~temperature_1',
                'auto~temperature_2',
                'auto~temperature_3',
                'auto~temperature_4',
                'auto~temperature_5',
                'auto~temperature_6',
                'auto~temperature_7',
                'auto~temperature_8',
                'auto~temperature_9',
                'auto~temperature_10',
                'auto~temperature_11',
                'auto~temperature_12',
                'auto~temperature_13',
                'auto~temperature_14',
                'auto~vibration_velocity_rms_1',
                'auto~vibration_velocity_rms_2',
                'auto~weight']
    
    fromDate = "2023-05-04T00:00:00.000Z"
    start_dt = datetime.datetime.strptime(fromDate, '%Y-%m-%dT%H:%M:%S.%fZ')

    auth_token = get_auth_token()

    for i in range(7):
        start = start_dt + datetime.timedelta(days=i)
        end =   start_dt + datetime.timedelta(days=i + 1)
        
        fromDate = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        toDate = end.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        pc_data = pd.DataFrame()

        if len(auth_token) > 0:
            data = get_pc_data(auth_token, uuid, metrics, fromDate, toDate)
            for sensor in data:
                name = list(sensor[uuid].keys())[0]
  
                ts = sensor[uuid][name]
                for i in range(len(ts)):
                    ts[i]['value'] = ts[i]['values']['value'] 
                    del ts[i]['values']
                df = pd.DataFrame(ts)
                df.rename(columns={'value': name[5:]}, inplace=True)

                if pc_data.shape[0] != 0:
                    if name[5:] in pc_data.columns:
                        pc_data = pd.concat([pc_data, df])
                    else:
                        pc_data = pc_data.merge(df, on='timestamp', how='outer')
                else:
                    pc_data = df
            
            pc_data = pc_data.groupby(['timestamp'], as_index=False).sum(min_count=1)
            pc_data.sort_values(by=['timestamp'], inplace=True)
            # replace phoenix with your windows user name
            pc_data.to_csv(r'C:\Users\phoenix\Downloads\beehyve_data\\' + fromDate[:10] + '.csv', index=False)

