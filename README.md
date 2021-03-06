# High-Density-Transposon-Mutant-Library

Script to process large mutant library data file by removing redundancies and to search, for each B. cenocepacia K56-2 essential/non-essential genes, mutants presenting the gene. 

Module requirements:
- pandas (pip install pandas)
- xlrd (pip install xlrd)
- xlsxwriter (pip install xlsxwriter)

How to run:
- Windows: *python MutantSearcher.py mutant_library reference_library processed_library*
- Linux (lab computer): *python3 MutantSearcher.py mutant_library reference_library processed_library*

  - mutant_library: mutant library Excel file
  - reference_library: reference essential genes library Excel file
  - processed_library: (Optional) add "true" to the end of the command if want to output processed mutant library csv file (only unique mutants, remove duplicate mutants)

Note: output excel (EssentialGenesMutants.xlsx) will contain 4 sheets; unique essential mutants; Essential mutants summary stats; then two sheets same as before but for non-essential mutants

Note: the reference_library MUST be the supplementary data excel file from Gislason et al. 2018. Microbial 
Genomics that lists all essential genes in K56-2. Do not edit this file, the script will only recognize the input in the default format
