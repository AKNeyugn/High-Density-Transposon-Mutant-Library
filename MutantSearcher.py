""" Script to process large mutant library data file by removing redundancies 
    and to search, for each B. cenocepacia K56-2 essential/non-essential genes, 
    mutants presenting the gene.

    Author: Roy Nguyen
    Last edited: June 4, 2019
"""

import sys
import collections
import datetime
import pandas as pd


processed_mutant_library = "ProcessedMutantLibrary.xlsx"
output = "EssentialGenesMutants.xlsx"
tags_to_remove = ["reference", "position", "count"]
locus_tag_identifier = ["BCA", "QU43"]

# Set pandas option to avoid displaying scientific notations
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def main(argv=None):
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    mutant_library_file = sys.argv[1]
    gene_library_file = sys.argv[2]
    output_excel = False
    if (len(sys.argv) == 4 and sys.argv[3].lower() == "true"):
        output_excel = sys.argv[3]

    processed_data = process_mutants(mutant_library_file, output_excel)
    search_mutants(gene_library_file, processed_data)

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return


def process_mutants(mutant_library_file, output_excel):
    '''
    Filter mutant library for unique gene annotations (ignoring reference,
    position, read count) into a new Excel file (optional) and return the processed
    dataframe

    Args:
        mutant_library_file (string): File name of HDTM library
        output_excel (boolean): Whether filtered data is written into an Excel file
    
    Return:
        (DataFrame): filtered mutant library
    '''
    sys.stdout.write("Processing mutant library... \n")
    with pd.ExcelFile(mutant_library_file) as xls:
        df_unprocessed = pd.read_excel(xls, sheet_name=0, keep_default_na=False, na_values=[""])
        df_unprocessed.drop(tags_to_remove, axis=1, inplace=True)
        df_processed = df_unprocessed.drop_duplicates(keep="first")

        if (output_excel):
            sys.stdout.write("Writing to Excel... \n")
            df_processed.to_excel(processed_mutant_library, index=False)

    sys.stdout.write("Finished processing mutants! \n")
    sys.stdout.write("\n")
    return df_processed

def search_mutants(gene_library_file, processed_data):
    '''
    For each B. cenocepacia J2315 locus tag, search all mutants possessing 
    the tag and output results into a new Excel file

    Args:
        gene_library_file (string): File name of reference essential genes
                        library
        processed_data (DataFrame): filtered mutant library
    '''
    sys.stdout.write("Searching essential genes mutants... \n")
    with pd.ExcelFile(gene_library_file) as gene_xls:
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_gene = pd.read_excel(gene_xls, sheet_name=0, keep_default_na=False, na_values=[""])
            df_mutant = processed_data
            columns_mutants = pd.Index(["J2315 locus tag"])
            columns_mutants = columns_mutants.append(df_mutant.columns)
            essentials_list = df_gene.iloc[2:510,12]
            essentials_dict = {gene: [] for gene in essentials_list}
            non_essentials_list = [ele for ele in df_gene.iloc[2:6362,43] if str(ele) != "nan"]
            non_essentials_dict = {gene: [] for gene in non_essentials_list}

            for index, row in df_mutant.iterrows():
                list_genes = get_locus_tags(row)
                essential = False
                for gene in list_genes:
                    if gene in essentials_dict.keys():
                        essentials_dict[gene].append(row)
                        essential = True
                if not essential:
                    for gene in list_genes:
                        if gene in non_essentials_dict.keys():
                            non_essentials_dict[gene].append(row)
            
            sys.stdout.write("Writing to Excel... \n")
            sys.stdout.write("Processing essential genes... \n")
            essentials_mutants = create_df_mutants(essentials_dict, essentials_list, columns_mutants)
            essentials_numbers = create_df_numbers(essentials_dict)
            essentials_mutants.to_excel(writer, sheet_name="Essential_Genes_Mutants", index=False)
            essentials_numbers.to_excel(writer, sheet_name="Essential_Genes_Numbers", index=False)
            create_chart(writer, essentials_numbers, True)

            sys.stdout.write("Processing non-essential genes... \n")
            non_essentials_mutants = create_df_mutants(non_essentials_dict, non_essentials_list, columns_mutants)
            non_essentials_numbers = create_df_numbers(non_essentials_dict)
            non_essentials_mutants.to_excel(writer, sheet_name="Non_Essential_Genes_Mutants", index=False)
            non_essentials_numbers.to_excel(writer, sheet_name="Non_Essential_Genes_Numbers", index=False)
            create_chart(writer, non_essentials_numbers, False)
            
    sys.stdout.write("Finished searching for mutants! \n")
    sys.stdout.write("\n")
    return


def get_locus_tags(row):
    '''
    Extract all old locus tags (eg. BCALxxxx) in mutant

    Args:
        row (Series): Excel row corresponding to mutant

    Return:
        (tuple): list of locus tags in mutant 
    '''
    list_locus_tags = []

    for i in range(len(row)):
        if (row[i] != ""):
            for tag_id in locus_tag_identifier:
                if tag_id in str(row[i]):
                    list_locus_tags.append(row[i])

    return tuple(list_locus_tags)

def create_df_mutants(data, order, columns):
    '''
    Convert gene-mutant dictionary into DataFrame to be written in Excel

    Args: 
        data (dict): gene-mutant dictionary
        order (list): order of gene to output
        columns (Index): list of column names

    Return:
        (DataFrame): gene-mutant DataFrame
    '''
    frames = []
    for gene in order:
        frames.append(pd.DataFrame([gene], columns=["J2315 locus tag"]))
        frames.append(pd.DataFrame(data[gene]))

    output = pd.concat(frames, sort=False)
    output = output[columns]

    return output

def create_df_numbers(data):
    '''
    Create gene-# mutants DataFrame to be written in Excel

    Args: 
        data (dict): gene-mutant dictionary
        columns (Index): list of column names

    Return:
        (DataFrame): gene-# mutants DataFrame
    '''
    df_columns = ["J2315 locus tag", "# mutants recovered"]
    chart_df_columns = df_columns + ["", "# mutants recovered", "Frequency"]
    sorted_data = sorted(data, key=lambda k: len(data[k]), reverse=True)
    sorted_data_full = []
    for gene in sorted_data:
        sorted_data_full.append((gene, len(data[gene])))

    output = pd.DataFrame(sorted_data_full, columns=df_columns)

    mutant_counter = collections.Counter(output[df_columns[1]])
    chart_data = []
    for i in range(max(mutant_counter.elements())+1):
        chart_data.append((i, mutant_counter[i]))
    output_chart_data = pd.DataFrame(chart_data)

    output = pd.concat([output, pd.DataFrame([""]), output_chart_data], axis=1)
    output.columns = chart_df_columns

    return output

def create_chart(writer, data, essential):
    '''
    Output histogram describing frequency of # mutants recovered 
    into Excel file

    Args:
        writer (ExcelWriter): writer for output Excel file
        data (DataFrame): gene-# mutant DataFrame
        essential (bool): True if essential genes DataFrame
    '''
    workbook = writer.book
    if essential:
        sheet_name = "Essential_Genes_Numbers"
        chart_name = "Frequency of # essential gene mutants recovered"
    else:
        sheet_name = "Non_Essential_Genes_Numbers"
        chart_name = "Frequency of # non-essential gene mutants recovered"
    worksheet = writer.sheets[sheet_name]
    data_range = sum(str(ele) != "nan" for ele in data[data.columns[4]].values)
    chart_cat = "=" + sheet_name + "!$D$2:$D$" + str(data_range + 1)
    chart_val = "=" + sheet_name + "!$E$2:$E$" + str(data_range + 1)

    chart = workbook.add_chart({"type": "column"})
    chart.add_series({
        "categories": chart_cat,
        "values": chart_val
    })
    chart.set_legend({"none": True})
    chart.set_title({"name": chart_name})
    chart.set_x_axis({"name": data.columns[3]})
    chart.set_y_axis({"name": data.columns[4]})
    worksheet.insert_chart("G2", chart)
    return


if __name__ == "__main__":
    main()

