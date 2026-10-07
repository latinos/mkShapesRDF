"""Yield and MC composition reports for an mkShapesRDF analysis folder."""

import argparse
from contextlib import ExitStack, contextmanager, redirect_stdout
import csv
import io
import math
import os
from pathlib import Path
import runpy
import sys
import zlib

import cloudpickle
import ROOT
from tabulate import tabulate

ROOT.gROOT.SetBatch(True)


@contextmanager
def open_root(path):
    path = str(path)
    source = ROOT.TFile.Open(path, "READ")
    if not source or source.IsZombie():
        raise OSError(f"Could not open ROOT file: {path}")
    try:
        yield source
    finally:
        source.Close()


def load_config(config_file, configs_folder):
    if config_file:
        path = Path(config_file)
    else:
        paths = list(Path(configs_folder).glob("*.pkl"))
        if not paths:
            raise ValueError("No compiled configuration found; run mkShapesRDF -c 1 first")
        path = max(paths, key=lambda p: (p.stat().st_mtime_ns, p.name))

    if not path.exists():
        raise FileNotFoundError(f"Compiled configuration does not exist: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Compiled configuration is empty: {path}")

    with path.open("rb") as stream:
        return cloudpickle.loads(zlib.decompress(stream.read()))


def region_names(cuts):
    """Expand categories without moving their parent relative to other cuts."""
    names = []

    for name, cut in cuts.items():
        if isinstance(cut, dict) and cut.get("categories"):
            names.extend(region_names({f"{name}_{category}": definition for category, definition in cut["categories"].items()}))
        else:
            names.append(name)

    if len(names) != len(set(names)):
        raise ValueError("Cuts produce duplicate region names")

    return names


def sample_names(samples):
    names = []

    for name, sample in samples.items():
        if "subsamples" in sample:
            naming = sample.get("flatten_samples_map", lambda name, sub: f"{name}_{sub}")
            names.extend(naming(name, sub) for sub in sample["subsamples"])
        else:
            names.append(name)

    if len(names) != len(set(names)):
        raise ValueError("Samples produce duplicate names")

    return names


def select_names(available, selection, label):
    selected = available if selection is None else [name.strip() for name in selection.split(",")]

    if not selected or len(selected) != len(set(selected)):
        raise ValueError(f"Select at least one {label}, without duplicates")

    unknown = [name for name in selected if name not in available]

    if unknown:
        raise ValueError(f"Unknown {label}: {', '.join(unknown)}")

    return selected


def histogram_yield(histogram, include_flow=False):
    dimension = histogram.GetDimension()
    nx = histogram.GetNbinsX()
    ny = histogram.GetNbinsY() if dimension >= 2 else 1
    nz = histogram.GetNbinsZ() if dimension >= 3 else 1

    xr = range(0, nx + 2) if include_flow else range(1, nx + 1)
    yr = range(0, ny + 2) if include_flow and dimension >= 2 else range(1, ny + 1)
    zr = range(0, nz + 2) if include_flow and dimension >= 3 else range(1, nz + 1)

    yield_value = 0.0
    variance = 0.0

    for ix in xr:
        for iy in yr:
            for iz in zr:
                if dimension == 1:
                    bin_number = histogram.GetBin(ix)
                elif dimension == 2:
                    bin_number = histogram.GetBin(ix, iy)
                else:
                    bin_number = histogram.GetBin(ix, iy, iz)

                value = histogram.GetBinContent(bin_number)
                error = histogram.GetBinError(bin_number)

                yield_value += value
                variance += error * error

    return yield_value, variance


def collect_yields(input_file, regions, samples, variable, include_flow=False, tag=None):
    """Return (sum of weights, statistical error) for every region/sample."""

    with ExitStack() as stack:
        if Path(input_file).is_dir():
            if not tag:
                raise ValueError("An input directory requires --tag or a configuration tag")

            files = {
                sample: stack.enter_context(open_root(Path(input_file) / f"plots_{tag}_ALL_{sample}.root"))
                for sample in samples
            }
        else:
            source = stack.enter_context(open_root(input_file))
            files = dict.fromkeys(samples, source)

        rows = []

        for region in regions:
            row = []

            for sample in samples:
                key = f"{region}/{variable}/histo_{sample}"
                histogram = files[sample].Get(key)

                if not histogram:
                    raise ValueError(f"Missing histogram: {key} in {files[sample].GetName()}")

                if not histogram.InheritsFrom("TH1"):
                    raise ValueError(f"Expected a histogram at {key}")

                yield_value, variance = histogram_yield(histogram, include_flow)

                if not math.isfinite(yield_value) or not math.isfinite(variance) or variance < 0:
                    raise ValueError(f"Invalid yield or variance for {key}")

                row.append((yield_value, math.sqrt(variance)))

            rows.append(row)

        return rows


def render_table(regions, samples, yields, table_format="text", precision=2, data=None):
    data = set() if data is None else data

    if table_format == "csv":
        output = io.StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(["cut"] + [column for sample in samples for column in (sample, f"{sample}_stat")])

        for region, row in zip(regions, yields):
            writer.writerow([region] + [value for sample, (value, error) in zip(samples, row) for value in (value, "" if sample in data else error)])

        return output.getvalue()

    rows = [
        [region] + [f"{value:.{precision}f}" if sample in data else f"{value:.{precision}f} +/- {error:.{precision}f}" for sample, (value, error) in zip(samples, row)]
        for region, row in zip(regions, yields)
    ]

    formats = {"text": "simple", "markdown": "github", "latex": "latex"}
    return tabulate(rows, headers=["Cut"] + samples, tablefmt=formats[table_format], disable_numparse=True) + "\n"


def defaultParser():
    parser = argparse.ArgumentParser(
        description="Write yield and MC composition tables for cuts.py regions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-f", "--folder", default=".", help="Analysis directory")
    parser.add_argument("--pycfg", default="configuration.py", help="Analysis configuration")
    parser.add_argument("--configFile", help="Use a compiled .pkl instead of --pycfg")
    parser.add_argument("--configsFolder", help="Use the latest compiled .pkl in this folder instead of --pycfg")
    parser.add_argument("--cutsFile", help="Override the configured cutsFile")
    parser.add_argument("--inputFile", help="Merged shapes file (or per-sample directory with compiled config)")
    parser.add_argument("--variable", "--onlyVariable", default="events", help="Scalar yield histogram")
    parser.add_argument("--onlyCut", help="Comma-separated flattened region names")
    parser.add_argument("--onlySample", help="Comma-separated nominal sample names")
    parser.add_argument("--dataSamples", help="Comma-separated data names; overrides automatic classification")
    parser.add_argument("--outputDir", default=".", help="Directory for the three CSV tables")
    parser.add_argument("--excludeFlow", action="store_true", help="Exclude underflow and overflow")
    parser.add_argument("--precision", type=int, default=3, help="Displayed yield precision (CSV keeps full precision)")
    parser.add_argument("--tag", help="Override the configuration tag")
    parser.add_argument("--format", choices=["text", "markdown", "csv", "latex"], help="Produce a region-by-sample table instead of the three CSV reports")
    parser.add_argument("--outputFile", help="Save a formatted table (defaults to text unless --format is supplied)")

    return parser


@contextmanager
def analysis_directory(folder):
    """Resolve the same relative imports and paths as running inside an example."""
    previous = Path.cwd()
    previous_path = sys.path[:]

    os.chdir(folder)
    sys.path.insert(0, str(Path.cwd()))

    try:
        yield
    finally:
        os.chdir(previous)
        sys.path[:] = previous_path


def read_configuration(args):
    if args.configFile or args.configsFolder:
        config = load_config(args.configFile, args.configsFolder or "configs")
        cuts = config["cuts"]

        if isinstance(cuts.get("cuts"), dict) and "preselections" in cuts:
            cuts = cuts["cuts"]
    else:
        with redirect_stdout(sys.stderr):
            config = runpy.run_path(args.pycfg)
            namespace = runpy.run_path(args.cutsFile or config.get("cutsFile", "cuts.py"), init_globals={**config, "cuts": {}})

        cuts = namespace["cuts"]

    if (args.configFile or args.configsFolder) and args.cutsFile:
        with redirect_stdout(sys.stderr):
            cuts = runpy.run_path(args.cutsFile, init_globals={**config, "cuts": {}})["cuts"]

    return config, cuts


def discover_samples(input_file, regions, variable):
    """Discover nominal histograms without dropping genuine sample prefixes."""
    names = set()

    with open_root(input_file) as source:
        for region in regions:
            directory = source.GetDirectory(f"{region}/{variable}")

            if not directory:
                raise ValueError(f"Missing histogram directory: {region}/{variable}")

            for key in directory.GetListOfKeys():
                name = key.GetName()
                classname = key.GetClassName()

                if name.startswith("histo_") and classname.startswith(("TH1", "TH2", "TH3")):
                    sample = name[len("histo_"):]

                    if not sample.endswith(("Up", "Down")) and "SPECIAL_NUIS" not in sample:
                        names.add(sample)

    if not names:
        raise ValueError("No nominal histograms found")

    return sorted(names)


def data_samples(config, samples, override=None):
    if override is not None:
        return set(select_names(samples, override, "data sample"))

    names = {sample for sample in samples if sample.upper() == "DATA"}

    for sample, definition in config.get("samples", {}).items():
        if definition.get("isData"):
            names.update(sample_names({sample: definition}))

    for sample, definition in config.get("structure", {}).items():
        if definition.get("isData"):
            names.add(sample)

    return names.intersection(samples)


def composition_rows(regions, samples, yields, data):
    rows = []

    for region, values in zip(regions, yields):
        total = sum(pair[0] for sample, pair in zip(samples, values) if sample not in data)

        for sample, (value, _) in zip(samples, values):
            fraction = None if sample in data or total == 0 else 100.0 * value / total
            rows.append([region, sample, value, fraction])

    return rows


def write_csv(path, header, rows):
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def report(config, regions, samples, yields, data, output_dir, precision):
    tag = str(config["tag"])
    order = sorted(range(len(samples)), key=lambda index: yields[0][index][0], reverse=True)

    samples = [samples[index] for index in order]
    yields = [[row[index] for index in order] for row in yields]

    wide = [[sample] + [row[index][0] for row in yields] for index, sample in enumerate(samples)]
    long = [[region, sample, pair[0]] for region, values in zip(regions, yields) for sample, pair in zip(samples, values)]
    composition = composition_rows(regions, samples, yields, data)

    output_dir.mkdir(parents=True, exist_ok=True)

    paths = [
        output_dir / f"yields_{tag}.csv",
        output_dir / f"yields_{tag}_long.csv",
        output_dir / f"composition_{tag}.csv",
    ]

    write_csv(paths[0], ["Sample"] + regions, wide)
    write_csv(paths[1], ["Cut", "Sample", "Yield"], long)
    write_csv(paths[2], ["Cut", "Sample", "Yield", "Composition_percent"], composition)

    print("NOMINAL YIELDS\n")
    print(tabulate(wide, headers=["Sample"] + regions, floatfmt=f".{precision}f", disable_numparse=True))

    print("\nSAMPLE COMPOSITION")

    for region in regions:
        print(f"\n--- {region} ---\n")

        for _, sample, value, fraction in sorted((row for row in composition if row[0] == region), key=lambda row: row[2], reverse=True):
            line = f"{sample:45s}{value:14.{precision}f}"

            if sample not in data:
                line += f"{fraction:10.2f}%" if fraction is not None else "       N/A"

            print(line)

    print("\nOUTPUT")

    for path in paths:
        print(path.resolve())


def main(argv=None):
    parser = defaultParser()
    args = parser.parse_args(argv)

    if args.precision < 0:
        parser.error("--precision must be nonnegative")

    with analysis_directory(args.folder):
        config, cuts = read_configuration(args)

        if args.tag:
            config["tag"] = args.tag

        regions = select_names(region_names(cuts), args.onlyCut, "cut")
        input_file = args.inputFile or str(Path(config["outputFolder"]) / config.get("outputFile", f"mkShapes__{config['tag']}.root"))

        print(f"[mkCutFlow] Input: {input_file}", file=sys.stderr)
        print(f"[mkCutFlow] Variable: {args.variable}", file=sys.stderr)
        print(f"[mkCutFlow] Regions: {', '.join(regions)}", file=sys.stderr)

        is_remote = input_file.startswith(("root://", "http://", "https://"))

        if not is_remote:
            input_path = Path(input_file)

            if not input_path.exists():
                raise FileNotFoundError(f"Input does not exist: {input_file}")

            if input_path.is_file() and input_path.stat().st_size == 0:
                raise ValueError(f"Input ROOT file is empty: {input_file}")

        if args.configFile or args.configsFolder:
            available = sample_names(config["samples"])
        else:
            if not is_remote and Path(input_file).is_dir():
                raise ValueError("A per-sample input directory requires --configFile or --configsFolder")

            available = discover_samples(input_file, regions, args.variable)

        samples = select_names(available, args.onlySample, "sample")

        print(f"[mkCutFlow] Samples: {len(samples)}", file=sys.stderr)

        data = data_samples(config, samples, args.dataSamples)
        yields = collect_yields(input_file, regions, samples, args.variable, not args.excludeFlow, config.get("tag"))

        if args.format or args.outputFile:
            table = render_table(regions, samples, yields, args.format or "text", args.precision, data)

            if args.outputFile:
                Path(args.outputFile).write_text(table)
            else:
                sys.stdout.write(table)
        else:
            report(config, regions, samples, yields, data, Path(args.outputDir), args.precision)


if __name__ == "__main__":
    main()
