import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style and figure parameters for high-quality visualizations
plt.style.use('seaborn-v0_8-white')  # Use white style without grid
sns.set_theme(style="white", font_scale=1.1)  # Clean style without grid
plt.rcParams['figure.figsize'] = [12, 7]  # Increased figure size
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 1.0  # Further increased padding
plt.rcParams['figure.constrained_layout.use'] = True  # Better layout handling
plt.rcParams['figure.autolayout'] = False  # Disable autolayout in favor of constrained_layout
plt.rcParams['axes.labelpad'] = 10  # Add padding to axis labels
plt.rcParams['figure.subplot.top'] = 0.95  # Adjust top margin
plt.rcParams['figure.subplot.bottom'] = 0.15  # Adjust bottom margin
plt.rcParams['figure.subplot.left'] = 0.15  # Adjust left margin
plt.rcParams['figure.subplot.right'] = 0.95  # Adjust right margin
plt.rcParams['axes.grid'] = False  # Explicitly disable grid
plt.rcParams['axes.spines.top'] = False  # Remove top spine
plt.rcParams['axes.spines.right'] = False  # Remove right spine

# Create directory for visualizations
import os
os.makedirs('visualization_outputs', exist_ok=True)

# Read the dataset
df = pd.read_excel('titanic3.xls')

# 1. Enhanced Survival Rate by Class
plt.figure(figsize=(10, 6))
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
plt.savefig('visualization_outputs/survival_by_class.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. Age Distribution with Survival Overlay
plt.figure(figsize=(10, 6))
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
plt.savefig('visualization_outputs/age_distribution.png', bbox_inches='tight', dpi=300)
plt.close()

# 3. Gender and Class Combined Analysis
plt.figure(figsize=(10, 6))
survival_by_gender_class = df.groupby(['sex', 'pclass'])['survived'].mean().unstack() * 100

ax = survival_by_gender_class.plot(kind='bar', width=0.8)
plt.title('Survival Rate by Gender and Class', pad=20, fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Survival Rate (%)', fontsize=12)
plt.legend(title='Passenger Class', title_fontsize=12)

# Add value labels
for i, (idx, row) in enumerate(survival_by_gender_class.iterrows()):
    for j, value in enumerate(row):
        ax.text(i, value + 2, f'{value:.1f}%', 
                ha='center', va='bottom')

plt.tight_layout()
plt.savefig('visualization_outputs/gender_class_survival.png', bbox_inches='tight', dpi=300)
plt.close()

print("Enhanced visualizations have been created in the 'visualization_outputs' directory.")
