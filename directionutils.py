#import psycopg2
#conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
import sqlite3
from datetime import datetime,time
import json
import pygal
import googlemaps
from collections import OrderedDict
import keys

# connect and create sqlite tables
conn = sqlite3.connect('sth.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS SLB_USER(name text primary key,home_address text, office_address text)")
cur.execute("""CREATE TABLE IF NOT EXISTS SLB_TH(
                                id INTEGER primary key AUTOINCREMENT,
                                distance int,
                                status varchar(12),
                                duration int,
                                duration_in_traffic int,
                                time_of_day date,
                                direction varchar(12),
                                fk_slb_user text references SLB_USER(name))
""")


def save_user_data( name,
                    home_address,
                    office_address = "Schlumberger India Technology Center,Jail Press Road,Yerawada,Pune, Maharashtra, India"
                   ):
    insert_addr_sql = "INSERT INTO SLB_USER(name,home_address,office_address) VALUES('%s','%s','%s')" % (name,home_address,office_address)
    try:
        cur.execute(insert_addr_sql)
        conn.commit()
    except Exception as err:
        print("ERROR", err)


def save_traffic_data():


    now = datetime.now()

    # execute this only during working hours 0800-2200
    if now.time() >= time(8, 00) and  now.time() <= time(22, 00) and now.weekday() < 5: # or (now.time()  >= time(16,00) and now.time()  <= time(22,00) ):
        # Query and go through all the users data

        users = cur.execute("SELECT * FROM SLB_USER").fetchall()
        if len(users) == 0: return

        origins = []
        destinations = []
        for u in users:
            # to office
            origins.append(u[1])
            destinations.append(u[2])


            # This things breaks the code !!!

            # to home
            #origins.append(u[2])
            #destinations.append(u[1])


        #print(origins,"\n", destinations)
        # Query wiseowl api and get their distance
        try:
            gmaps = googlemaps.Client(key=keys.google_key)
            matrix = gmaps.distance_matrix(origins, destinations,
                                           mode="driving",
                                           language="en-AU",
                                           units="metric",
                                           departure_time=now,
                                           traffic_model="pessimistic",
                                           transit_routing_preference="fewer_transfers"

                                           )

        except Exception as e:
            print(e)
            return
        # save traffic data for each user
        results = matrix['rows']
        print(results)
        for r in results:
            print("--------------")
            print(users[results.index(r)][0])
            elem = r['elements'][0]
            distance = elem['distance']['value']
            status = elem['status']
            duration = elem['duration']['value']
            duration_in_traffic = elem['duration_in_traffic']['value']

            insert_sql = """
                INSERT INTO  SLB_TH(distance,status,duration,duration_in_traffic,time_of_day,fk_slb_user) VALUES(%s,'%s',%s,%s,'%s','%s')
            """ % (distance, status, duration, duration_in_traffic,now,users[results.index(r)][0])
            cur.execute(insert_sql)
            conn.commit()
    else:
        print("Not in time range")

def get_traffic_data(user_name):
    fetch_sql = "SELECT * FROM SLB_TH WHERE fk_slb_user = '%s' ORDER BY time_of_day DESC" % user_name
    result =  cur.execute(fetch_sql).fetchall()
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]

    arr = []
    for r in result:
        arr.append(dict(zip(field_names, r)))

    return arr

def get_traffic_data_for_today(user_name):
    fetch_sql = "SELECT * FROM SLB_TH WHERE fk_slb_user = '%s' ORDER BY time_of_day DESC LIMIT 1" % user_name
    result =  cur.execute(fetch_sql).fetchall()
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]

    arr = []
    for r in result:
        arr.append(dict(zip(field_names, r)))

    return arr

def get_avg_duration(user_name,direction='to_office'):
    # make buckets of 1 hours each, calculate avg duration
    if direction == 'to_office':
        fetch_sql = "SELECT time_of_day,duration_in_traffic FROM SLB_TH WHERE fk_slb_user = '%s' AND direction = '%s' ORDER BY time_of_day DESC" % (user_name,direction)
    else:
        fetch_sql = "SELECT time_of_day,duration_in_traffic FROM SLB_TH WHERE fk_slb_user = '%s' AND direction = '%s' ORDER BY time_of_day DESC" % (
        user_name, direction)

    result = cur.execute(fetch_sql).fetchall()
    avg_time = OrderedDict()

    for t in range(8, 22):
        time_bucket = []
        for r in result:
            time_of_day = datetime.strptime(r[0],"%Y-%m-%d %H:%M:%S.%f")
            if time_of_day.time() >= time(t, 00) and time_of_day.time() <= time(t+1, 00):
                time_bucket.append(r[1])

            t_str = str(t) + "-" + str(t + 1)

            if len(time_bucket) > 0 :
                avg_time[t_str] = sum(time_bucket)/len(time_bucket)/60
            else:
                avg_time[t_str] = 0


    return avg_time


def plot_bar_chart(data):
    line_chart = pygal.Line(width=600,height=300)
    line_chart.title = 'Average duration in traffic / hour'
    line_chart.x_labels = data.keys()
    #for k,v in data.items():
    line_chart.add("Duration", data.values())

    return line_chart.render()

if __name__ == '__main__':
    save_user_data("ranjan",'Kondhwa, Pune, Maharashtra 411048, India')
    #save_user_data("mayank", 'Kharadi, Pune, Maharashtra 411048, India')
    save_traffic_data()
    print(json.dumps(get_traffic_data('ranjan')))
    # print(json.dumps(get_traffic_data('mayank')))
    # print(json.dumps(get_traffic_data('nilesh')))
    # print(json.dumps(get_traffic_data('jaydeep')))
    #
    print(get_avg_duration('ranjan'))
    print(get_avg_duration('mayank'))
    print(get_avg_duration('nilesh'))
    print(get_avg_duration('jaydeep'))
    print(get_avg_duration('vijay'))





