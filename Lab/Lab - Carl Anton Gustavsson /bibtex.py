# Bibtext module


def extract_author(str):
    s = str.split(" ")
    if "," in str:
        t = str.split(",")
        first = t[1]
        last = t[0]
        first = first.strip()
        last = last.strip()
        author = (last, first)
        return author
    if len(s) == 1:
        return (str, "")
    if len(s) == 2:
        return (s[1], s[0])
    else:
        return (s[2], s[0] + " " + s[1])

def extract_authors(str):
    l = str.split(" and ")
    authors = []
    print(l)
    for i in l:
        authors.append(extract_author(i))
    return authors
