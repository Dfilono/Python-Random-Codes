# names of hurricanes
names = ['Cuba I', 'San Felipe II Okeechobee', 'Bahamas', 'Cuba II', 'CubaBrownsville', 'Tampico', 'Labor Day', 'New England', 'Carol', 'Janet', 'Carla', 'Hattie', 'Beulah', 'Camille', 'Edith', 'Anita', 'David', 'Allen', 'Gilbert', 'Hugo', 'Andrew', 'Mitch', 'Isabel', 'Ivan', 'Emily', 'Katrina', 'Rita', 'Wilma', 'Dean', 'Felix', 'Matthew', 'Irma', 'Maria', 'Michael']

# months of hurricanes
months = ['October', 'September', 'September', 'November', 'August', 'September', 'September', 'September', 'September', 'September', 'September', 'October', 'September', 'August', 'September', 'September', 'August', 'August', 'September', 'September', 'August', 'October', 'September', 'September', 'July', 'August', 'September', 'October', 'August', 'September', 'October', 'September', 'September', 'October']

# years of hurricanes
years = [1924, 1928, 1932, 1932, 1933, 1933, 1935, 1938, 1953, 1955, 1961, 1961, 1967, 1969, 1971, 1977, 1979, 1980, 1988, 1989, 1992, 1998, 2003, 2004, 2005, 2005, 2005, 2005, 2007, 2007, 2016, 2017, 2017, 2018]

# maximum sustained winds (mph) of hurricanes
max_sustained_winds = [165, 160, 160, 175, 160, 160, 185, 160, 160, 175, 175, 160, 160, 175, 160, 175, 175, 190, 185, 160, 175, 180, 165, 165, 160, 175, 180, 185, 175, 175, 165, 180, 175, 160]

# areas affected by each hurricane
areas_affected = [['Central America', 'Mexico', 'Cuba', 'Florida', 'The Bahamas'], ['Lesser Antilles', 'The Bahamas', 'United States East Coast', 'Atlantic Canada'], ['The Bahamas', 'Northeastern United States'], ['Lesser Antilles', 'Jamaica', 'Cayman Islands', 'Cuba', 'The Bahamas', 'Bermuda'], ['The Bahamas', 'Cuba', 'Florida', 'Texas', 'Tamaulipas'], ['Jamaica', 'Yucatn Peninsula'], ['The Bahamas', 'Florida', 'Georgia', 'The Carolinas', 'Virginia'], ['Southeastern United States', 'Northeastern United States', 'Southwestern Quebec'], ['Bermuda', 'New England', 'Atlantic Canada'], ['Lesser Antilles', 'Central America'], ['Texas', 'Louisiana', 'Midwestern United States'], ['Central America'], ['The Caribbean', 'Mexico', 'Texas'], ['Cuba', 'United States Gulf Coast'], ['The Caribbean', 'Central America', 'Mexico', 'United States Gulf Coast'], ['Mexico'], ['The Caribbean', 'United States East coast'], ['The Caribbean', 'Yucatn Peninsula', 'Mexico', 'South Texas'], ['Jamaica', 'Venezuela', 'Central America', 'Hispaniola', 'Mexico'], ['The Caribbean', 'United States East Coast'], ['The Bahamas', 'Florida', 'United States Gulf Coast'], ['Central America', 'Yucatn Peninsula', 'South Florida'], ['Greater Antilles', 'Bahamas', 'Eastern United States', 'Ontario'], ['The Caribbean', 'Venezuela', 'United States Gulf Coast'], ['Windward Islands', 'Jamaica', 'Mexico', 'Texas'], ['Bahamas', 'United States Gulf Coast'], ['Cuba', 'United States Gulf Coast'], ['Greater Antilles', 'Central America', 'Florida'], ['The Caribbean', 'Central America'], ['Nicaragua', 'Honduras'], ['Antilles', 'Venezuela', 'Colombia', 'United States East Coast', 'Atlantic Canada'], ['Cape Verde', 'The Caribbean', 'British Virgin Islands', 'U.S. Virgin Islands', 'Cuba', 'Florida'], ['Lesser Antilles', 'Virgin Islands', 'Puerto Rico', 'Dominican Republic', 'Turks and Caicos Islands'], ['Central America', 'United States Gulf Coast (especially Florida Panhandle)']]

# damages (USD($)) of hurricanes
damages = ['Damages not recorded', '100M', 'Damages not recorded', '40M', '27.9M', '5M', 'Damages not recorded', '306M', '2M', '65.8M', '326M', '60.3M', '208M', '1.42B', '25.4M', 'Damages not recorded', '1.54B', '1.24B', '7.1B', '10B', '26.5B', '6.2B', '5.37B', '23.3B', '1.01B', '125B', '12B', '29.4B', '1.76B', '720M', '15.1B', '64.8B', '91.6B', '25.1B']

# deaths for each hurricane
deaths = [90,4000,16,3103,179,184,408,682,5,1023,43,319,688,259,37,11,2068,269,318,107,65,19325,51,124,17,1836,125,87,45,133,603,138,3057,74]

# 1
# Update Recorded Damages
conversion = {"M": 1000000,
              "B": 1000000000}

# test function by updating damages
def update_damages(damages, conversion):
  updated = []
  num = '0123456789'
  punc = ".,!:;"
  for i in damages:
    if i == "Damages not recorded":
      updated.append(i)
    else:
      if 'M' in i:
        new_int = float(i.strip('M'))
        new_int *= float(conversion['M'])
        updated.append(new_int)

      if 'B' in i:
        new_int = float(i.strip('B'))
        new_int *= float(conversion['B'])
        updated.append(new_int)

  return updated

damages = update_damages(damages, conversion)

# 2 
# Create a Table
def create_dict(name, month, year, winds, area, damages, deaths):
  combined = {}

  for i in range(len(name)):
    combined[name[i]] = {
      "Name" : name[i],
      "Month" : month[i],
      "Year" : year[i],
      'Max Sustained Winds' : winds[i],
      'Areas Affected' : area[i],
      'Damages' : damages[i],
      'Deaths' : deaths[i]
    } 

  return combined

hurricanes = create_dict(names, months, years, max_sustained_winds, areas_affected, damages, deaths)
# Create and view the hurricanes dictionary

# 3
# Organizing by Year
def organize_by_year(dictionary):
  new_dict = {}
  for i in dictionary:
    new_dict[dictionary[i]['Year']] = dictionary[i]

  return new_dict
  
sort_dict = organize_by_year(hurricanes)
# create a new dictionary of hurricanes with year and key


# 4
# Counting Damaged Areas
def count_areas(dictionary):
  new_dict = {}

  for i in dictionary:
    for area in dictionary[i]['Areas Affected']:
      if area not in new_dict:
        new_dict[area] = 1
      else:
        new_dict[area] += 1
    
  return new_dict

count = count_areas(hurricanes)
#print(count)

# create dictionary of areas to store the number of hurricanes involved in


# 5 
# Calculating Maximum Hurricane Count
def find_max(areas):
  max_area = ''
  max_hit = 0
  for i in areas:
    times_hit = areas[i]

    if times_hit > max_hit:
      max_area = i
      max_hit = times_hit

  return max_area, max_hit

max_area, max_hit = find_max(count)
#print(max_area)
#print(max_hit)

# find most frequently affected area and the number of hurricanes involved in


# 6
# Calculating the Deadliest Hurricane
def find_max_deaths(dictionary):
  max_deaths = 0
  deadliest = ''
  for i in dictionary:
    deaths = dictionary[i]['Deaths']

    if deaths > max_deaths:
      max_deaths = deaths
      deadliest = i

  return max_deaths, deadliest

max_deaths, deadliest = find_max_deaths(hurricanes)
#print(deadliest)
#print(max_deaths)
# find highest mortality hurricane and the number of deaths

# 7
# Rating Hurricanes by Mortality
def mortality_rating(dictionary):
  mortality_scale = {
    0: 0,
    1: 100,
    2: 500,
    3: 1000,
    4: 10000}

  new_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

  for i in dictionary:
    deaths = dictionary[i]["Deaths"]

    if deaths <= mortality_scale[0]:
      new_dict[0].append(i)
    
    elif mortality_scale[0] < deaths <= mortality_scale[1]:
      new_dict[1].append(i)

    elif mortality_scale[1] < deaths <= mortality_scale[2]:
      new_dict[2].append(i)

    elif mortality_scale[2] < deaths <= mortality_scale[3]:
      new_dict[3].append(i)

    elif mortality_scale[3] < deaths <= mortality_scale[4]:
      new_dict[4].append(i)

    elif mortality_scale[4] < deaths:
      new_dict[5].append(i)

  return new_dict

mortality = mortality_rating(hurricanes)
#print(mortality)

# categorize hurricanes in new dictionary with mortality severity as key


# 8 Calculating Hurricane Maximum Damage
def highest_cost(dictionary):
  max_cost = 0
  costly = ''
  for i in dictionary:
    cost = dictionary[i]['Damages']
    if cost == "Damages not recorded":
      continue
    else:
      if cost > max_cost:
        max_cost = cost
        costly = i

  return max_cost, costly

max_cost, costly = highest_cost(hurricanes)
#print(max_cost)
#print(costly)
# find highest damage inducing hurricane and its total cost


# 9
# Rating Hurricanes by Damage
def damage_rating(dictionary):
  damage_scale = {0: 0,
                  1: 100000000,
                  2: 1000000000,
                  3: 10000000000,
                  4: 50000000000}
  
  new_dict = {'Unrated': [], 0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

  for i in dictionary:
    cost = dictionary[i]["Damages"]

    if cost == "Damages not recorded":
      new_dict['Unrated'].append(i)
    elif cost <= damage_scale[0]:
      new_dict[0].append(i)
    elif damage_scale[0] < cost <= damage_scale[1]:
      new_dict[1].append(i)
    elif damage_scale[1] < cost <= damage_scale[2]:
      new_dict[2].append(i)
    elif damage_scale[2] < cost <= damage_scale[3]:
      new_dict[3].append(i)
    elif damage_scale[3] < cost <= damage_scale[4]:
      new_dict[4].append(i)
    elif damage_scale[4] < cost:
      new_dict[5].append(i)

  return new_dict

damage = damage_rating(hurricanes)
print(damage)
  
# categorize hurricanes in new dictionary with damage severity as key
