import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import os

# Set style for high-quality visualizations
plt.style.use('seaborn-v0_8-white')  # Use white style without grid
sns.set_theme(style="white", font_scale=1.2)  # Clean style without grid
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.75
plt.rcParams['axes.grid'] = False  # Explicitly disable grid
plt.rcParams['axes.spines.top'] = False  # Remove top spine
plt.rcParams['axes.spines.right'] = False  # Remove right spine

# Create directory for enhanced visualizations
os.makedirs('enhanced_analysis_outputs', exist_ok=True)

# Read and preprocess the dataset
df = pd.read_excel('titanic3.xls')

# 1. Enhanced Survival by Port Analysis
plt.figure(figsize=(10, 6))
port_survival = df.groupby('embarked')['survived'].agg(['mean', 'count', 'std']).reset_index()
port_survival['mean'] *= 100
port_survival['std'] *= 100

# Calculate confidence intervals
confidence = 0.95
port_survival['ci'] = stats.t.ppf((1 + confidence) / 2, port_survival['count'] - 1) * \
                     port_survival['std'] / np.sqrt(port_survival['count'])

ax = sns.barplot(data=port_survival, x='embarked', y='mean',
                color='skyblue', alpha=0.8)

# Add error bars for confidence intervals
plt.errorbar(x=range(len(port_survival)), y=port_survival['mean'],
            yerr=port_survival['ci'], fmt='none', color='black', capsize=5)

# Add value labels
for i, row in enumerate(port_survival.itertuples()):
    mean_val = port_survival['mean'].iloc[i]
    count_val = port_survival['count'].iloc[i]
    ax.text(i, mean_val + 1, f'{mean_val:.1f}%\n(n={count_val:d})',
            ha='center', va='bottom')

plt.title('Survival Rate by Port of Embarkation with 95% CI', pad=20)
plt.xlabel('Port (C=Cherbourg, Q=Queenstown, S=Southampton)')
plt.ylabel('Survival Rate (%)')
plt.savefig('enhanced_analysis_outputs/port_survival.png')
plt.close()

# 2. Family Size Analysis
df['family_size'] = df['sibsp'] + df['parch'] + 1
plt.figure(figsize=(10, 6))

family_survival = df.groupby('family_size')['survived'].agg(['mean', 'count', 'std']).reset_index()
family_survival['mean'] *= 100
family_survival['std'] *= 100

# Calculate confidence intervals
family_survival['ci'] = stats.t.ppf((1 + confidence) / 2, family_survival['count'] - 1) * \
                       family_survival['std'] / np.sqrt(family_survival['count'])

ax = sns.barplot(data=family_survival, x='family_size', y='mean',
                color='lightgreen', alpha=0.8)

plt.errorbar(x=range(len(family_survival)), y=family_survival['mean'],
            yerr=family_survival['ci'], fmt='none', color='black', capsize=5)

for i, row in enumerate(family_survival.itertuples()):
    count_val = family_survival['count'].iloc[i]
    if count_val >= 10:  # Only show labels for groups with sufficient data
        mean_val = family_survival['mean'].iloc[i]
        ax.text(i, mean_val + 1, f'{mean_val:.1f}%\n(n={count_val:d})',
                ha='center', va='bottom')

plt.title('Survival Rate by Family Size with 95% CI', pad=20)
plt.xlabel('Family Size (including self)')
plt.ylabel('Survival Rate (%)')
plt.savefig('enhanced_analysis_outputs/family_survival.png')
plt.close()

# 3. Age Group Analysis with Class Breakdown
age_bins = [0, 12, 20, 30, 40, 50, 60, 100]
age_labels = ['0-12', '13-20', '21-30', '31-40', '41-50', '51-60', '60+']
df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

plt.figure(figsize=(12, 7))
age_class_survival = df.groupby(['age_group', 'pclass'])['survived'].mean().unstack() * 100

ax = age_class_survival.plot(kind='bar', width=0.8)
plt.title('Survival Rate by Age Group and Class', pad=20)
plt.xlabel('Age Group')
plt.ylabel('Survival Rate (%)')
plt.legend(title='Passenger Class', title_fontsize=10)
# Add value labels
values = age_class_survival.to_numpy()
for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        value = values[i, j]
        if not np.isnan(value):
            ax.text(i, value + 1, f'{value:.1f}%',
                   ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('enhanced_analysis_outputs/age_class_survival.png')
plt.close()

# 4. Advanced Machine Learning Analysis
# Prepare features for ML
features = ['pclass', 'age', 'fare', 'sibsp', 'parch']
X = df[features].copy()
y = df['survived']

# Handle missing values
X = X.fillna(X.mean())

# Add engineered features
X['family_size'] = df['sibsp'] + df['parch'] + 1
X['is_alone'] = (X['family_size'] == 1).astype(int)
X['fare_per_person'] = df['fare'] / X['family_size']

# Add gender
X['is_female'] = (df['sex'] == 'female').astype(int)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

# Train Random Forest with cross-validation
rf = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(rf, X_scaled, y, cv=5)

# Get feature importance
rf.fit(X_scaled, y)
importance = pd.DataFrame({
    'feature': X_scaled.columns,
    'importance': rf.feature_importances_
})
importance = importance.sort_values('importance', ascending=False)

# Plot feature importance with confidence intervals
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='importance', y='feature', data=importance,
                palette='viridis')

plt.title('Feature Importance in Survival Prediction\nCV Accuracy: {:.1f}% ± {:.1f}%'.format(
    cv_scores.mean() * 100, cv_scores.std() * 100 * 2))
plt.xlabel('Relative Importance')
plt.ylabel('Feature')

# Add value labels
for i, v in enumerate(importance['importance']):
    ax.text(v, i, f'{v:.3f}', va='center')

plt.tight_layout()
plt.savefig('enhanced_analysis_outputs/advanced_feature_importance.png')
plt.close()

# 5. Survival Probability Surface Plot
plt.figure(figsize=(12, 8))
fare_bins = pd.qcut(df['fare'], q=10, labels=False)
age_bins_simple = pd.qcut(df['age'], q=10, labels=False)

survival_matrix = df.groupby([age_bins_simple, fare_bins])['survived'].mean().unstack() * 100

plt.imshow(survival_matrix, cmap='RdYlBu', aspect='auto')
plt.colorbar(label='Survival Rate (%)')
plt.title('Survival Rate by Age and Fare Percentiles', pad=20)
plt.xlabel('Fare Percentile (0=Lowest, 9=Highest)')
plt.ylabel('Age Percentile (0=Youngest, 9=Oldest)')

# Add text annotations for survival rates
for i in range(survival_matrix.shape[0]):
    for j in range(survival_matrix.shape[1]):
        plt.text(j, i, f'{survival_matrix.iloc[i, j]:.1f}%',
                ha='center', va='center', color='black',
                fontsize=8)

plt.tight_layout()
plt.savefig('enhanced_analysis_outputs/survival_surface.png')
plt.close()

print("Enhanced analysis visualizations have been created in the 'enhanced_analysis_outputs' directory.")

# Save statistical summary
statistical_summary = pd.DataFrame({
    'Metric': [
        'Overall Survival Rate',
        'Female Survival Rate',
        'Male Survival Rate',
        'Child Survival Rate (0-12)',
        'First Class Survival Rate',
        'Second Class Survival Rate',
        'Third Class Survival Rate',
        'Average Age',
        'Median Fare',
        'Family Size Average',
        'Cross-Validation Accuracy'
    ],
    'Value': [
        f"{df['survived'].mean()*100:.1f}%",
        f"{df[df['sex']=='female']['survived'].mean()*100:.1f}%",
        f"{df[df['sex']=='male']['survived'].mean()*100:.1f}%",
        f"{df[df['age']<=12]['survived'].mean()*100:.1f}%",
        f"{df[df['pclass']==1]['survived'].mean()*100:.1f}%",
        f"{df[df['pclass']==2]['survived'].mean()*100:.1f}%",
        f"{df[df['pclass']==3]['survived'].mean()*100:.1f}%",
        f"{df['age'].mean():.1f} years",
        f"£{df['fare'].median():.2f}",
        f"{df['family_size'].mean():.1f}",
        f"{cv_scores.mean()*100:.1f}% ± {cv_scores.std()*100*2:.1f}%"
    ]
})

statistical_summary.to_csv('enhanced_analysis_outputs/statistical_summary.csv', index=False)
