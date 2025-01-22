import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style and figure parameters for high-quality visualizations
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['figure.figsize'] = [10, 6]  # Reduced size for better fit
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.75  # Increased padding
plt.rcParams.update({'figure.autolayout': True})  # Enable automatic layout

# Create directory for visualizations
import os
os.makedirs('visualization_outputs', exist_ok=True)

# Read the dataset
df = pd.read_excel('attachments/083d2ec1-9bbf-4f94-bfec-ec6ea70df661/titanic3.xls')

# 1. Enhanced Survival Rate by Class
plt.figure(figsize=(12, 8))
survival_by_class = df.groupby('pclass')['survived'].agg(['mean', 'count']).reset_index()
survival_by_class['mean'] *= 100

ax = sns.barplot(data=survival_by_class, x='pclass', y='mean',
                hue='pclass', palette='deep', alpha=0.8, legend=False)

# Add value labels on bars
for i, v in enumerate(survival_by_class['mean']):
    ax.text(i, v + 1, f'{v:.1f}%\n(n={survival_by_class["count"][i]})', 
            ha='center', va='bottom')

plt.title('Survival Rate by Passenger Class', pad=20, fontsize=16)
plt.xlabel('Passenger Class (1 = First, 2 = Second, 3 = Third)', fontsize=12)
plt.ylabel('Survival Rate (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig('visualization_outputs/survival_by_class.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. Age Distribution with Survival Overlay
plt.figure(figsize=(12, 8))
sns.kdeplot(data=df, x='age', hue='survived',
            hue_order=[0, 1],
            multiple="layer",
            fill=True, alpha=0.5,
            palette=['red', 'green'],
            common_norm=False)

plt.title('Age Distribution by Survival Status', pad=20, fontsize=16)
plt.legend(title='Survival Status',
          labels=['Did Not Survive', 'Survived'])
plt.xlabel('Age (Years)', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend(title='Survival Status', title_fontsize=12, fontsize=10)
plt.grid(True, alpha=0.3)
plt.savefig('visualization_outputs/age_distribution.png', bbox_inches='tight', dpi=300)
plt.close()

# 3. Gender and Class Combined Analysis
plt.figure(figsize=(12, 8))
survival_by_gender_class = df.groupby(['sex', 'pclass'])['survived'].mean().unstack() * 100

ax = survival_by_gender_class.plot(kind='bar', width=0.8)
plt.title('Survival Rate by Gender and Class', pad=20, fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Survival Rate (%)', fontsize=12)
plt.legend(title='Passenger Class', title_fontsize=12)
plt.grid(True, alpha=0.3)

# Add value labels
for i, (idx, row) in enumerate(survival_by_gender_class.iterrows()):
    for j, value in enumerate(row):
        ax.text(i, value + 2, f'{value:.1f}%', 
                ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visualization_outputs/gender_class_survival.png', bbox_inches='tight', dpi=300)
plt.close()

# 4. Fare Distribution Boxplot with Survival
plt.figure(figsize=(12, 8))
sns.boxplot(x='pclass', y='fare', hue='survived', data=df, 
            palette='Set2', showfliers=False)
plt.title('Fare Distribution by Class and Survival', pad=20, fontsize=16)
plt.xlabel('Passenger Class', fontsize=12)
plt.ylabel('Fare (£)', fontsize=12)
plt.legend(title='Survived', labels=['No', 'Yes'])
plt.grid(True, alpha=0.3)
plt.savefig('visualization_outputs/fare_distribution.png', bbox_inches='tight', dpi=300)
plt.close()

# 5. Age Group Survival Heatmap
age_bins = [0, 12, 20, 30, 40, 50, 60, 100]
df['age_group'] = pd.cut(df['age'], bins=age_bins, 
                        labels=['0-12', '13-20', '21-30', '31-40', '41-50', '51-60', '60+'])
survival_matrix = df.pivot_table(values='survived', 
                               index='pclass',
                               columns='age_group',
                               aggfunc='mean') * 100

plt.figure(figsize=(12, 8))
sns.heatmap(survival_matrix, annot=True, fmt='.1f', cmap='YlOrRd',
            cbar_kws={'label': 'Survival Rate (%)'},
            annot_kws={'size': 10})
plt.title('Survival Rate Heatmap: Class vs Age Group', pad=20, fontsize=16)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Passenger Class', fontsize=12)
plt.tight_layout()
plt.savefig('visualization_outputs/survival_heatmap.png', bbox_inches='tight', dpi=300)
plt.close()

# 6. Embarkation Port Analysis
plt.figure(figsize=(12, 8))
embarked_survival = df.groupby(['embarked'])['survived'].agg(['mean', 'count']).reset_index()
embarked_survival['mean'] *= 100

ax = sns.barplot(data=embarked_survival, x='embarked', y='mean',
                hue='embarked', palette='deep', alpha=0.8, legend=False)

# Add value labels
for i, v in enumerate(embarked_survival['mean']):
    ax.text(i, v + 1, f'{v:.1f}%\n(n={embarked_survival["count"][i]})',
            ha='center', va='bottom')

plt.title('Survival Rate by Port of Embarkation', pad=20, fontsize=16)
plt.xlabel('Port of Embarkation (C=Cherbourg, Q=Queenstown, S=Southampton)', fontsize=12)
plt.ylabel('Survival Rate (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig('visualization_outputs/embarkation_survival.png', bbox_inches='tight', dpi=300)
plt.close()

print("Enhanced visualizations have been created in the 'visualization_outputs' directory.")
