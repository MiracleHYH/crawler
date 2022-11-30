import re


def parse_title(title: str) -> str:
    res = re.sub(r'<font[^>]*>', "", title)
    res = re.sub(r'</font>', "", res)
    return res


def parse_time(pub_time: str) -> str:
    pub_time = re.search(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', pub_time).group(0)
    return re.sub(r':', '-', pub_time)


def parse_content(content: str) -> str:
    content = content.replace('pagebreak', '')
    content = content.replace(u'\u00A0', '')
    content = content.replace(u'\u2002', '')
    content = content.replace(u'\u2003', '')
    return content
