import click
import pandas as pd


@click.command()
def cli():
    """Download data from JE9PEL's website."""
    # Download the data
    url = "http://www.ne.jp/asahi/hamradio/je9pel/satslist.csv"
    df = pd.read_csv(url, delimiter=";", header=None, dtype=str)

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

    # Lowercase all the statuses
    df.status = df.status.str.lower()

    # Write out
    df.to_csv("./data/all-frequencies.csv", index=False)
    df.to_json("./data/all-frequencies.json", orient="records", indent=2)

    # Filter to active, then write that out
    active_df = df[df.status == "active"].drop(["status"], axis=1).copy()
    active_df.to_csv("./data/active-frequencies.csv", index=False)
    active_df.to_json("./data/active-frequencies.json", orient="records", indent=2)


if __name__ == "__main__":
    cli()
