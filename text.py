import boto3
#import PyMySQL
import pymysql
import os
from time import sleep

def phone_lookup():
    Dburl = os.environ['DBurl']
    DBusername = os.environ['DBusername']
    DBpassword = os.environ['DBpassword']
    DBname = os.environ['DBname']

    #userID = 3547
    # Open database connection
    connection = pymysql.connect(DBurl,DBusername,DBpassword,DBname )

    # prepare a cursor object using cursor() method
    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT phone_num from `users` WHERE `id` = (SELECT MAX(id) FROM users)"
            cursor.execute(sql)
            result = str(cursor.fetchone()[0])

            phone_num = (result)
    finally:
        connection.close()


    return(phone_num)
    sns_client = boto3.client('sns')
    phone_lookup()
def fire(picURL):
	sns_client = boto3.client('sns')
	phone = str(phone_lookup())


	response = sns_client.publish(

		PhoneNumber=phone,
    		Message='We detected an object of intrest please check the following url:'+picURL,
			 MessageAttributes={
    'AWS.SNS.SMS.SenderID': {
      'DataType': 'String',
      'StringValue': 'OpenGunAi'
    }
	}

    #TopicArn='string', (Optional - can't be used with PhoneNumer)
    #TargetArn='string', (Optional - can't be used with PhoneNumer)
    #Subject='string', (Optional - not used with PhoneNumer)
    #MessageStructure='string' (Optional)
	)




#fire()
