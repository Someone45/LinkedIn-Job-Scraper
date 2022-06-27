with open('replace.txt', 'r') as file:
    replacer = file.read()

# Read in the file
with open('Table.html', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('<table>', replacer)

# Write the file out again
with open('Table.html', 'w') as file:
  file.write(filedata)
