import pandas as pd   # 1.2


unscaled_data=pd.read_csv("data/unscaled_cleaned_data.csv")

col_names=[
    ('Radius (mean)', 'radius_mean'),
    ('Texture (mean)', 'texture_mean'),
    ('Perimeter (mean)', 'perimeter_mean'),
    ('Area (mean)', 'area_mean'),
    ('Smoothness (mean)', 'smoothness_mean'),
    ('Compactness (mean)', 'compactness_mean'),
    ('Concavity (mean)', 'concavity_mean'),
    ('Concave points (mean)', 'concave points_mean'),
    ('Symmetry (mean)', 'symmetry_mean'),
    ('Fractal dimension (mean)', 'fractal_dimension_mean'),
    ('Radius (se)', 'radius_se'),
    ('Texture (se)', 'texture_se'),
    ('Perimeter (se)', 'perimeter_se'),
    ('Area (se)', 'area_se'),
    ('Smoothness (se)', 'smoothness_se'),
    ('Compactness (se)', 'compactness_se'),
    ('Concavity (se)', 'concavity_se'),
    ('Concave points (se)', 'concave points_se'),
    ('Symmetry (se)', 'symmetry_se'),
    ('Fractal dimension (se)', 'fractal_dimension_se'),
    ('Radius (worst)', 'radius_worst'),
    ('Texture (worst)', 'texture_worst'),
    ('Perimeter (worst)', 'perimeter_worst'),
    ('Area (worst)', 'area_worst'),
    ('Smoothness (worst)', 'smoothness_worst'),
    ('Compactness (worst)', 'compactness_worst'),
    ('Concavity (worst)', 'concavity_worst'),
    ('Concave points (worst)', 'concave points_worst'),
    ('Symmetry (worst)', 'symmetry_worst'),
    ('Fractal dimension (worst)', 'fractal_dimension_worst')
]



def Max(col):
    return float(unscaled_data[col].max())

def Mean(col):
    return float(unscaled_data[col].mean())



