import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def five_number_summary(df):
    quartiles = np.percentile(df, [25, 50, 75])
    df_min, df_max = df.min(), df.max()
    return df_min, quartiles[0],quartiles[1],quartiles[2], df_max


def main():
    st.sidebar.title("Stats 21 Discussion Project")
    st.title("Exploratory Data Analysis Application")
    # Add your app code here

if __name__ == '__main__':
    main()

def main():
    st.sidebar.title("CSV File Uploader")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write(df)

        available_columns = df.columns.tolist()


        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])

        # Count the number of categorical, numerical, and boolean variables
        categorical_vars = df.select_dtypes(include=['object']).columns
        numerical_vars = df.select_dtypes(include=['int', 'float']).columns
        boolean_vars = df.select_dtypes(include=['bool']).columns

        st.write("Number of Categorical Variables:", len(categorical_vars))
        st.write("Number of Numerical Variables:", len(numerical_vars))
        st.write("Number of Boolean Variables:", len(boolean_vars))

        st.write("Categorical Variables:", list(categorical_vars))
        st.write("Numerical Variables:", list(numerical_vars))
        st.write("Boolean Variables:", list(boolean_vars))

        # Display the column selector widget
        selected_columns = st.multiselect('Select columns', available_columns)

        # Filter the dataframe based on the selected columns
        filtered_df = df[selected_columns]

        # Display the filtered dataframe
        st.write(filtered_df)

        for i in range(filtered_df.shape[1]):
            col_name = filtered_df.columns[i]
            selected_col = filtered_df[col_name].to_numpy()
            if selected_col.dtype == "object":
                proportions = filtered_df[col_name].value_counts(normalize=True)
                table = pd.DataFrame({'Category': proportions.index, 'Proportion': proportions.values})
                st.title(col_name +  " Proportion Table:")
                st.write(table)    
                barplot = sns.countplot(data = filtered_df, x = col_name, color = "steelblue", saturation = 0.8, mouseover = True)
                barplot.set(title="Barplot of " + col_name, xlabel = col_name, ylabel = "Counts")
                st.pyplot(barplot.figure)
            elif selected_col.dtype == "int" or selected_col.dtype == "float": 
                st.title(col_name +  " Distribution:")
                st.write("Five Number Summary:", five_number_summary(selected_col))
                fig, ax = plt.subplots()
                ax.set_title(col_name + 'Histogram')
                ax.set_xlabel(col_name)
                ax.set_ylabel('Count')
                binwidth = int((max(filtered_df[col_name]) - min(filtered_df[col_name]))/20)
                N, bins, patches = ax.hist(filtered_df[col_name], bins=range(int(min(filtered_df[col_name])), int(max(filtered_df[col_name])) + binwidth, binwidth), facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.85)
                for i in range(len(patches)):
                    patches[i].set_facecolor(plt.cm.Greens(N[i]/max(N)))
                st.pyplot(fig)


if __name__ == '__main__':
    main()