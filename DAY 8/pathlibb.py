from pathlib import Path

the_data_dir = Path("DAY 8/data")
the_file_path = the_data_dir / "user_data.txt"

print(the_file_path.exists())
print(the_file_path.name)
print(the_file_path.suffix)

students = [
    {"name": "Alice", "age": 24, "grade": "A"},
    {"name": "Bob", "age": 22, "grade": "B"}
]

the_data_dir.mkdir(exist_ok=True)
the_file_path.write_text(f"{students}",encoding="utf-8")
print(the_file_path.read_text(encoding="utf-8"))