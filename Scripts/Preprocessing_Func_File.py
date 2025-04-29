from Scripts import Imports

# Add BMI Category
def bmi_category(bmi):
    if bmi < 18.5:
        return 1
    elif bmi < 24.9:
        return 2
    elif bmi < 29.9:
        return 3
    else:
        return 4

def Preprocessing_Func(age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active):
    # Create a dictionary with the column names and corresponding values
    data = {
        'age': [age],
        'gender': [gender],
        'height': [height],
        'weight': [weight],
        'ap_hi': [ap_hi],
        'ap_lo': [ap_lo],
        'cholesterol': [cholesterol],
        'gluc': [gluc],
        'smoke': [smoke],
        'alco': [alco],
        'active': [active]
    }
    
    # Load the scaler
    with open("pklFiles/StandardScaler.pkl", "rb") as f:
        scaler1 = pickle.load(f)

    with open("pklFiles/PowerTransformation.pkl", "rb") as f:
        scaler2 = pickle.load(f)

    # Convert dictionary to DataFrame
    Healthcare = Imports.pd.DataFrame(data)

    Healthcare_Cleaned=Healthcare.copy()
    Healthcare_Cleaned['age']=Healthcare_Cleaned['age'].astype('int64')
    Healthcare_Cleaned.loc[:,'height_m'] = Healthcare_Cleaned['height'] / 100  # Convert height to meters
    Healthcare_Cleaned.loc[:,'bmi'] = Healthcare_Cleaned['weight'] / (Healthcare_Cleaned['height_m'] ** 2)  # Calculate BMI
    Healthcare_Cleaned.drop(columns=['height_m'], inplace=True)  # Remove temporary column
    Healthcare_Cleaned.loc[:,'bmi_category'] = Healthcare_Cleaned['bmi'].apply(bmi_category)
    # Calculate Mean Arterial Pressure (MAP)
    Healthcare_Cleaned.loc[:,'MAP'] = (Healthcare_Cleaned['ap_hi'] + 2 * Healthcare_Cleaned['ap_lo']) / 3

    # Calculate Pulse Pressure (PP)
    Healthcare_Cleaned.loc[:,'PP'] = Healthcare_Cleaned['ap_hi'] - Healthcare_Cleaned['ap_lo']
    bins = [0, 30, 60, 90, 120, 140]  # Adjust these ranges based on your criteria
    labels = [1, 2, 3, 4, 5]  # Category labels
    # Apply categorization
    Healthcare_Cleaned['pp_category'] = Imports.pd.cut(Healthcare_Cleaned['PP'], bins=bins, labels=labels, right=True,include_lowest=True)
    age_bins = [20, 30, 40, 50, 60, 70, 80]
    age_labels = ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79']

    # Step 2: Create 'age_group' using Imports.pd.cut()
    Healthcare_Cleaned['age_group'] = Imports.pd.cut(Healthcare_Cleaned['age'],bins=age_bins,labels=age_labels,right=False,include_lowest=True)

    # Step 3: Map the age group to numeric values
    age_mapping = {'20-29':1, '30-39':2, '40-49':3, '50-59':4, '60-69':5, '70-79':6}
    Healthcare_Cleaned['age_group'] = Healthcare_Cleaned['age_group'].map(age_mapping)
    X = Healthcare_Cleaned.drop(columns = ['gender','height'], axis = 1)
    X_filtered=X[['age','weight','ap_hi','ap_lo','bmi','MAP','PP']]
    categorical_cols = X[['cholesterol','gluc','smoke','alco','active','bmi_category','pp_category','age_group']]
    X_scaled = scaler1.fit_transform(X_filtered)
    df_scaled = Imports.pd.DataFrame(X_scaled, columns=X_filtered.columns)
    X_transformed = scaler2.fit_transform(df_scaled)
    df_transformed = Imports.pd.DataFrame(X_transformed, columns=df_scaled.columns)
    x_final= Imports.pd.concat([df_transformed, categorical_cols.reset_index(drop=True)], axis=1)
    x_final['pp_category'] = x_final['pp_category'].astype('int')
    x_final['age_group'] = x_final['age_group'].astype('int')

    return x_final


