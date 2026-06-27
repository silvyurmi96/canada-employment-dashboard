import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
df = pd.read_csv("example_data.csv")

print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Date range: {df['month'].min()} to {df['month'].max()}")
print(f"Variables: {df['variable'].unique()}")
print(f"Sex categories: {df['sex'].unique()}")

provinces = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
             'Newfoundland and Labrador', 'Nova Scotia', 'Ontario',
             'Prince Edward Island', 'Quebec', 'Saskatchewan']

# check missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# 2019 employment by province - both sexes, total employment
latest = df[df['month'].str.startswith('2019') & 
            (df['variable'] == 'Employment') & 
            (df['sex'] == 'Both sexes')]

province_totals = latest[provinces].mean().sort_values(ascending=False)
print("\n2019 Employment by Province (thousands):")
print(province_totals.round(1))

# which province grew the most since 1976?
base1976 = df[df['month'].str.startswith('1976') & 
              (df['variable'] == 'Employment') & 
              (df['sex'] == 'Both sexes')][provinces].mean()

growth = ((province_totals - base1976) / base1976 * 100).round(1)
print("\nEmployment growth since 1976 (%):")
print(growth.sort_values(ascending=False))

# gender gap - Ontario 2019
ont_male = df[df['month'].str.startswith('2019') & 
              (df['variable'] == 'Employment') & 
              (df['sex'] == 'Males')]['Ontario'].mean()
ont_female = df[df['month'].str.startswith('2019') & 
                (df['variable'] == 'Employment') & 
                (df['sex'] == 'Females')]['Ontario'].mean()

print(f"\nOntario 2019 - Male: {round(ont_male)}K, Female: {round(ont_female)}K")
print(f"Gender gap: {round(ont_male - ont_female)}K")

# full time vs part time trend - Ontario
df['year'] = df['month'].str[:4]
yearly = df.groupby(['year', 'variable', 'sex'])[provinces].mean().reset_index()

ft = yearly[(yearly['variable'] == 'Full-time employment') & (yearly['sex'] == 'Both sexes')][['year', 'Ontario']]
pt = yearly[(yearly['variable'] == 'Part-time employment ') & (yearly['sex'] == 'Both sexes')][['year', 'Ontario']]

# chart 1 - 2019 employment by province
plt.figure(figsize=(10, 6))
province_totals.plot(kind='barh', color='#2b6cb0')
plt.title('Employment by Province in 2019 (thousands)')
plt.xlabel('Employment (thousands)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('province_employment_2019.png')
print("\nChart saved: province_employment_2019.png")

# chart 2 - Ontario employment over time
ontario_ts = yearly[(yearly['variable'] == 'Employment') & (yearly['sex'] == 'Both sexes')][['year', 'Ontario']]

plt.figure(figsize=(12, 5))
plt.plot(ontario_ts['year'], ontario_ts['Ontario'], color='#2b6cb0', linewidth=2)
plt.title('Ontario Employment Trend 1976-2019 (thousands)')
plt.xlabel('Year')
plt.ylabel('Employment (thousands)')
plt.xticks(ontario_ts['year'][::5], rotation=45)
plt.tight_layout()
plt.savefig('ontario_trend.png')
print("Chart saved: ontario_trend.png")

# chart 3 - full time vs part time Ontario
plt.figure(figsize=(12, 5))
plt.plot(ft['year'], ft['Ontario'], color='#276749', linewidth=2, label='Full-time')
plt.plot(pt['year'], pt['Ontario'], color='#d69e2e', linewidth=2, label='Part-time')
plt.title('Full-time vs Part-time Employment - Ontario (thousands)')
plt.xlabel('Year')
plt.ylabel('Employment (thousands)')
plt.legend()
plt.xticks(ft['year'][::5], rotation=45)
plt.tight_layout()
plt.savefig('fulltime_vs_parttime.png')
print("Chart saved: fulltime_vs_parttime.png")

print("\nAll done!")
