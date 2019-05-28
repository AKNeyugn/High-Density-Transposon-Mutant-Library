import sys
import numpy as np
import pandas as pd


processed_mutant_library = "ProcessedMutantLibrary.xlsx"
output = "EssentialGenesMutants.xlsx"
filter_tag = "Locus TAG"


def process_mutants(mutant_library_file):
    '''
    Filter mutant library for unique gene annotations (ignoring position,
    read count, gene IDs and length) into a new Excel file

    Args:
        mutant_library_file (string): File name of HDTM library
    '''
    
    sys.stdout.write("Processing mutant library... \n")
    with pd.ExcelFile(mutant_library_file) as xls:
        df_unprocessed = pd.read_excel(xls, sheet_name=0, keep_default_na=False, na_values=[""])
        column = df_unprocessed.columns
        df_processed = pd.DataFrame(columns=column)
        prev_row = set()
        num_mutant_processed = 0

        for index, row in df_unprocessed.iterrows():
            num_mutant_processed += 1

            # Filter N/A CDS strand and strands with already seen Locus tag
            if (row["CDS strand"] != "N/A" and row[filter_tag] not in prev_row):

                # Increase number of columns for mutants with operons
                new_column = column
                for j in range(len(row) - len(column)):
                    new_column.append(j)
                new_df = pd.DataFrame(columns=new_column)

                # Copy mutant data into new data frame
                for k in range(len(row)):
                    df_index = new_df.columns[k]
                    new_df.at[0, df_index] = row[k]
                df_processed = df_processed.append(new_df, sort=False)

                # Remember previous row to reduce redundancies
                prev_row.add(row[filter_tag])

            sys.stdout.write("Processed %d mutants \r" % (num_mutant_processed))
            sys.stdout.flush()

        df_processed.to_excel(processed_mutant_library, index=False)


def search_mutants(gene_library_file):
    '''
    '''
    return

def output_to_file():
    '''
    '''
    return

def main(argv=None):
    mutant_library_file = sys.argv[1]
    gene_library_file = sys.argv[2]
    process_mutants(mutant_library_file)
    search_mutants(gene_library_file)

    sys.stdout.write("\nDone")
    return

if __name__ == "__main__":
    main()

