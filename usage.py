from read_pdf import read_pdf
from xyz_processor import xyz_processor
from save_xyz import save_xyz

# Example with simple coordinates
pdf_file = "examples/pdf_files/example_coords.pdf"
text = read_pdf(pdf_file)
clean_text = xyz_processor(text, role="clean")
save_xyz(text=clean_text, path_dir="examples/created_xyz/example_coords")

# Example with coordinates on several columns
pdf_file = "examples/pdf_files/example_columns.pdf"
text = read_pdf(pdf_file)
clean_text = xyz_processor(text, role="clean")
save_xyz(text=clean_text, path_dir="examples/created_xyz/example_columns")

# Example with columns and atomic numbers instead of element symbols
pdf_file = "examples/pdf_files/example_atomic_number.pdf"
text = read_pdf(pdf_file)
clean_text = xyz_processor(text, role="clean")
save_xyz(text=clean_text, path_dir="examples/created_xyz/example_atomic_number")

# Example with columns, atomic numbers, and coordinates in table
pdf_file = "examples/pdf_files/example_table.pdf"
text = read_pdf(pdf_file)
clean_text = xyz_processor(text, role="clean")
save_xyz(text=clean_text, path_dir="examples/created_xyz/example_table")