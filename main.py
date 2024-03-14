
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math
import seaborn as sns
import sklearn
from sklearn import linear_model
from sklearn import preprocessing
import statsmodels.api as sm
import pylab
import scipy.stats as stats
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn import ensemble
from sklearn.model_selection import cross_val_score

import seaborn as sns;

sns.set()
import sklearn
import warnings

warnings.filterwarnings("ignore")

"""# AIM: Calculating life expectancies of developing and developed

Now that you know that your aim is to predict the life expectancies by grouping the countires by the above groups.
You began by reading the file

# Reading file
"""

df = pd.read_csv('LifeExpectancyData.csv')
df.head()

"""Interpretation: We see that the data has been loaded properly"""

df.columns

pd.set_option('display.max_columns', None)
df.columns = ['Country', 'Year', 'Status', 'Life Expectancy', 'Adult Mortality',
              'Infant Deaths', 'Alcohol', 'Percent Expenditure', 'Hep B',
              'Measles', 'BMI', 'U-5 Deaths', 'Polio', 'Total Expenditure',
              'Diphtheria', 'HIVAIDS', 'GDP', 'Population', 'Thinness 10-19',
              'Thinness 5-9', 'Income Composition', 'Schooling']

df.head()

"""Interpretation: The required columns have been set

# Describing and cleaning data
"""

df.shape

"""Interpretation: The given dataframe has 2938 rows and 22 columns."""

df.isnull().sum(axis=0)

"""Interpretation: We see that there are a lot of empty fields. Now we need to cleanse this data to ensure that there is no empty field.

## Visualising missing data
"""

import missingno as msno

print(msno.matrix(df))
df.describe()

"""Interpretation: We see that this way is easier to visualise missing data"""

# Replace Missing Values Associated with Country Feature Mean
for column in df.columns:
    for i in range(len(df)):
        country = df['Country'][i]
        status = df['Country'][i]
        if (df[column].isnull()[i] == True):
            df[column][i] = df[df['Country'] == country][column].mean()
        else:
            pass
# Fill Unresolved Values by Status
# Check for missing values in 'Status' column
missing_status = df.isnull().sum()
if missing_status.sum() > 0:
    for column in missing_status.index:
        if missing_status[column] > 0:
            df[column].fillna(df[column].mean(), inplace=True)
else:
    df1 = df[df['Status'] == 'Developed']
    df2 = df[df['Status'] == 'Developing']

# df1 = df[(df['Status'] == 'Developed')].fillna(df[(df['Status'] == 'Developed')].mean())
# df2 = df[(df['Status'] == 'Developing')].fillna(df[(df['Status'] == 'Developing')].mean())
# df = df2.append(df1)

print(df.shape)
print(msno.matrix(df))

"""Interpretation: All the missing data has been cleaned, and there is no NULL/NAN values in any columm now."""

# deleting the null values
before_drop = df.shape[0]
df = df.dropna()
after_drop = df.shape[0]

df.head()

# Canada and France are mislabeled as Developing
df[df['Country'] == 'France']['Status'].replace('Developing', 'Developed')
df[df['Country'] == 'Canada']['Status'].replace('Developing', 'Developed')

"""Interpretation: France and Canada have been labelled as developed"""

df.info()

"""Interpretation:  We see that we have various types of data in our dataset, ranging from object to float type

# EDA - Exploratory Data Analysis
"""

# Filter out non-numeric columns
numeric_columns = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_columns.corr()
plt.figure(figsize=(12, 10))

# Generate the correlation heatmap
# sns.heatmap(numeric_columns.corr(), square=True, cmap='RdYlGn')
sns.heatmap(correlation_matrix, square=True, cmap='RdYlGn')

# sns.heatmap(df.corr(), square=True, cmap='RdYlGn')

df.describe()

"""# Life Expectancy and QQ plots"""

# Life Expectancy
sns.distplot(df['Life Expectancy'])
plt.axvline(df['Life Expectancy'].mean(), 0, .6, color='black')
plt.axvline(df['Life Expectancy'].mean() + df['Life Expectancy'].std(), 0, .45, color='black', linestyle='--')
plt.axvline(df['Life Expectancy'].mean() - df['Life Expectancy'].std(), 0, .45, color='black', linestyle='--')
plt.axvline(df['Life Expectancy'].mean() + 2 * df['Life Expectancy'].std(), 0, .30, color='black', linestyle='--')
plt.axvline(df['Life Expectancy'].mean() - 2 * df['Life Expectancy'].std(), 0, .30, color='black', linestyle='--')
plt.axvline(df['Life Expectancy'].mean() - 3 * df['Life Expectancy'].std(), 0, .15, color='black', linestyle='--')
sns.set(rc={'figure.figsize': (10, 10)})
plt.show()

# QQ plot
stats.probplot(df['Life Expectancy'], dist="norm", plot=plt)
plt.title('Life Expectancy QQ Plot')
plt.show()
print(stats.shapiro(df['Life Expectancy']))

# """Interpretation: The maximum value 89.0 is about 2.08 standard deviations away from the mean 69.2 while the minimum 36.3 is about 3.46 deviations away. The standard deviation for the whole sample is 9.50 years.Shapiro Wilk's p-value is more valid with over 5000 data points, but using the QQ plot and the Wilk statistic is trending close to normality.


# """

# Life Expectancy
sns.distplot(df[df['Status'] == 'Developed']['Life Expectancy'])
sns.distplot(df[df['Status'] == 'Developing']['Life Expectancy'], color='y')
labels = ['Developed', 'Developing']
plt.legend(labels=labels, bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
sns.set(rc={'figure.figsize': (10, 10)})
plt.show()

# QQ plot
stats.probplot(df[df['Status'] == 'Developed']['Life Expectancy'], dist="norm", plot=plt)
plt.title('Life Expectancy Developed Countries QQ Plot')
print(stats.shapiro(df['Life Expectancy']))
plt.show()
# QQ plot
stats.probplot(df[df['Status'] == 'Developing']['Life Expectancy'], dist="norm", plot=plt)
plt.title('Life Expectancy Developing Countries QQ Plot')
print(stats.shapiro(df['Life Expectancy']))
plt.show()

df['Life Expectancy'].groupby(df['Status']).describe()


def LEfactorplot(column):
    developed_data = df[df['Status'] == 'Developed']
    developing_data = df[df['Status'] == 'Developing']

    x_developed = developed_data[~developed_data[column].isnull()][column]
    y_developed = developed_data[~developed_data[column].isnull()]['Life Expectancy']
    x_developing = developing_data[~developing_data[column].isnull()][column]
    y_developing = developing_data[~developing_data[column].isnull()]['Life Expectancy']

    plt.scatter(x_developed, y_developed, alpha=0.7, label='Developed')
    plt.scatter(x_developing, y_developing, alpha=0.7, label='Developing')

    if len(x_developed) > 0 and len(y_developed) > 0:
        z1 = np.polyfit(x_developed, y_developed, 1)
        z1poly = np.poly1d(z1)
        plt.plot(x_developed, z1poly(x_developed), linewidth=2, color='blue')

    if len(x_developing) > 0 and len(y_developing) > 0:
        z2 = np.polyfit(x_developing, y_developing, 1)
        z2poly = np.poly1d(z2)
        plt.plot(x_developing, z2poly(x_developing), linewidth=2, color='orange')

    plt.xlabel(column)
    plt.ylabel('Life Expectancy')
    plt.legend()
    plt.show()


# Call the function for each column
for column in df.columns:
    if column not in ['Country', 'Status', 'Life Expectancy', 'world', 'Year']:
        LEfactorplot(column)

"""Interpretation: We see the difference in life expectancies of developing and developed countries through the LE factor plot we have made"""
# df = df.apply(pd.to_numeric, errors='coerce')

# Encode Country and Create copy of dataframe for regression
df_reg = df.copy()
from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df_reg["country_code"] = lb_make.fit_transform(df_reg["Country"])

# Binarize Status
df_reg['Status'] = np.where(df_reg['Status'] == 'Developing', 0, 1)

df_reg.columns

""""Interpretation`: All the countries have been encoded and the country status have been binarised to 0 and 1"""

# remove outliers
for col in df_reg.columns:
    if (col == 'world') or (col == 'Country'):
        pass
    else:
        df_reg = df_reg[np.abs(df_reg[col] - df_reg[col].mean()) <= (3 * df_reg[col].std())]

"""# Parameter """

# Full Training Set
X_train = df_reg[df_reg['Year'] < 2011].drop('Life Expectancy', axis=1)
Y_train = df_reg[df_reg['Year'] < 2011]['Life Expectancy']

# Full Testing Set
X_test = df_reg[df_reg['Year'] > 2011].drop('Life Expectancy', axis=1)
Y_test = df_reg[df_reg['Year'] > 2011]['Life Expectancy']

# Full Set
X = df_reg.drop('Life Expectancy', axis=1)
Y = df_reg['Life Expectancy']

# Breakdown
Xlist = [X_train, X_test]
Ylist = [Y_train, Y_test]
xlist = ['X_train', 'X_test']
status = ['Full Training', 'Full Testing']

df_reg['Life Expectancy'].describe()

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from pylab import rcParams

for x, y, i, z, s in zip(Xlist, Ylist, range(len(Xlist)), xlist, status):
    x = x.drop(['Country', 'Status', 'Infant Deaths', 'Thinness 10-19'], axis=1)
    x = scale(x)

    print('Linear Regression {}'.format(z))
    print(z, x.shape)
    # Model
    linear = LinearRegression()
    linear.fit(x, y)

    # R2
    R = linear.score(x, y)
    print('R^2 Score:{:0.4f}'.format(R))

    # Predictions
    Y_pred = linear.predict(x)
    RMSE = mean_squared_error(y, Y_pred) ** 0.5
    print('RMSE: {:0.3f}'.format(RMSE))
    print('Minimum LE: {:0.1f}'.format(Y_pred.min()))
    print('Maximum LE: {:0.1f}'.format(Y_pred.max()))
    print('Average Predicted LE: {:0.1f}'.format(Y_pred.mean()))
    print('LE Standard Deviation: {:0.3f}'.format(Y_pred.std()))
    print('LE Variance: {:0.3f}'.format(Y_pred.std() ** 2))

    # plot
    z1 = np.polyfit(Y_pred, y, 1)
    z1poly = np.poly1d(z1)
    plt.scatter(Y_pred, y, alpha=1)
    plt.plot(Y_pred, z1poly(Y_pred), linewidth=7.0, color='r')
    plt.title('Linear Regression {}'.format(z))
    plt.xlabel('Y_pred')
    plt.ylabel('Y')
    rcParams['figure.figsize'] = 10, 10
    plt.show()

    if i == 0:
        # Result DataFrame
        results = pd.DataFrame()
        results["Method"] = ['Linear']
        results['Set'] = z
        results['Status'] = s
        results['Datapoint Count'] = x.shape[0] * x.shape[1]
        results["RMSE"] = RMSE.round(2)
        results["R^2"] = R.round(2)
        results['LE Min'] = Y_pred.min().round(1)
        results['LE Max'] = Y_pred.max().round(1)
        results['Average LE'] = Y_pred.mean().round(1)
        results['LE Std'] = Y_pred.std().round(2)
        results['LE Var'] = (Y_pred.std() ** 2).round(1)
    else:
        results.loc[i] = ['Linear', z, s, x.shape[0] * x.shape[1]
            , RMSE.round(3)
            , R.round(4)
            , Y_pred.min().round(1)
            , Y_pred.max().round(1)
            , Y_pred.mean().round(1)
            , Y_pred.std().round(3)
            , (Y_pred.std() ** 2).round(3)]

from sklearn.linear_model import TheilSenRegressor
from sklearn.preprocessing import scale
from pylab import rcParams

for x, y, i, z, s in zip(Xlist, Ylist, range(len(Xlist)), xlist, status):
    x = x.drop(['Country', 'Status', 'Infant Deaths', 'Thinness 10-19'], axis=1)
    x = scale(x)

    print('Thiel {}'.format(z))
    print(z, x.shape)
    # Model
    theil = TheilSenRegressor(random_state=52).fit(x, y)

    # R2
    R = theil.score(x, y)
    print('R^2 Score:{:0.4f}'.format(R))

    # Predictions
    Y_pred = theil.predict(x)
    RMSE = mean_squared_error(y, Y_pred) ** 0.5
    print('RMSE: {:0.3f}'.format(RMSE))
    print('Minimum LE: {:0.1f}'.format(Y_pred.min()))
    print('Maximum LE: {:0.1f}'.format(Y_pred.max()))
    print('Average Predicted LE: {:0.1f}'.format(Y_pred.mean()))
    print('LE Standard Deviation: {:0.3f}'.format(Y_pred.std()))
    print('LE Variance: {:0.3f}'.format(Y_pred.std() ** 2))

    # plot
    z1 = np.polyfit(Y_pred, y, 1)
    z1poly = np.poly1d(z1)
    plt.scatter(Y_pred, y, alpha=1)
    plt.plot(Y_pred, z1poly(Y_pred), linewidth=7.0, color='r')
    plt.title('Thiel {}'.format(z))
    plt.xlabel('Y_pred')
    plt.ylabel('Y')
    rcParams['figure.figsize'] = 10, 10
    plt.show()

    if i == 0:
        # Result DataFrame
        results = pd.DataFrame()
        results["Method"] = ['Thiel']
        results['Set'] = z
        results['Status'] = s
        results['Datapoint Count'] = x.shape[0] * x.shape[1]
        results["RMSE"] = RMSE.round(2)
        results["R^2"] = R.round(2)
        results['LE Min'] = Y_pred.min().round(1)
        results['LE Max'] = Y_pred.max().round(1)
        results['Average LE'] = Y_pred.mean().round(1)
        results['LE Std'] = Y_pred.std().round(2)
        results['LE Var'] = (Y_pred.std() ** 2).round(1)
    else:
        results.loc[i] = ['Thiel', z, s, x.shape[0] * x.shape[1]
            , RMSE.round(3)
            , R.round(4)
            , Y_pred.min().round(1)
            , Y_pred.max().round(1)
            , Y_pred.mean().round(1)
            , Y_pred.std().round(3)
            , (Y_pred.std() ** 2).round(3)]

from sklearn.model_selection import GridSearchCV

model = linear_model.Ridge()

para = {'alpha': [10, 20, 40, 55, 70, 90]}
grid = GridSearchCV(model, para, cv=3)
grid.fit(x, y)

grid.best_estimator_

grid.best_score_

grid.best_params_

"""Interpretation: We have found the best parameters for our Ridge Model"""

for x, y, i, z, s in zip(Xlist, Ylist, range(len(Xlist)), xlist, status):
    x = x.drop(['Country', 'Status'], axis=1)
    x = scale(x)
    print('Ridge {}'.format(z))
    print(z, x.shape)
    # Model
    ridgeregr = linear_model.Ridge(alpha=10, fit_intercept=True, solver='auto', random_state=65)
    ridge = ridgeregr.fit(x, y)

    # R2
    R = ridge.score(x, y)
    print('R^2 Score: {:0.4f}'.format(R))

    # Predictions
    Y_pred = ridge.predict(x)
    RMSE = mean_squared_error(y, Y_pred) ** 0.5
    print('RMSE: {:0.3f}'.format(RMSE))
    print('Minimum LE: {:0.1f}'.format(Y_pred.min()))
    print('Maximum LE: {:0.1f}'.format(Y_pred.max()))
    print('Average Predicted LE: {:0.1f}'.format(Y_pred.mean()))
    print('LE Standard Deviation: {:0.3f}'.format(Y_pred.std()))
    print('LE Variance: {:0.3f}'.format(Y_pred.std() ** 2))

    # plot
    z1 = np.polyfit(Y_pred, y, 1)
    z1poly = np.poly1d(z1)
    plt.scatter(Y_pred, y, alpha=1)
    plt.plot(Y_pred, z1poly(Y_pred), linewidth=7.0, color='r')
    plt.title('Ridge {}'.format(z))
    plt.xlabel('Y_pred')
    plt.ylabel('Y')
    plt.show()

    if i == 0:
        # Result DataFrame
        results = pd.DataFrame()
        results["Method"] = ['Thiel']
        results['Set'] = z
        results['Status'] = s
        results['Datapoint Count'] = x.shape[0] * x.shape[1]
        results["RMSE"] = RMSE.round(2)
        results["R^2"] = R.round(2)
        results['LE Min'] = Y_pred.min().round(1)
        results['LE Max'] = Y_pred.max().round(1)
        results['Average LE'] = Y_pred.mean().round(1)
        results['LE Std'] = Y_pred.std().round(2)
        results['LE Var'] = (Y_pred.std() ** 2).round(1)
    else:
        results.loc[i] = ['Ridge', z, s, x.shape[0] * x.shape[1]
            , RMSE.round(3)
            , R.round(4)
            , Y_pred.min().round(1)
            , Y_pred.max().round(1)
            , Y_pred.mean().round(1)
            , Y_pred.std().round(3)
            , (Y_pred.std() ** 2).round(3)]

from sklearn.model_selection import GridSearchCV

model = linear_model.Lasso()

para = {'alpha': [0.01, 0.015, 0.02, 0.025]}
grid = GridSearchCV(model, para, cv=3)
grid.fit(x, y)

grid.best_estimator_

grid.best_score_

grid.best_params_

cols = ['Year', 'AdultMortality', 'Infant Deaths', 'Alcohol', 'PercentExpenditure', 'Hep B', 'Measles', 'BMI',
        'U5Deaths',
        'Polio', 'TotalExpenditure', 'Diphtheria', 'HIVAIDS', 'Thinness1019',
        'Thinness59', 'IncomeComposition', 'Schooling', 'country_code']
feature_importances = pd.DataFrame(index=cols)
for x, y, i, z, s in zip(Xlist, Ylist, range(len(Xlist)), xlist, status):
    x
    y
    x = x.drop(['Country', 'Status'], axis=1)
    x = scale(x)
    print('Lasso {}'.format(z))
    print(z, x.shape)
    # Model
    rf = linear_model.Lasso(alpha=0.025, fit_intercept=True, random_state=65)
    rfc = rf.fit(x, y)

    # R2
    R = rfc.score(x, y)
    print('R^2 Score: {:0.4f}'.format(R))

    # Predictions
    Y_pred = rf.predict(x)
    RMSE = mean_squared_error(y, Y_pred) ** 0.5
    print('RMSE: {:0.3f}'.format(RMSE))
    print('Minimum LE: {:0.1f}'.format(Y_pred.min()))
    print('Maximum LE: {:0.1f}'.format(Y_pred.max()))
    print('Average Predicted LE: {:0.1f}'.format(Y_pred.mean()))
    print('LE Standard Deviation: {:0.3f}'.format(Y_pred.std()))
    print('LE Variance: {:0.3f}'.format(Y_pred.std() ** 2))

    # plot
    z1 = np.polyfit(Y_pred, y, 1)
    z1poly = np.poly1d(z1)
    plt.scatter(Y_pred, y, alpha=1)
    plt.plot(Y_pred, z1poly(Y_pred), linewidth=7.0, color='r')
    plt.title('Lasso {}'.format(z))
    plt.xlabel('Y_pred')
    plt.ylabel('Y')
    plt.show()
    if i == 0:
        # Result DataFrame
        results = pd.DataFrame()
        results["Method"] = ['Thiel']
        results['Set'] = z
        results['Status'] = s
        results['Datapoint Count'] = x.shape[0] * x.shape[1]
        results["RMSE"] = RMSE.round(2)
        results["R^2"] = R.round(2)
        results['LE Min'] = Y_pred.min().round(1)
        results['LE Max'] = Y_pred.max().round(1)
        results['Average LE'] = Y_pred.mean().round(1)
        results['LE Std'] = Y_pred.std().round(2)
        results['LE Var'] = (Y_pred.std() ** 2).round(1)
    else:
        results.loc[i] = ['Lasso', z, s, x.shape[0] * x.shape[1]
            , RMSE.round(3)
            , R.round(4)
            , Y_pred.min().round(1)
            , Y_pred.max().round(1)
            , Y_pred.mean().round(1)
            , Y_pred.std().round(3)
            , (Y_pred.std() ** 2).round(3)]

from sklearn.model_selection import GridSearchCV

model = ensemble.GradientBoostingRegressor()
para = {'n_estimators': [50, 100, 150], 'max_depth': [1, 2, 3]}
grid = GridSearchCV(model, para, cv=3)
grid.fit(x, y)

grid.best_estimator_

grid.best_score_

grid.best_params_

cols = ['Year', 'AdultMortality', 'Infant Deaths', 'Alcohol', 'Population', 'GDP', 'PercentExpenditure', 'Hep B',
        'Measles', 'BMI', 'U5Deaths',
        'Polio', 'TotalExpenditure', 'Diphtheria', 'HIVAIDS', 'Thinness1019',
        'Thinness59', 'IncomeComposition', 'Schooling', 'country_code']
feature_importances = pd.DataFrame(index=cols)
for x, y, i, z, s in zip(Xlist, Ylist, range(len(Xlist)), xlist, status):
    x
    y
    x = x.drop(['Country', 'Status'], axis=1)
    x = scale(x)
    print('Gradient Boosting {}'.format(z))
    print(z, x.shape)
    # Model
    params = {'n_estimators': 100, 'max_depth': 3}
    rf = ensemble.GradientBoostingRegressor(**params)
    rfc = rf.fit(x, y)

    # R2
    R = rfc.score(x, y)
    print('R^2 Score: {:0.4f}'.format(R))

    # Predictions
    Y_pred = rf.predict(x)
    RMSE = mean_squared_error(y, Y_pred) ** 0.5
    print('RMSE: {:0.3f}'.format(RMSE))
    print('Minimum LE: {:0.1f}'.format(Y_pred.min()))
    print('Maximum LE: {:0.1f}'.format(Y_pred.max()))
    print('Average Predicted LE: {:0.1f}'.format(Y_pred.mean()))
    print('LE Standard Deviation: {:0.3f}'.format(Y_pred.std()))
    print('LE Variance: {:0.3f}'.format(Y_pred.std() ** 2))

    # plot
    z1 = np.polyfit(Y_pred, y, 1)
    z1poly = np.poly1d(z1)
    plt.scatter(Y_pred, y, alpha=1)
    plt.plot(Y_pred, z1poly(Y_pred), linewidth=7.0, color='r')
    plt.title('Gradient Boosting {}'.format(z))
    plt.xlabel('Y_pred')
    plt.ylabel('Y')
    plt.show()

    # Feature Importance
    feature_importances[z] = (rfc.feature_importances_ * 100).round(2)
    print('Top 5 Features\n', feature_importances[z].nlargest(5).round(2), '\n')

    if i == 0:
        # Result DataFrame
        results = pd.DataFrame()
        results["Method"] = ['Thiel']
        results['Set'] = z
        results['Status'] = s
        results['Datapoint Count'] = x.shape[0] * x.shape[1]
        results["RMSE"] = RMSE.round(2)
        results["R^2"] = R.round(2)
        results['LE Min'] = Y_pred.min().round(1)
        results['LE Max'] = Y_pred.max().round(1)
        results['Average LE'] = Y_pred.mean().round(1)
        results['LE Std'] = Y_pred.std().round(2)
        results['LE Var'] = (Y_pred.std() ** 2).round(1)
    else:
        results.loc[i] = ['Gradient Boosting', z, s, x.shape[0] * x.shape[1]
            , RMSE.round(3)
            , R.round(4)
            , Y_pred.min().round(1)
            , Y_pred.max().round(1)
            , Y_pred.mean().round(1)
            , Y_pred.std().round(3)
            , (Y_pred.std() ** 2).round(3)]

feature_importances