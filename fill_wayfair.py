import pandas as pd
import openpyxl

file_path = '/root/.openclaw/media/inbound/file_3---fdf5fa93-ae80-487c-a3ba-d83afddef241.xlsx'
output_path = 'Wayfair_Spec_Sheet_Filled.xlsx'

# Data for TV Stand
tv_stand = {
    'Supplier Part Number': 'CASA-TV-018',
    'Brand': 'Casa Design Furniture',
    'Product Name': '#018 NORALIE TV STAND & FIREPLACE',
    'Marketing Copy': 'Elevate your entertainment area with the Noralie TV Stand & Fireplace. Featuring a beveled mirrored finish and elegant faux diamond inlays, this free-standing unit adds a touch of luxury to any room. Includes a built-in LED electric fireplace with touch control and remote, providing 4777 BTUs of heat for areas up to 400 sq ft.',
    'Feature Bullet 1': 'Mirrored finish with beveled edges',
    'Feature Bullet 2': 'Faux diamond inlay accents',
    'Feature Bullet 3': 'Built-in 4777 BTU LED electric fireplace',
    'Feature Bullet 4': 'Includes remote control and touch panel',
    'Feature Bullet 5': 'Two storage doors with internal compartments',
    'Base Cost': 899.00
}

# Data for Bed
bed = {
    'Supplier Part Number': 'CASA-BED-003',
    'Brand': 'Casa Design Furniture',
    'Product Name': '#003 PERRIS TWIN WORKSTATION LOFT BED',
    'Marketing Copy': 'Perfect for space-saving needs, the Perris Twin Workstation Loft Bed combines sleep and study in one elegant design. Crafted from select woods and Asian veneers, it features a large workspace with a dedicated keyboard drawer and integrated bookshelves.',
    'Feature Bullet 1': 'Space-saving twin loft bed design',
    'Feature Bullet 2': 'Integrated study area with large workspace',
    'Feature Bullet 3': 'Keyboard drawer and storage bookshelves included',
    'Feature Bullet 4': 'Max weight capacity of 400 lbs',
    'Feature Bullet 5': 'Crafted from Asian veneers and select woods',
    'Base Cost': 459.00,
    'Overall Width': 41.75,
    'Overall Depth': 80.0,
    'Overall Height': 74.0
}

# Load the entire workbook to preserve formatting if possible
# Note: pandas.to_excel with openpyxl engine is better for this
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # We need to read and write all sheets to keep the file valid
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        # Read the sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Add products to specific sheets
        if sheet_name == '6 - TV Stands & Enterta':
            # Wayfair header starts at row 4 (index 3)
            # We'll just append our row at the end of the existing dataframe
            # But we need to match the columns
            new_row = pd.Series(dtype='object')
            # Map columns by name
            cols = pd.read_excel(file_path, sheet_name=sheet_name, header=3).columns
            for col in cols:
                if col in tv_stand:
                    new_row[col] = tv_stand[col]
            
            # Find the first empty row in the original dataframe (starts at row 6)
            # Actually, let's just append to the end
            df.loc[len(df)] = new_row
            
        elif sheet_name == '12 - Beds':
            cols = pd.read_excel(file_path, sheet_name=sheet_name, header=3).columns
            new_row = pd.Series(dtype='object')
            for col in cols:
                if col in bed:
                    new_row[col] = bed[col]
            df.loc[len(df)] = new_row
            
        # Write back to the new file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"File saved to {output_path}")
