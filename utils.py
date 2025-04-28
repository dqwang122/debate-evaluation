import re

def remove_citation(text: str, keep_main=False) -> str:
    """
    Remove citations in formats like (1), (1,2), [1], [1,2,3] from text.
    
    Args:
        text (str): Input text containing citations
        
    Returns:
        str: Text with citations removed
    """
    # Remove citations with parentheses ()
    statement = re.sub(r"[\*]*Reference[\S]*[\*]*", "Reference", text)
    statement = statement.replace("## Reference", "Reference")
    statement = statement.replace("Reference", "**Reference**")


    if "**Reference**" in statement:
        content, reference = statement.split("**Reference**")[:2]
    else:
        content, reference = statement, ''

    if not keep_main:
        pattern = r'\([^()]*\)'
        content = re.sub(pattern, '', content)
        
        # Remove citations with square brackets []
        pattern = r'\[[^\[\]]*\]'
        content = re.sub(pattern, '', content)
        
        # Remove extra whitespace that might be left
        # content = re.sub(r'\s+', ' ', content)
    
    return content.strip(), reference.strip()