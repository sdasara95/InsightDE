# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:12:51 2019

@author: Satya
"""
import csv
import os
import datetime as dt
import copy

class Solver:
    def __init__(self, filename='../input/Border_Crossing_Entry_Data.csv', interested_columns=['Border','Date','Measure','Value']):
        self.filename = filename
        self.interested_columns = interested_columns
    
    def to_int(self, val):
        try:
            val = int(val)
            return val 
        except:
            return None
    
    def is_date(self,val):
        try:
            dt.datetime.strptime(val, '%m/%d/%Y %I:%M:%S %p')
            return True
        except:
            return False
            
    def read(self,filename=None):
        if filename==None:
            filename = self.filename
        else:
            self.filename = filename
        if len(filename) == 0:
            raise Exception('Empty File')
        if filename.endswith('.csv')==False:
            raise Exception('Not a CSV')
        if os.path.isfile(self.filename)==False:
            raise Exception('File does not exist!')
            
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            length_data = 0
            
            self.dataset = []
            for row in reader:
                
                if length_data==0:
                    keys = list(row.keys())
                    for i in self.interested_columns:
                        if i in keys:
                            pass
                        else:
                            raise Exception('Interested Columns not in the Data!')
                
                row_to_append = []
                valid_flag = 1
                
                for i in self.interested_columns:
                    if not row[i]=='':
                        if i=='Date' and not self.is_date(row[i]):
                                valid_flag = 0
                        
                        if i=='Value':
                            if not(self.to_int(row[i])==None):                       
                                row[i] = self.to_int(row[i])
                            else:
                                valid_flag = 0
                        row_to_append.append(row[i])
                    else:
                        valid_flag = 0
                
                if valid_flag:
                    self.dataset.extend([row_to_append])
                    length_data += 1
                else:
                    print(row_to_append)
            
            csvfile.close()
            
            if len(self.dataset)==0:
                raise Exception("Empty dataset! No valid rows!")
            print('Read Successful')
            print('Number of rows read is {}'.format(length_data))
    
    def process(self):
        data = self.dataset
        
        data_dict = {}
        for row in data:
            
            border,date,measure,value = row
            dt_list = dt.datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
            month = int(dt_list.month)
            year = int(dt_list.year)
            try:
                data_dict[border][measure][year][month]+=value
            except KeyError:
                data_dict.setdefault(border, {}).setdefault(measure, {}).setdefault(year, {})[month] = value
        
        self.data_dict = data_dict
    
    def get_unique(self,array):
        array = list(set(array))
        return array
        
    def get_all(self):
        all_borders = []
        all_measures = []
        all_years = []
        all_months = []
        
        d1 = self.data_dict
        
        for i in d1:
            all_borders.append(i)
            for j in d1[i]:
                all_measures.append(j)
                for k in d1[i][j]:
                    all_years.append(k)
                    for l in d1[i][j][k]:
                        all_months.append(l)
                        
        self.all_borders = self.get_unique(all_borders)
        self.all_measures = self.get_unique(all_measures)
        self.all_years = self.get_unique(all_years)
        self.all_months = self.get_unique(all_months)
        
    def solve(self):
        m_dict = copy.deepcopy(self.data_dict)
        d_dict = copy.deepcopy(self.data_dict)
        final_dict = copy.deepcopy(self.data_dict)
        
        for border in m_dict:
            for measure in m_dict[border]:
                month_count = 0
                years = m_dict[border][measure].keys()
                years = sorted(list(years))
                for year in years:
                    if not year==min(years):
                        prev_year_index = years.index(year)-1
                        prev_year = years[prev_year_index]
                    months = m_dict[border][measure][year].keys()
                    months = sorted(list(months))
                    for month in months:
                        month_count+=1
                        if month==min(months):
                            if year==min(years):
                                cumulative=0
                            else:
                                months_prev_year = m_dict[border][measure][prev_year].keys()
                                months_prev_year = sorted(list(months_prev_year))
                                max_month_prev_year = max(months_prev_year)
                                cumulative = m_dict[border][measure][prev_year][max_month_prev_year] + d_dict[border][measure][prev_year][max_month_prev_year]
                                
                        else:
                            prev_month_index = months.index(month)-1
                            prev_month = months[prev_month_index]
                            cumulative = m_dict[border][measure][year][prev_month] + d_dict[border][measure][year][prev_month]
                        
                        if cumulative>0:
                            denom = month_count - 1
                            avg = cumulative/denom
                        else:
                            avg = 0
                        
                        m_dict[border][measure][year][month] = cumulative
                        final_dict[border][measure][year][month] = round(avg+0.05)
                                               
        self.cum_dict = m_dict        
        self.mavg_dict = final_dict
    
    def write(self,output_path):
        self.get_all()
        borders = self.all_borders.copy()
        borders = sorted(borders,reverse=1)
        years = self.all_years.copy()
        years = sorted(years,reverse=1)
        measures = self.all_measures.copy()
        months = self.all_months.copy()
        months = sorted(months,reverse=1)
        
        mavg = copy.deepcopy(self.mavg_dict)
        ddict = copy.deepcopy(self.data_dict)
        
        with open(output_path,'w',newline='\n') as csvfile:
            fieldnames = ['Border','Date','Measure','Value','Average']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for year in years:
                for month in months:
                    for border in borders:
                        for measure in measures:
                            try:
                                val = ddict[border][measure][year][month]
                                avg = mavg[border][measure][year][month]
                            except KeyError:
                                continue
                            val= int(val)
                            avg = int(avg)
                            date_obj = dt.datetime(year, month, 1, hour=12, minute=0, second=0, microsecond=0)
                            date = date_obj.strftime("%m/%d/%Y %H:%M:%S")
                            date += ' AM'
                            
                            writer.writerow({'Border':border,'Date':date,'Measure':measure,'Value':val,'Average':avg})
                    
        csvfile.close()
        print('Written Successfully!')
            

#sum2 =0
#for year in d1['US-Canada Border']['Trains']:
#    for month in d1['US-Canada Border']['Trains'][year]:
#        sum2+=d1['US-Canada Border']['Trains'][year][month]
#print(sum1==sum2)


''' 
Just Sanity Check Code
US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0

obj = Solver()
obj.read()
obj.process()
obj.solve()

d1 = obj.data_dict        
sum1 = 0
for i in d1:
    for j in d1[i]:
        for k in d1[i][j]:
            for l in d1[i][j][k]:
                sum1+=d1[i][j][k][l]
print(sum1)
'''            
        
    

        
                            
                    
                
            
        
    