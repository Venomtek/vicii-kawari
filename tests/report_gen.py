#!/usr/bin/env python3

from pathlib import Path


def print_log_excerpt(log_path: Path) -> None:
    if not log_path.exists():
        print("DID NOT RUN")
        return

    count = 0
    with log_path.open(encoding="utf-8", errors="replace") as log_file:
        for line in log_file:
            line = line.rstrip("\n")
            if line.startswith("INFO: next xpos"):
                continue
            print(line)
            count += 1
            if count == 10:
                break


def main() -> None:
    print("<body>")
    print("<table>")

    with Path("list.txt").open(encoding="utf-8", errors="replace") as list_file:
        for line in list_file:
            line = line.rstrip("\n")
            if not line:
                continue

            separator = line.rfind("/")
            if separator == -1:
                raise ValueError(f"test path has no directory: {line}")

            directory = line[:separator]
            filename = line[separator + 1 :]
            web_directory = f"tests/{directory}"

            print("<tr>")
            print("<td>")
            print(line)
            print("</td>")
            print("</tr>")

            print("<tr>")
            print("<td>")
            print(
                f'<a target=_blank href="{web_directory}/vice_{filename}.png">'
                f'<img src="{web_directory}/vice_{filename}.png"></img></a>'
            )
            print("</td>")
            print("<td>")
            print(
                f'<a target=_blank href="{web_directory}/fpga_{filename}.png">'
                f'<img src="{web_directory}/fpga_{filename}.png"></img></a>'
            )
            print("</td>")
            print("<td>")
            print('<textarea rows="10" cols="50">')
            print_log_excerpt(Path(directory) / f"vice_{filename}.log")
            print("</textarea>")
            print("</td>")
            print("</tr>")

    print("</table>")
    print("</body>")


if __name__ == "__main__":
    main()
