from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from scipy import stats

import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from stemgraphic import stem_graphic




def home(request):
    print('Home')
    return render(request, 'home.html')


def about(request):
    print('About')
    return render(request, 'about.html')


def data_analysis(request):
    print('Data analysis')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        df = pd.read_csv(fs.open(filename))

        # File Information
        file_info = {
            "File Name": myfile.name,
            "Number of Rows": df.shape[0],
            "Number of Columns": df.shape[1]
        }

        # Missing Values
        missing_values = pd.DataFrame(df.isnull().sum(), columns=["Missing Values"]).reset_index()
        missing_values.columns = ["Column", "Missing Values"]

        # Data Types
        data_types = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index()
        data_types.columns = ["Column", "Data Type"]

        # Data analysis
        r_table = df.apply(lambda x: df.apply(lambda y: r_xor_p(x, y, r_xor_p='r')))
        p_table = df.apply(lambda x: df.apply(lambda y: r_xor_p(x, y, r_xor_p='p')))

        # Summary Statistics
        summary_stats = df.describe()

        '''Correlation Heatmap
        corr_heatmap = None
        display_corr_heatmap = request.POST.get('display_corr_heatmap')
        if display_corr_heatmap:
            corr = df.corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            corr_heatmap = plt.gcf()
        
        # Histogram
        selected_column_hist = request.POST.get('selected_column_hist')
        fig_hist, ax_hist = plt.subplots(figsize=(8, 6))
        sns.histplot(data=df, x=selected_column_hist, kde=True, ax=ax_hist)

        # Density Plot
        selected_column_density = request.POST.get('selected_column_density')
        fig_density, ax_density = plt.subplots(figsize=(8, 6))
        sns.kdeplot(data=df, x=selected_column_density, fill=True, ax=ax_density)'''



        return render(request, 'data_analysis.html', {
            'result_present': True,
            'results': {
                'r_table': r_table.to_html(),
                'p_table': p_table.to_html()
            },
            'file_info': file_info,
            'missing_values': missing_values.to_html(),
            'data_types': data_types.to_html(),
            'df_preview': df.head().to_html(),
            'summary_stats': summary_stats.to_html()
            
        })

    return render(request, 'data_analysis.html')



def r_xor_p(x, y, r_xor_p='r'):
    ''' Pearson's r or its p
    Depending of what you would like to get.
    '''
    r, p = stats.pearsonr(x, y)

    if r_xor_p == 'r':
        return r
    else:
        return p
