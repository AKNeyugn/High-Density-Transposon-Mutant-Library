import sys
import numpy as np
import pandas as pd


gene_mutant_dict = {}
processed_mutant_library = "ProcessedMutantLibrary.xlsx"
output = "EssentialGenesMutants.xlsx"

def process_mutants(mutant_library_file):
    '''
    Filter mutant library for unique gene annotations (ignoring position,
    read count, gene IDs and length) into a new Excel file

    Args:
        mutant_library_file (string): File name of HDTM library
    '''

    with pd.ExcelFile(mutant_library_file) as xls:
        df = pd.read_excel(xls, "Sheet1", keep_default_na=False, na_values=[""])
        prev_cog = u""
        prev_locus_tag = u""
        for index, row in df.iterrows():
            if (row['CDS strand'] != "N/A"):
                if (row['COG'] != unicode(prev_cog) and row['Locus tag'] != unicode(prev_locus_tag)):
                    print(row['COG'], row['Locus tag'])
                    prev_cog = row['COG']
                    prev_locus_tag = row['Locus tag']


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

    print("Done")
    return

if __name__ == "__main__":
    main()

