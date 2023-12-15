from collections.abc import Callable
import re
from sys import path
path.append("../")
import unit_test

def SanitizeInput(x: list[str]) -> str:
    """Cleans the user text to protect against injections

    Args:
        x: The string to clean

    Returns:
        The cleaned string
    """
    x = "".join(x)
    x = x.replace("&", "&amp;")
    x = x.replace("<", "&lt;")
    x = x.replace(">", "&gt;")
    x = x.replace("\"", "&quot;")
    x = x.replace("\'", "&apos;")
    return x

def AddNewlines(x: str) -> str:
    """Replaces newline escape characters with HTML newlines

    Args:
        x: The text to edit

    Returns:
        The edited text
    """
    return x.replace("\n", "<br>")

def StyleText(x: str, styling: dict[str, Callable[[str], str]]) -> str:
    """Makes a substitution in the user-submitted text

    Args:
        x: The text to edit
        styling: A dictionary of regex, function pairs, where the function determines how the text should be replaced

    Returns:
        The edited text
    """
    for old, repFunc in styling.items():
        for s in re.findall(old, x):
            x = x.replace(s, repFunc(s), 1)
    return x

def IsHex(x: str) -> bool:
    """Determines if a string represents a hex color

    Args:
        x: The color to determine

    Returns:
        True if it does represent a hex character, False otherwise
    """
    if not len(x) == 7:
        return False
    for char in x[1:]:
        if not char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"]:
            return False
    return True

def GetColor(x: str) -> str:
    """Determines the user-specified color. It may be one of a few pre-specified colors, or a hex color.
    If the input does not follow this format, it will default to black.

    Args:
        x: The color the user specified

    Returns:
        The actual color
    """
    colors = ["black", "red", "green", "blue", "yellow", "purple"]
    col = x.split()[-1].rstrip("\\")
    if col in colors or (col[0] == "#" and len(col[1:])):
        return col
    return "black"

def GetSize(x: str) -> str:
    """Determines the user-specified font-size. It must be an int. If it isn't, it will default to 12.

    Args:
        x: The user specified size

    Returns:
        The font size
    """
    size = x.split()[-1].rstrip("\\")
    return size if size.isdigit() else "12"

def FormatDocumentation(x: str) -> str:
    """Handles all functions relating to cleaning and formatting user-inputted text.
    This function sanitizes, adds new lines, and styles the text.

    Args:
        x: The text to be formatted

    Returns:
        The formatted text
    """
    #size, italic, bold, color, links, justify, bullet points

    backslash = "\\"

    styling = {
        "\[b\]": lambda _: "<b>",
        "\[\/b\]": lambda _: "</b>",
        "\[it\]": lambda _: "<em>",
        "\[\/it\]": lambda _: "</em>",
        "\[color .+?\]": lambda x: f"<span style=\"color:{GetColor(x)};\">",
        "\[\/color\]": lambda _: "</span>",
        "\[size \d+?\]": lambda x: f"<span style=\"font-size:{GetSize(x)}px;\">",
        "\[\/size\]": lambda _: "</span>",
        "\[hplk .+?\]": lambda x: f"<a href={x.split()[-1].rstrip(backslash)}>",
        "\[\/hplk\]": lambda _: "</a>",
        "\[center\]": lambda _: "<p style=\"margin: 0 auto; text-align: center;\">",
        "\[\/center\]": lambda _: "</p>",
        "\[right\]": lambda _: "<p style=\"margin: 0 auto; text-align: right;\">",
        "\[\/right\]": lambda _: "</p>",
        "\[list\]": lambda _: "<ul>",
        "\[\/list\]": lambda _: "</ul>",
        "\[#list\]": lambda _: "<ol>",
        "\[\/#list\]": lambda _: "</ol>",
        "\[\*\]": lambda _: "<li>",
        "\[\/\*\]": lambda _: "</li>",
    }

    return StyleText(AddNewlines(SanitizeInput(x)), styling)

if __name__ == "__main__":
    unit_test.UnitTest(SanitizeInput, ("<script>alert(\"Evil text here >:)\")</script>",),
                       ("&lt;script&gt;alert(&quot;Evil text here &gt;:)&quot;)&lt;/script&gt;",))
    
    unit_test.UnitTest(AddNewlines, ("Hello\nThis is text\nGoodbye!",), ("Hello<br>This is text<br>Goodbye!",))

    unit_test.UnitTest(IsHex, ("#FFFFFF",), (True,))
    unit_test.UnitTest(IsHex, ("#FFFF",), (False,))
    unit_test.UnitTest(IsHex, ("#FFFFFFFF",), (False,))
    unit_test.UnitTest(IsHex, ("#FF05dg",), (False,))

    unit_test.UnitTest(GetColor, ("#FF05dg",), ("#FF05dg",))
    unit_test.UnitTest(GetColor, ("green",), ("green",))
    unit_test.UnitTest(GetColor, ("pink",), ("black",))

    unit_test.UnitTest(GetSize, ("12",), ("12",))
    unit_test.UnitTest(GetSize, ("40",), ("40",))
    unit_test.UnitTest(GetSize, ("big",), ("12",))

    unit_test.UnitTest(FormatDocumentation, ("[b]Bold[/b]",), ("<b>Bold</b>",))
    unit_test.UnitTest(FormatDocumentation, ("[it]Bold[/it]",), ("<em>Bold</em>",))
