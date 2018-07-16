def print_hash(hash, files):
    print(hash + ':')
    for file in files:
        print('    ' + file)

def print_report(hashes, duplicates_only=False):
    if duplicates_only:
        for hash, files in hashes.items():
            if len(files) > 1:
                print_hash(hash, files)
    else:
        for hash, files in hashes.items():
            print_hash(hash, files)
