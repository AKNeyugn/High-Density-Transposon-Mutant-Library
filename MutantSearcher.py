import sys
import numpy as np
import pandas as pd


processed_mutant_library = "ProcessedMutantLibrary.xlsx"
output = "EssentialGenesMutants.xlsx"
tags_to_remove = ["reference", "position", "count"]

# Set pandas option to avoid displaying scientific notations
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def process_mutants(mutant_library_file):
    '''
    Filter mutant library for unique gene annotations (unique old locus tags,
    and ignoring reference, position, read count) into a new Excel file

    Args:
        mutant_library_file (string): File name of HDTM library
    '''
    sys.stdout.write("Processing mutant library... \n")
    with pd.ExcelFile(mutant_library_file) as xls:
        df_unprocessed = pd.read_excel(xls, sheet_name=0, keep_default_na=False, na_values=[""])
        df_unprocessed.drop(tags_to_remove, axis=1, inplace=True)
        columns = df_unprocessed.columns
        df_processed = pd.DataFrame(columns=columns)
        prev_row = set()
        num_mutant_processed = 0

        for index, row in df_unprocessed.iterrows():
            num_mutant_processed += 1

            # Filter N/A CDS strand
            if (row["CDS strand"] != "N/A"):
                locus_tags = get_locus_tags(row)

                #  Filter strands with already seen locus tag
                if (locus_tags not in prev_row):
                    # Increase number of columns for mutants with operons
                    new_columns = columns
                    for j in range(len(row) - len(columns)):
                        new_columns.append(j)
                    new_df = pd.DataFrame(columns=new_columns)

                    # Copy mutant data into new data frame
                    for k in range(len(row)):
                        df_index = new_df.columns[k]
                        new_df.at[0, df_index] = row[k]
                    df_processed = df_processed.append(new_df, sort=False)

                    # Remember previous row to reduce redundancies
                    prev_row.add(locus_tags)

            sys.stdout.write("Processed %d mutants \r" % (num_mutant_processed))
            sys.stdout.flush()

        sys.stdout.write("\n")
        df_processed.to_excel(processed_mutant_library, index=False)

def search_mutants(gene_library_file):
    '''
    '''
    return

def cleanup():
    '''
    '''
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
        if (row[i] != "" and "BCAL" in str(row[i])):
            list_locus_tags.append(row[i])

    return tuple(list_locus_tags)


def main(argv=None):
    mutant_library_file = sys.argv[1]
    gene_library_file = sys.argv[2]
    process_mutants(mutant_library_file)
    search_mutants(gene_library_file)
    #cleanup()

    sys.stdout.write("\nDone!")
    return

if __name__ == "__main__":
    main()

