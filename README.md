# High-Density-Transposon-Mutant-Library

Script to process large mutant library data file by removing redundancies and to search, for each B. cenocepacia K56-2 essential/non-essential genes, mutants presenting the gene. 

Script expected runtime: ~5 minutes

Module requirements:
- pandas (pip install pandas)
- xlrd (pip install xlrd)
- xlsxwriter (pip install xlsxwriter)

How to run:
- Windows: python MutantSearcher.py mutant_library reference_library processed_library
- Linux (lab computer): sudo python3 MutantSearcher.py mutant_library reference_library processed_library

  - mutant_library: mutant library Excel file
  - reference_library: reference essential genes library Excel file
  - processed_library: (Optional) "true" if want to output processed mutant library Excel file
