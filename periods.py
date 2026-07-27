import json
from datetime import datetime, timedelta

class Periods():
  def log_period(self,user_id,date):
    with open("Data/periodsData.json") as filedata:
      data=json.load(filedata)
      if str(user_id) in data:
        data[str(user_id)].append(date)
      else:
        data[str(user_id)]=[date,]
    with open("Data/periodsData.json","w") as filedata:
      json.dump(data,filedata,indent=4)

  
  def next_period(self,user_id):
    CYCLE_LENGTH=28
    
    with open("Data/periodsData.json") as filedata:
      data=json.load(filedata)
      if str(user_id) in data:
        last = datetime.strptime(data[str(user_id)][-1], "%d-%m-%Y")
        next_period = last + timedelta(days=28)
        
        return next_period.strftime("%d-%m-%Y")
      return None


  def next_ovulation(self,user_id):
    try :
      period = datetime.strptime(self.next_period(user_id), "%d-%m-%Y")
      ovulation = period - timedelta(days=14)
      return ovulation.strftime("%d-%m-%Y")
    except Exception:
      return None

  def period_history(self,user_id):
    with open("Data/periodsData.json") as filedata:
      data=json.load(filedata)
      if str(user_id) in data:
        return data[str(user_id)]
      else:
        return None
    
        