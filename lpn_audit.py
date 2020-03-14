# import required libraries
import pandas as pd

# import CSV file to audit against
wms_data = pd.read_csv('pick_list.csv')

# main function to call
def main():
    row_count = int(wms_data.shape[0])
    user_audit = create_list(row_count)

    audit_data = pd.DataFrame(user_audit, columns=['lpn','part_no','qty'])

    differences = compare_dataframes(wms_data,audit_data)
    differences.rename(columns = {'_merge':'Present in'}, inplace=True)

    # Print summary analysis
    print("Audit Summary")
    print('-'*50)
    count_row1 = round(differences.shape[0] / 2)
    count_row2 = wms_data.shape[0]
    diff_percentage = round((count_row1 / count_row2) * 100, 2)
    print(str(audit_data.shape[0]) + ' peices audited.')
    print(str(count_row1) + ' of the ' + str(count_row2) + ' pieces have variances.')
    print('Accuracy rate is ' + str(100 - diff_percentage) + ' %.')

# function accept user input
def create_list(row_count):
    """"Prompt user for input once for each record in WMS data"""

    user_audit = []
    for x in range(row_count):
        user_audit.append([object(input("LPN: ")), object(input("Part No: ")), int(input("Quantity: "))])
    return user_audit

# function to compare two dataframes
def compare_dataframes(df1, df2, which=None):
    """Find rows which are different between two DataFrames."""
   
    comparison_df = df1.merge(df2,
                              indicator=True,
                              how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df

if __name__ == '__main__':
    main()