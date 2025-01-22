import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['figure.figsize'] = [10, 6]  # Reduced size for better fit
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.75  # Increased padding
plt.rcParams.update({'figure.autolayout': True})  # Enable automatic layout

# Create directory for saving plots
import os
os.makedirs('visualization_drafts', exist_ok=True)

# Read the dataset
df = pd.read_excel('titanic3.xls')

# 1. Passenger Class and Survival Rate
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='pclass', y='survived', data=df, palette='deep')
plt.title('Survival Rate by Passenger Class', pad=20)
plt.xlabel('Passenger Class (1 = First, 2 = Second, 3 = Third)')
plt.ylabel('Survival Rate')

# Add percentage labels on bars
survival_rates = df.groupby('pclass')['survived'].mean() * 100
for i, rate in enumerate(survival_rates):
    ax.text(i, rate/100, f'{rate:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visualization_drafts/class_survival.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. Age and Survival
plt.figure(figsize=(10, 6))
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

print("Visualization drafts have been created in the visualization_drafts directory.")
