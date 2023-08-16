import re
from typing import Text

def mdconverter(markdown):
    markdown = markdown + "\0"
    markdown = bold(markdown)
    markdown = ul(markdown)
    markdown = headers(markdown)
    markdown = paragraph(markdown)
    return markdown

def ul(markdown):
    symbols = ["-", "\*", "\+"]

    for symbol in symbols:
        beginning = re.compile(rf'(?<=\t|\n){symbol}\s')
        end = re.compile(rf'(?<=\t|\n){symbol}(?!.+\n(?:\t|{symbol}))(?=\s)')
        
        beginning_match = re.search(beginning, markdown)
        end_match = re.search(end, markdown)

        while beginning_match and end_match:
            beginning_match = beginning_match.start()
            end_match = end_match.end()

            while markdown[beginning_match] != "\n":
                beginning_match -= 1
            while markdown[end_match] != "\n" and markdown[end_match] != "\0":
                end_match += 1
            
            temp_text = markdown[beginning_match + 1:end_match + 1]

            if markdown[end_match] == "\0":
                temp_text = "<ul>\n" + temp_text + "\n</ul>"
            else:
                temp_text = "<ul>\n" + temp_text + "</ul>"
            
            sub_text = sub_ul(temp_text, symbol)

            if (sub_text):
                temp_text = sub_text
            
            temp_text = re.sub(beginning, "\t<li>", temp_text)

            matches = [m.end() for m in re.finditer("<li>", temp_text)]

            times = 0        
            for match in matches:
                if times:
                    match += 5 * times
                while temp_text[match] != "\n" and temp_text[match] != "\0":
                    match += 1
                
                if temp_text[match + 2] != "\t":
                    temp_text = temp_text[ : match] + "</li>" + temp_text[match: ]
                    times += 1

            markdown = markdown[ : beginning_match + 1] + temp_text + markdown[end_match: ]
    
            beginning_match = re.search(beginning, markdown)
            end_match = re.search(end, markdown)
    return markdown


def sub_ul(temp_text, symbol):
    tab_beginning = re.compile(rf'(?<=\t){symbol}\s')
    tab_end = re.compile(rf'(?<=\t){symbol}(?!.+\n\t{symbol})(?=\s)')

    beginning_tab_match = re.search(tab_beginning, temp_text)
    end_tab_match = re.search(tab_end, temp_text)
        
    if not beginning_tab_match and not end_tab_match:
        return

    while beginning_tab_match and end_tab_match:
        beginning_tab_match = beginning_tab_match.start()
        end_tab_match = end_tab_match.end()

        while temp_text[beginning_tab_match] != "\n":
            beginning_tab_match -= 1
        while temp_text[end_tab_match] != "\n":
            end_tab_match += 1
                    
        temp_text = temp_text[ : beginning_tab_match + 1] + "\t\t<ul>\n" + temp_text[beginning_tab_match + 1: end_tab_match + 1] + "\t\t</ul>\n" +"\t</li>\n" + temp_text[end_tab_match : ]

        end_tab_match += 20

        matches = [m.start() for m in re.finditer(tab_beginning, temp_text)]
        counter = 0
        for match in matches:
            if match > beginning_tab_match and match < end_tab_match:
                counter += 1
        
        temp_text = re.sub(tab_beginning, "\t\t<li>", temp_text, counter)

        beginning_tab_match = re.search(tab_beginning, temp_text)
        end_tab_match = re.search(tab_end, temp_text)

    matches = [m.end() for m in re.finditer("<li>", temp_text)]

    temp_text = matcher(temp_text, matches, "</li>", 5)

    return temp_text

def headers(markdown):
    markdown = markdown.replace('#', '>', 1)
    markdown = "<h1" + markdown
    
    header_patterns = {}
    header_patterns["h1"] = re.compile(r'(?<=\n)(?<!#)#(?!#)(?=\s)')
    header_patterns["h2"] = re.compile(r'(?<=\n)(?<!#)##(?!#)(?=\s)')
    header_patterns["h3"] = re.compile(r'(?<=\n)(?<!#)###(?!#)(?=\s)')
    header_patterns["h4"] = re.compile(r'(?<=\n)(?<!#)####(?!#)(?=\s)')
    header_patterns["h5"] = re.compile(r'(?<=\n)(?<!#)#####(?!#)(?=\s)')
    header_patterns["h6"] = re.compile(r'(?<=\n)(?<!#)######(?!#)(?=\s)')

    for pattern in header_patterns.items():
        markdown = re.sub(pattern[1], f"<{pattern[0]}>", markdown)
        matches = [m.end() for m in re.finditer(f"<{pattern[0]}>", markdown)]
        
        markdown = matcher(markdown, matches, f" </{pattern[0]}>", 6)
    return markdown


def bold(markdown):
    strong1 = re.compile(r'\*\*(?=.+\*\*)')
    strong2 = re.compile(r'__(?=.+__)')
    
    star_exists = re.search(strong1, markdown)
    underscore_exists = re.search(strong2, markdown)

    while underscore_exists or star_exists:
        markdown = re.sub(strong1, "<strong>", markdown, 1)
        markdown = re.sub(strong2, "<strong>", markdown, 1)
        matches = [m.end() for m in re.finditer(r'<strong>(?!.+</strong>)(?=.+(__|\*\*))', markdown)]
        
        times = 0
        for match in matches:
            if times:
                match += 9 * times
            while markdown[match] != "_" and markdown[match] != "*":
                match += 1
            markdown = markdown[ : match] + "</strong>" + markdown[match + 2: ]
            times += 1

        star_exists = re.search(strong1, markdown)
        underscore_exists = re.search(strong2, markdown)

    return markdown

def paragraph(markdown):
    p_pattern = re.compile(r'\n(?=\w)')

    markdown = re.sub(p_pattern, "\n<p>", markdown)

    matches = [m.end() for m in re.finditer("<p>", markdown)]

    markdown = matcher(markdown, matches, "</p>", 4)

    return markdown


def matcher(text, matches, pattern, len):
    times = 0
    for match in matches:
        if times:
            match += len * times
        while text[match] != "\n" and text[match] != "\0":
            match += 1
        
        text = text[ : match] + f"{pattern}" + text[match : ]
        times += 1
    return text