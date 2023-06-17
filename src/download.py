import click
import pandas as pd


@click.group()
def cli():
    """Download satellite data."""
    pass


@cli.command()
def satnogs():
    """Download data from JE9PEL's website."""
    url = "https://db.satnogs.org/api/satellites.json"
    df = pd.read_json(url)
    df.norad_cat_id = df.norad_cat_id.astype(int, errors="ignore")
    df.to_csv("./data/satnogs.csv", index=False)
    df.to_json("./data/satnogs.json", orient="records", indent=2)


@cli.command()
def je9pel():
    """Download data from JE9PEL's website."""
    # Download the data
    url = "http://www.ne.jp/asahi/hamradio/je9pel/satslist.csv"
    fields = [
        "name",
        "norad_id",
        "uplink",
        "downlink",
        "beacon",
        "mode",
        "callsign",
        "status",
    ]
    df = pd.read_csv(
        url,
        delimiter=";",
        header=None,
        names=fields,
        dtype=str,
        on_bad_lines="warn",
    )

    # Strip all whitespace
    for c in df.columns:
        df[c] = df[c].str.strip()

    # Lowercase all the statuses
    df.status = df.status.str.lower()

    # Merge in SatNOGS ids
    satnogs = pd.read_csv(
        "./data/satnogs.csv", usecols=["sat_id", "norad_cat_id"], dtype=str
    ).rename(columns={"sat_id": "satnogs_id", "norad_cat_id": "norad_id"})
    satnogs = satnogs[~pd.isnull(satnogs.norad_id)].copy()
    satnogs.norad_id = satnogs.norad_id.str.replace(".0", "", regex=False)
    merged = df.merge(satnogs, on="norad_id", how="left")
    assert len(merged) == len(df)

    # Write out
    merged.to_csv("./data/amsat-all-frequencies.csv", index=False)
    merged.to_json("./data/amsat-all-frequencies.json", orient="records", indent=2)

    # Filter to active, then write that out
    active_df = merged[merged.status == "active"].drop(["status"], axis=1).copy()
    active_df.to_csv("./data/amsat-active-frequencies.csv", index=False)
    active_df.to_json(
        "./data/amsat-active-frequencies.json", orient="records", indent=2
    )


if __name__ == "__main__":
    cli()
