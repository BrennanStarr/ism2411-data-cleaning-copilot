# Reflection on using Copilot for data cleaning

What Copilot generated
- I used GitHub Copilot to generate starter code for several functions, primarily `load_data` and `clean_column_names`.
- I triggered suggestions by writing clear comments above the function stubs (e.g., "Load the CSV file into a pandas DataFrame"). Copilot produced reasonable code that I accepted as a starting point.

What I modified
- I changed the generated code to be more defensive: I forced reading the raw CSV as strings, added a helper `_to_numeric_clean` to robustly remove currency symbols, and adjusted how missing prices and quantities are handled (fill `quantity` with 1 and `price` with the median).
- I also renamed and reorganized small pieces to make behavior explicit and reproducible.

What I learned
- Copilot is fast at suggesting straightforward boilerplate (reading a CSV, normalizing column names), but its suggestions may assume ideal input. Real messy data needs explicit, defensive cleaning steps.
- Example: Copilot's initial suggestion didn't handle currency symbols like `$10.00` or values like `N/A`. Adding `_to_numeric_clean` to strip non-numeric characters and coerce safely was necessary.

Overall, Copilot was a useful assistant for scaffolding, but human review and targeted edits were essential for correctness.
