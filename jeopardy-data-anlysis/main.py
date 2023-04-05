import pandas as pd
pd.set_option('display.max_colwidth', -1)
df = pd.read_csv("jeopardy.csv")
print(df.columns)

df = df.rename(columns = {
  ' Air Date' : 'Air Date',
  ' Round' : 'Round',
  ' Category' : 'Category',
  ' Value' : 'Value',
  ' Question' : 'Question',
  ' Answer' : 'Answer'
})

print(df.columns)

def FindWords(words, data):
  filter = lambda x: all(word.lower() in x.lower() for word in words)
  found = data.loc[data["Question"].apply(filter)]
  found_num = len(found)
  return found, found_num

words = ["King", "England"]
found, num_found = FindWords(words, df)
print(num_found)
print(found["Question"])

convert_to_float = lambda x: float(x[1:].replace(',','')) if x!= "None" else 0

df['Float Values'] = df.Value.apply(convert_to_float)
print(df)

filtered, num_filtered = FindWords(["King"], df)
print(filtered)
avg_difficulty = filtered["Float Values"].mean()
print(avg_difficulty)

def unique_ans(data):
  return data["Answer"].value_counts()

print(unique_ans(filtered))
