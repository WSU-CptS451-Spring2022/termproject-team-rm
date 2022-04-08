#CptS 451 - Spring 2022
# httpswww.psycopg.orgdocsusage.html#query-parameters

#  if psycopg2 is not installed, install it using pip installer   pip install psycopg2  (or pip3 install psycopg2) 
import json
import psycopg2

def cleanStr4SQL(s)
    return s.replace(',`).replace(n, )

def int2BoolStr (value)
    if value == 0
        return 'False'
    else
        return 'True'

def insert2BusinessTable()
    with open('contentdriveMyDriveyelp_business.JSON','r') as f    #TODO update path for the input file
        #outfile =  open('.yelp_business_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0
        outfile =  open('.business.sql', 'w')
        # no numcheckin and numtips instead we have review_count
        while line            
            data = json.loads(line) 
            sql_str = (INSERT INTO business (business_id, business_name, address, business_state, city, postalcode, latitude, longitude, rating, review_count, is_open,numCheckins,numTips)
                       +  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, {10}, {11}, {12})).format(data['business_id'],cleanStr4SQL(data[name]), cleanStr4SQL(data[address]), data[state], data[city], data[postal_code], data[latitude], data[longitude], data[stars], data[review_count], [False,True][data[is_open]] ,0,0)            
            outfile.write(sql_str+ ';' +'n')
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()
def insertfriends(user_id,friends,outfile1)
  for friend in friends
    sql_str = (INSERT INTO Friends (yelp_user_id, friend_id)
    +  VALUES ('{0}', '{1}')).format(user_id,friend)
    outfile1.write(sql_str+ ';' +'n')

def insert2UserTable()
    with open('contentdriveMyDriveyelp_user.JSON','r') as f    #TODO update path for the input file
        #outfile =  open('.yelp_business_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0
        outfile =  open('.user.sql', 'w')
        outfile1 = open('.friends.sql', 'w')
        while line            
            data = json.loads(line) 
            sql_str = (INSERT INTO yelp_user (yelp_user_id, yelp_user_name, yelping_since, rating, cool_count, funny_count, fans_count, useful_count, tips_count,totalLikes,tipCount)
                       +  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8},{9},{10})).format(cleanStr4SQL(data['user_id']),cleanStr4SQL(data[name]), cleanStr4SQL(data[yelping_since]),str(data[average_stars]), str(data[cool]),str(data[funny]),str(data[fans]),str(data[useful]), str(data[tipcount]),0,0 )            
            outfile.write(sql_str+ ';' +'n')
            insertfriends(cleanStr4SQL(data['user_id']),data['friends'],outfile1)
            line = f.readline()
            count_line +=1
    print(User)
    print(count_line)
    outfile.close()
    outfile1.close()
    f.close()

def parseAttributes(dictionary, outfile,business_id)
    for key, value in dictionary.items()
      if isinstance(value, str)
        sql_str = (INSERT INTO business_attributes (business_id, attribute_name, attribute_value)
                       +  VALUES ('{0}', '{1}', '{2}')).format(business_id,key, value)
        outfile.write(sql_str+ ';' +'n') 
      else
        parseAttributes(value, outfile,business_id)

def processhoursdata(dictionary,outfile2,business_id)
  for day in dictionary.keys()
    opening_time, closing_time = dictionary[day].split('-')
    sql_str = (INSERT INTO business_hour (business_id, Week_day, opening_time,closing_time)
                       +  VALUES ('{0}', '{1}', '{2}','{3}')).format(business_id,day, opening_time,closing_time)
    outfile2.write(sql_str+ ';' +'n') 

def insertBusinessAttributesAndHours()
  with open('contentdriveMyDriveyelp_business.JSON','r') as f    #TODO update path for the input file
        line = f.readline()
        count_line = 0
        outfile =  open('.businessHours.sql', 'w')
        outfile2 =  open('.businessAttributes.sql', 'w')
        outfile3 =  open('.businessCategories.sql', 'w')
        while line
          data = json.loads(line)
          parseAttributes(data[attributes],outfile2,cleanStr4SQL(data['business_id']))
          processhoursdata(data[hours],outfile,cleanStr4SQL(data['business_id']))
          categories = data[categories].split(', ')
          for category in categories
            sql_str = (INSERT INTO business_category (business_id, category_name)
                       +  VALUES ('{0}', '{1}')).format(cleanStr4SQL(data['business_id']),category)
            outfile3.write(sql_str+ ';' +'n') 
          line = f.readline()
          count_line +=1
  print(count_line)
  outfile.close()
  outfile2.close()
  outfile3.close()
  f.close()

def insert2TipTable()
    with open('contentdriveMyDriveyelp_tip.JSON','r') as f    #TODO update path for the input file
        outfile =  open('.yelp_business_tip.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0
        while line            
            data = json.loads(line) 
            sql_str = (INSERT INTO tip (business_id, yelp_user_id, tip_date, tip_text, compliment_count)
                       +  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')).format(cleanStr4SQL(data['business_id']),cleanStr4SQL(data[user_id]),cleanStr4SQL(data[date]), cleanStr4SQL(data[text]), str(data[likes]))            
            outfile.write(sql_str+ ';' +'n')
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()

def insert2CheckinTable()
    with open('contentdriveMyDriveyelp_checkin.JSON','r') as f    #TODO update path for the input file
        outfile =  open('.yelp_checkin.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0
        while line            
            data = json.loads(line)
            Dates = data[date].split(',')
            #print(Dates)
            for date in Dates
              sql_str = (INSERT INTO checkin (business_id, checkin_date)
                       +  VALUES ('{0}', '{1}')).format(cleanStr4SQL(data['business_id']),date) + ;            
              outfile.write(sql_str+ ';' +'n')
            line = f.readline()
            count_line +=1
    outfile.close()
    f.close()


insert2BusinessTable()
insert2UserTable()
insertBusinessAttributesAndHours()
insert2TipTable()
insert2CheckinTable()