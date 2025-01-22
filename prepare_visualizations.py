import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_excel('attachments/083d2ec1-9bbf-4f94-bfec-ec6ea70df661/titanic3.xls')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.5

# Create directory for saving plots
import os
os.makedirs('visualization_drafts', exist_ok=True)

# 1. Passenger Class and Survival Rate
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='pclass', y='survived', data=df, palette='deep')
plt.title('Survival Rate by Passenger Class', pad=20)
plt.xlabel('Passenger Class (1 = First, 2 = Second, 3 = Third)')
plt.ylabel('Survival Rate')

# Add percentage labels on bars
survival_rates = df.groupby('pclass')['survived'].mean() * 100
for i, rate in enumerate(survival_rates):
    ax.text(i, rate/100, f'{rate:.1f}%', ha='center', va='bottom')

# Add descriptive statistics
plt.figtext(0.02, 0.02, 
            f'Survival Rates:\n'
            f'First Class: {survival_rates[1]:.1f}%\n'
            f'Second Class: {survival_rates[2]:.1f}%\n'
            f'Third Class: {survival_rates[3]:.1f}%',
            fontsize=10, va='bottom')

plt.tight_layout()
plt.savefig('visualization_drafts/class_survival.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. Age and Survival
plt.figure(figsize=(12, 8))
# Create violin plot with box plot inside
ax = sns.violinplot(x='survived', y='age', data=df, inner='box', palette='deep')
plt.title('Age Distribution by Survival Status', pad=20)
plt.xlabel('Survival Status (0 = Did Not Survive, 1 = Survived)')
plt.ylabel('Age (Years)')

# Add statistical annotations
age_stats = df.groupby('survived')['age'].agg(['mean', 'std', 'count']).round(1)
for i, (survived, stats) in enumerate(age_stats.iterrows()):
    plt.text(i, df['age'].max() + 2,
             f'Mean Age: {stats["mean"]:.1f}\n'
             f'Std Dev: {stats["std"]:.1f}\n'
             f'Count: {stats["count"]:.0f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visualization_drafts/age_survival.png', bbox_inches='tight', dpi=300)
plt.close()

# 3. Gender and Survival
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='sex', y='survived', data=df, palette='deep')
plt.title('Survival Rate by Gender', pad=20)
plt.xlabel('Gender')
plt.ylabel('Survival Rate')

# Add percentage labels on bars
survival_by_gender = df.groupby('sex')['survived'].mean() * 100
for i, (gender, rate) in enumerate(survival_by_gender.items()):
    ax.text(i, rate/100, f'{rate:.1f}%', ha='center', va='bottom')

# Add count annotations
gender_counts = df.groupby(['sex', 'survived']).size().unstack()
for i, gender in enumerate(gender_counts.index):
    survived = gender_counts.loc[gender, 1]
    total = gender_counts.loc[gender].sum()
    plt.text(i, -0.1, 
             f'Survived: {survived:.0f}/{total:.0f}\n'
             f'({survived/total*100:.1f}%)',
             ha='center', va='top')

plt.tight_layout()
plt.savefig('visualization_drafts/gender_survival.png', bbox_inches='tight', dpi=300)
plt.close()

# 4. Fare and Class Distribution
plt.figure(figsize=(12, 8))
ax = sns.boxplot(x='pclass', y='fare', data=df, palette='deep')
plt.title('Fare Distribution by Passenger Class', pad=20)
plt.xlabel('Passenger Class (1 = First, 2 = Second, 3 = Third)')
plt.ylabel('Fare (£)')

# Add statistical annotations
fare_stats = df.groupby('pclass')['fare'].agg(['mean', 'median', 'std', 'count']).round(2)
for i, (pclass, stats) in enumerate(fare_stats.iterrows()):
    plt.text(i, df['fare'].max() * 1.1,
             f'Mean: £{stats["mean"]:.1f}\n'
             f'Median: £{stats["median"]:.1f}\n'
             f'Std Dev: £{stats["std"]:.1f}\n'
             f'Count: {stats["count"]:.0f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visualization_drafts/fare_class.png', bbox_inches='tight', dpi=300)
plt.close()

print("Visualization drafts have been created in the visualization_drafts directory.")
print("\nKey statistics for planning Tableau visualizations:")
print("\nSurvival rate by class:")
print(df.groupby('pclass')['survived'].mean())
print("\nSurvival rate by gender:")
print(df.groupby('sex')['survived'].mean())
print("\nAge statistics by survival:")
print(df.groupby('survived')['age'].describe())
print("\nFare statistics by class:")
print(df.groupby('pclass')['fare'].describe())
