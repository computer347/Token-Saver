Next, people need their data to persist. Some will keep a simple JSON file they can back up and read; others prefer SQLite. Older JSON files from an earlier version of the app also have to keep working. Please add storage that matches this interface exactly:

{{CONTRACT}}

Add tests for the new behaviour and keep the whole suite passing.
