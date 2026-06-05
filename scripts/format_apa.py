import json
import re

json_path = "/Users/ahmadhidayat/.gemini/antigravity-cli/brain/1c5e6391-0a3d-42a1-b3d8-3eebbbda984f/scratch/ensitrelvir_abstracts.json"

with open(json_path, 'r') as f:
    abstracts = json.load(f)

def format_apa(pub):
    # Format authors
    authors = pub.get('authors', [])
    formatted_authors = []
    for author in authors:
        parts = author.strip().split()
        if len(parts) > 1:
            last = parts[0]
            initials = "".join([f"{part[0]}." for part in parts[1:]])
            formatted_authors.append(f"{last}, {initials}")
        else:
            formatted_authors.append(author)
    
    if not formatted_authors:
        author_str = "Unknown Author"
    elif len(formatted_authors) == 1:
        author_str = formatted_authors[0]
    elif len(formatted_authors) == 2:
        author_str = f"{formatted_authors[0]} & {formatted_authors[1]}"
    elif len(formatted_authors) > 20:
        author_str = ", ".join(formatted_authors[:19]) + ", ... " + formatted_authors[-1]
    else:
        author_str = ", ".join(formatted_authors[:-1]) + ", & " + formatted_authors[-1]
    
    # Format date (extract year)
    pubdate = pub.get('pubdate', '')
    year_match = re.search(r'\d{4}', pubdate)
    year = year_match.group(0) if year_match else "n.d."
    
    title = pub.get('title', '').strip()
    if title.endswith('.'):
        title = title[:-1]
    
    # Capitalize only first letter of title and first letter of subtitle (after colon)
    # Actually, APA has sentence case for titles. But let's keep it clean.
    
    journal = pub.get('journal', '').strip()
    # Title-case the journal name
    journal = journal.title()
    
    doi = pub.get('doi', '')
    doi_str = f" https://doi.org/{doi}" if doi else ""
    
    pmid = pub.get('pmid', '')
    pmid_str = f" (PMID: {pmid})"
    
    return f"{author_str} ({year}). {title}. *{journal}*{doi_str}{pmid_str}"

for p in abstracts:
    print(f"PMID: {p['pmid']}")
    print(format_apa(p))
    print("-" * 40)
