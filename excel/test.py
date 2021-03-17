import pandas as pd


def defdrop_duplicates(oldExcel, newExcel, outputExcel):
    df1 = pd.read_excel(oldExcel)
    df2 = pd.read_excel(newExcel)
    c = df1.append(df2)
    c.drop_duplicates(keep=False, inplace=True)
    print(c)
    df = pd.DataFrame(c)
    df.to_excel(outputExcel, index=False)


defdrop_duplicates('old.xlsx', 'new.xlsx', 'out.xlsx')
