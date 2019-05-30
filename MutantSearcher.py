import sys
import os
import datetime
import pandas as pd


processed_mutant_library = "ProcessedMutantLibrary.xlsx"
output = "EssentialGenesMutants.xlsx"
tags_to_remove = ["reference", "position", "count"]
locus_tag_identifier = ["BCA", "pBCA", "QU43"]

# Set pandas option to avoid displaying scientific notations
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def main(argv=None):
    start = datetime.datetime.now()
    mutant_library_file = sys.argv[1]
    gene_library_file = sys.argv[2]
    output_excel = False
    if (len(sys.argv) == 4 and sys.argv[3].lower() == "true"):
        output_excel = sys.argv[3]

    processed_data = process_mutants(mutant_library_file, output_excel)
    search_mutants(gene_library_file, processed_data)

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.total_seconds() / 60) + " minutes. \n")
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

        # Write filtered data into an Excel file
        if (output_excel):
            sys.stdout.write("Writing to Excel... \n")
            df_processed.to_excel(processed_mutant_library, index=False)

    sys.stdout.write("Finished processing mutants! \n")
    sys.stdout.write("\n")
    return df_processed

def search_mutants(gene_library_file, processed_data):
    '''
    For every B. cenocepacia J2315 locus tag, search all mutants possessing 
    the tag and output results into a new Excel file

    Args:
        gene_library_file (string): File name of reference essential genes
                        library
        processed_data (DataFrame): filtered mutant library
    '''
    sys.stdout.write("Searching essential genes mutants... \n")
    with pd.ExcelFile(gene_library_file) as gene_xls:
        df_gene = pd.read_excel(gene_xls, sheet_name=0, keep_default_na=False, na_values=[""])
        df_mutant = processed_data
        columns = pd.Index(["J2315 locus tag"])
        columns = columns.append(df_mutant.columns)
        essentials_list = df_gene.iloc[2:510,12]
        essentials_dict = {gene: [] for gene in essentials_list}

        for index, row in df_mutant.iterrows():
            list_genes = get_locus_tags(row)
            for gene in list_genes:
                if gene in essentials_dict.keys():
                    essentials_dict[gene].append(row)
        
        df_output = create_df_output(essentials_dict, columns)
        sys.stdout.write("Writing to Excel... \n")
        df_output.to_excel(output, index=False)
        
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

def create_df_output(data, columns):
    '''
    Convert gene-mutant dictionary into DataFrame to be written in Excel

    Args: 
        data (dict): gene-mutant dictionary
        columns (Index): list of column names

    Return:
        (DataFrame): gene-mutant DataFrame
    '''
    output = pd.DataFrame(columns=columns)
    ind = 0
    for gene in data.keys():
        output.at[ind, "J2315 locus tag"] = gene
        ind += 1
        for mutant in data[gene]:
            for i in range(len(mutant)):
                df_index = output.columns[i+1]
                output.at[ind, df_index] = mutant[i]
            ind += 1

    return output


if __name__ == "__main__":
    main()

