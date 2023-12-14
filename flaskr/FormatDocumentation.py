from collections.abc import Callable
import re

def SanitizeInput(x: list[str]) -> str:
    x = "".join(x)
    x = x.replace("&", "&amp;")
    x = x.replace("<", "&lt;")
    x = x.replace(">", "&gt;")
    x = x.replace("\"", "&quot;")
    x = x.replace("\'", "&apos;")
    return x

def AddNewlines(x: str) -> str:
    return x.replace("\n", "<br>")

def StyleText(x: str, styling: dict[str, Callable]) -> str:
    for old, repFunc in styling.items():
        for s in re.findall(old, x):
            x = x.replace(s, repFunc(s), 1)
    return x

def IsHex(x: str):
    if not len(x) == 7:
        return False
    for char in x[1:]:
        if not char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"]:
            return False
    return True

def GetColor(x: str):
    colors = ["black", "red", "green", "blue", "yellow", "purple"]
    col = x.split()[-1][:-1]
    if col in colors or (col[0] == "#" and len(col[1:])):
        return col
    return "black"

def GetSize(x: str):
    size = x.split()[-1][:-1]
    return size if size.isdigit() else 12

def GetBulletPoints(x: str):
    print(x)

def FormatDocumentation(x: str) -> str:
    #size, italic, bold, color, links, justify, bullet points

    styling = {
        "\[b\]": lambda _: "<b>",
        "\[\/b\]": lambda _: "</b>",
        "\[it\]": lambda _: "<em>",
        "\[\/it\]": lambda _: "</em>",
        "\[color .+?\]": lambda x: f"<span style=\"color:{GetColor(x)};\">",
        "\[\/color\]": lambda _: "</span>",
        "\[size \d+?\]": lambda x: f"<span style=\"font-size:{GetSize(x)}px;\">",
        "\[\/size\]": lambda _: "</span>",
        "\[hplk .+?\]": lambda x: f"<a href={x.split()[-1][:-1]}>",
        "\[\/hplk\]": lambda _: "</a>",
        "\[center\]": lambda _: "<p style=\"margin: 0 auto; text-align: center;\">",
        "\[\/center\]": lambda _: "</p>",
        "\[right\]": lambda _: "<p style=\"margin: 0 auto; text-align: right;\">",
        "\[\/right\]": lambda _: "</p>",
        "\[list\]": lambda _: "<ul>",
        "\[\/list\]": lambda _: "</ul>",
        "\[\*\]": lambda _: "<li>",
        "\[\/\*\]": lambda _: "</li>",
    }

    return StyleText(AddNewlines(SanitizeInput(x)), styling)