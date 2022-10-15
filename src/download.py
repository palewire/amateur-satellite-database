import click
import pandas as pd


@click.command()
def cli():
    """Download data from JE9PEL's website."""
    # Download the data
    url = "http://www.ne.jp/asahi/hamradio/je9pel/satslist.csv"
    df = pd.read_csv(url, delimiter=";", header=None, on_bad_lines="warn", dtype=str)

    # Name the columns
    df.columns = [
        "satellite",
        "number",
        "uplink",
        "downlink",
        "beacon",
        "mode",
        "callsign",
        "status",
    ]

    # Strip all whitespace
    for c in df.columns:
        df[c] = df[c].str.strip()

    # Write out
    df.to_csv("./data/satellites.csv", index=False)
    df.to_json("./data/satellites.json", orient="records", indent=2)


if __name__ == "__main__":
    cli()
